#!/usr/bin/env python3
"""Validate a branch name against the project's convention.

Settings come from .thunai/config/project.config.json: "branch" (prefix, types, ...),
plus top-level "teams" and "activeTeam". Format:
  <username>/<prefix>[-team-<team>]-sprint-<NN>-<type>-<issue>-<short-name>
The "-team-<team>" segment is present only when more than one team is configured.
  single team: jdoe/acme-sprint-01-feat-123-login-form
  multi team:  jdoe/acme-team-web-sprint-01-feat-123-login-form

Usage: validate_branch.py [NAME] [--expect-user LOGIN] [--json]
  NAME defaults to the current branch.
Exit 0 ok (warnings allowed), 1 invalid, 2 error.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROTECTED = ("main", "master", "develop", "release")
DEFAULTS = {"prefix": "project", "types": ["feat", "bug", "enh", "task", "docs", "hotfix"],
            "requireIssueNumber": True, "maxLength": 100}
SEGMENT = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def slug(text):
    """Team name -> branch-safe segment (lowercase, hyphen-separated)."""
    return re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower()).strip("-")


def load_config():
    cfg = dict(DEFAULTS)
    data = {}
    try:
        data = json.loads((ROOT / ".thunai" / "config" / "project.config.json").read_text(encoding="utf-8"))
        cfg.update(data.get("branch") or {})
    except (OSError, json.JSONDecodeError):
        pass
    cfg["teams"] = [s for s in (slug(t) for t in (data.get("teams") or [])) if s] or ["core"]
    cfg["activeTeam"] = slug(data.get("activeTeam")) or None
    return cfg


def example(cfg):
    team = f"-team-{'|'.join(cfg['teams'])}" if len(cfg["teams"]) > 1 else ""
    return f"<username>/{cfg['prefix']}{team}-sprint-<NN>-<{'|'.join(cfg['types'])}>-" \
           + ("<issue>-" if cfg["requireIssueNumber"] else "[<issue>-]") + "<short-name>"


def normalize_user(login):
    """GitHub login -> branch-safe username (lowercase, underscores become hyphens)."""
    return re.sub(r"_", "-", (login or "").strip().lower())


def validate(name, cfg=None, expect_user=None):
    """Return (problems, warnings, parts). parts is None when the name is invalid."""
    cfg = cfg or load_config()
    problems, warnings = [], []
    if name in PROTECTED:
        return [f"'{name}' is a protected branch name; create a task branch ({example(cfg)})"], [], None
    if len(name) > cfg["maxLength"]:
        problems.append(f"too long ({len(name)} chars, max {cfg['maxLength']}); shorten the short-name")
    if re.search(r"[A-Z]", name):
        problems.append("use lowercase only")
    if re.search(r"[^A-Za-z0-9/-]", name):
        problems.append("only letters, digits and hyphens are allowed (no spaces, underscores or dots)")
    if name.count("/") != 1:
        problems.append("exactly one '/' is required: <username>/<rest>")
    if "--" in name or name.startswith("-") or name.endswith("-") or "-/" in name or "/-" in name:
        problems.append("no double, leading or trailing hyphens")
    if problems:
        return problems, warnings, None

    user, rest = name.split("/", 1)
    if not SEGMENT.fullmatch(user):
        return [f"username '{user}' must be lowercase letters, digits and single hyphens"], warnings, None
    if user in PROTECTED:
        return [f"username segment cannot be '{user}'"], warnings, None
    if expect_user is not None and user != normalize_user(expect_user):
        problems.append(f"username must be your own: expected '{normalize_user(expect_user)}', found '{user}'")

    parts, pos = {"user": user, "team": cfg["teams"][0]}, 0
    multi = len(cfg["teams"]) > 1
    steps = [("prefix", rf"{re.escape(cfg['prefix'])}-", f"after '{user}/' start with '{cfg['prefix']}-'")]
    if multi:
        steps += [("team-marker", r"team-", f"after '{cfg['prefix']}-' add 'team-<team>'"),
                  ("team", rf"({'|'.join(map(re.escape, cfg['teams']))})-", f"team must be one of: {', '.join(cfg['teams'])}")]
    steps += [("sprint", r"sprint-(\d{2})-", "sprint must be 'sprint-' plus two digits (sprint-01)"),
              ("type", rf"({'|'.join(map(re.escape, cfg['types']))})-", f"type must be one of: {', '.join(cfg['types'])}")]
    if cfg["requireIssueNumber"]:
        steps.append(("issue", r"(\d+)-", "an issue number is required after the type (e.g. feat-955-...)"))
    for label, pattern, hint in steps:
        m = re.compile(pattern).match(rest, pos)
        if not m:
            problems.append(f"{label}: {hint}")
            return problems, warnings, None
        parts[label] = m.group(1) if m.groups() else m.group(0)
        pos = m.end()
    parts.pop("team-marker", None)
    if not cfg["requireIssueNumber"]:
        m = re.compile(r"(\d+)-(?=[a-z])").match(rest, pos)
        if m:
            parts["issue"], pos = m.group(1), m.end()
    short = rest[pos:]
    if not SEGMENT.fullmatch(short):
        problems.append("short-name: add a short kebab-case description of the work (e.g. employee-id-filter)")
        return problems, warnings, None
    parts["name"] = short
    if int(parts["sprint"]) < 1:
        problems.append("sprint number must be 01 or higher")
    if len(short.split("-")) > 6:
        warnings.append("short-name has more than 6 words; keep it short")
    active = cfg.get("activeTeam")
    if multi and active and parts["team"] != active:
        warnings.append(f"branch is for team {parts['team']} but the active team is {active}; confirm the user authorized it")
    return problems, warnings, (None if problems else parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?")
    ap.add_argument("--expect-user")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    name = args.name
    if not name:
        try:
            name = subprocess.check_output(["git", "branch", "--show-current"], text=True, cwd=ROOT).strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"error: cannot read current branch: {exc}", file=sys.stderr)
            return 2
    problems, warnings, parts = validate(name, expect_user=args.expect_user)
    if args.json:
        print(json.dumps({"branch": name, "valid": not problems, "parts": parts, "problems": problems, "warnings": warnings}))
    elif problems:
        print(f"INVALID: '{name}'\n- " + "\n- ".join(problems) + f"\nFormat: {example(load_config())}")
    else:
        print(f"OK: {name}\n  " + (f"team {parts['team']} | " if len(load_config()["teams"]) > 1 else "") + f"sprint {parts['sprint']} | {parts['type']}"
              + (f" | issue #{parts['issue']}" if parts.get("issue") else "") + f" | {parts['name']}")
    if not args.json:
        for w in warnings:
            print(f"WARN: {w}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
