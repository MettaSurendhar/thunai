#!/usr/bin/env python3
"""Read-only fact gatherer for Thunai's /orient. Prints JSON. Never writes anything.

Usage: python .thunai/scripts/orient_snapshot.py [--name NAME ...]
  --name  extra name to look for in the docs (for example the user's first name); repeatable.

It collects git state (with the branch name parsed), GitHub login, assigned issues, milestones,
and an inventory of the active team's documents (docs.root; with several teams, the matching team folder). Everything it cannot
determine is listed under "not_found" with the reason.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TEXT_EXT = {".md", ".markdown", ".txt", ".rst", ".adoc", ".csv", ".json", ".yml", ".yaml", ".html"}
BINARY_EXT = {".docx", ".doc", ".pdf", ".pptx", ".ppt", ".xlsx", ".xls", ".vsdx"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
CATEGORIES = [  # first match on the path below the docs folder wins
    ("sprints", re.compile(r"sprint|iteration", re.I)),
    ("architecture", re.compile(r"architect|(?<![a-z])adr(?![a-z])|(?<![a-z])[hl]ld(?![a-z])|design|diagram", re.I)),
    ("specifications", re.compile(r"spec|requirement|(?<![a-z])(srs|brd|prd)(?![a-z])|user[\s_-]*stor|acceptance", re.I)),
    ("project_plan", re.compile(r"plan|roadmap|milestone|schedule|timeline|backlog", re.I)),
]
SHARED_DIR = re.compile(r"^(shared|common|general|project)$", re.I)
SPRINT_NO = re.compile(r"sprint[\s_-]*0*(\d+)", re.I)
SPRINT_LINE = re.compile(r"\b(start|end|goal|duration|dates?|period)\b", re.I)
MAX_FILES, MAX_HITS, MAX_HITS_PER_FILE = 500, 40, 6


def load_branch_validator():
    path = ROOT / "skills" / "git-workflow" / "scripts" / "validate_branch.py"
    try:
        spec = importlib.util.spec_from_file_location("validate_branch", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:  # noqa: BLE001 - the validator is optional for orient
        return None


def run(cmd, timeout=25):
    """Return (ok, stdout_or_error). Never raises."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
    except FileNotFoundError:
        return False, f"{cmd[0]} is not installed or not on PATH"
    except subprocess.TimeoutExpired:
        return False, f"{' '.join(cmd[:3])} timed out"
    if p.returncode != 0:
        msg = (p.stderr or p.stdout).strip().splitlines()
        return False, msg[-1] if msg else "command failed"
    return True, p.stdout.strip()


def load_config(not_found):
    try:
        return json.loads((ROOT / ".thunai" / "config" / "project.config.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        not_found.append(f"project.config.json unreadable: {exc}")
        return {}


# ---- docs -------------------------------------------------------------------------------
def norm(name):
    """Lowercase alphanumerics only, so 'Team-B', 'team_b' and 'TeamB' compare equal."""
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def team_names(team):
    """Folder names (normalised) that belong to a team: 'b' or 'teamb'."""
    n = norm(team)
    return {n, "team" + n} if n else set()


def teams_of(config):
    teams = config.get("teams") or ["core"]
    active = config.get("activeTeam") or teams[0]
    return teams, active


def walk_files(base):
    files = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            if not fn.startswith("."):
                files.append(Path(dirpath) / fn)
        if len(files) >= MAX_FILES:
            break
    return files[:MAX_FILES]


def categorize(rel_inside):
    for name, rx in CATEGORIES:
        if rx.search(rel_inside):
            return name
    return "other"


def read_lines(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []


def sprint_summary(lines):
    title = next((ln.lstrip("# ").strip() for ln in lines if ln.strip()), "")
    picked = [ln.strip()[:160] for ln in lines if SPRINT_LINE.search(ln)][:3]
    return ([title[:120]] if title else []) + picked


def scan_docs(config, needles, not_found):
    cfg = config.get("docs") or {}
    root = ROOT / (cfg.get("root") or "docs")
    out = {"root": root.relative_to(ROOT).as_posix(), "root_exists": root.is_dir(), "team_folder": None,
           "other_team_folders_not_read": [], "other_folders_not_read": [], "inventory": {}, "latest_sprint_found": None, "hits": []}
    if not root.is_dir():
        not_found.append(f"docs: folder '{out['root']}' does not exist (set docs.root in project.config.json)")
        return out
    teams, active = teams_of(config)
    mine = team_names(active)
    others = set().union(*(team_names(x) for x in teams if norm(x) != norm(active))) if len(teams) > 1 else set()
    team_dir, shared_dirs = None, []
    single = len(teams) <= 1 and not cfg.get("teamFolder")
    if single:
        team_dir = root  # one team: the whole docs root is the team scope
    if cfg.get("teamFolder"):
        cand = ROOT / cfg["teamFolder"]
        team_dir = cand if cand.is_dir() else None
        if not team_dir:
            not_found.append(f"docs: configured docs.teamFolder '{cfg['teamFolder']}' does not exist")
    for d in sorted(p for p in root.iterdir() if p.is_dir() and not single):
        if team_dir and d == team_dir:
            continue
        if not team_dir and norm(d.name) in mine:
            team_dir = d
        elif norm(d.name) in others:
            out["other_team_folders_not_read"].append(d.relative_to(ROOT).as_posix())
        elif SHARED_DIR.match(d.name):
            shared_dirs.append(d)
        else:
            out["other_folders_not_read"].append(d.relative_to(ROOT).as_posix())
    if not team_dir:
        if not cfg.get("teamFolder"):
            not_found.append(f"docs: no folder for team '{active}' under '{out['root']}/' "
                             f"(looked for '{active}' or 'team-{active}' in any casing; or set docs.teamFolder)")
    else:
        out["team_folder"] = team_dir.relative_to(ROOT).as_posix()

    # (path, scope, base used to categorize)
    sources = []
    if team_dir:
        sources += [(f, "team", team_dir) for f in walk_files(team_dir)]
    if team_dir != root:
        sources += [(f, "shared", root) for f in sorted(root.iterdir()) if f.is_file() and not f.name.startswith(".")]
    for d in shared_dirs:
        sources += [(f, "shared", d) for f in walk_files(d)]
    for extra in cfg.get("shared") or []:
        p = ROOT / extra
        if p.is_file():
            sources.append((p, "shared", p.parent))
        elif p.is_dir():
            sources += [(f, "shared", p) for f in walk_files(p)]
        else:
            not_found.append(f"docs: configured shared path '{extra}' does not exist")

    inventory = {k: [] for k, _ in CATEGORIES} | {"other": []}
    needle_rx = [re.compile(n, re.I) for n in needles]
    sprints = []
    for f, scope, base in sources:
        ext = f.suffix.lower()
        if ext not in TEXT_EXT and ext not in BINARY_EXT:
            continue
        rel_inside = f.relative_to(base).as_posix()
        cat = categorize(rel_inside)
        entry = {"path": f.relative_to(ROOT).as_posix(), "scope": scope, "readable_by_script": ext in TEXT_EXT}
        if not entry["readable_by_script"]:
            entry["note"] = "binary format: open it with the matching pdf/docx/pptx/xlsx skill or tool"
        m = SPRINT_NO.search(rel_inside)
        if m:
            entry["sprint"] = int(m.group(1))
            sprints.append(int(m.group(1)))
        lines = read_lines(f) if ext in TEXT_EXT else []
        if cat == "sprints" and lines:
            entry["summary"] = sprint_summary(lines)
        inventory[cat].append(entry)
        if lines and needle_rx and len(out["hits"]) < MAX_HITS:
            per_file = 0
            for i, line in enumerate(lines, 1):
                if any(rx.search(line) for rx in needle_rx):
                    out["hits"].append(f"{entry['path']}:{i}: {line.strip()[:200]}")
                    per_file += 1
                    if per_file >= MAX_HITS_PER_FILE or len(out["hits"]) >= MAX_HITS:
                        break
    out["inventory"] = {k: v for k, v in inventory.items()}
    out["latest_sprint_found"] = max(sprints) if sprints else None
    if team_dir:
        for key, label in (("sprints", "sprint"), ("architecture", "architecture"),
                           ("specifications", "specification"), ("project_plan", "project plan")):
            if not any(e["scope"] == "team" for e in inventory[key]):
                not_found.append(f"docs: no {label} documents found in '{out['team_folder']}'")
    if needles and not out["hits"] and (team_dir or sources):
        not_found.append("docs: no line in the docs mentions your assigned issues, your login or the names given")
    return out


# ---- main -------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", action="append", default=[])
    args = ap.parse_args()

    not_found = []
    config = load_config(not_found)
    snap = {"git": {}, "github": {}, "assigned_issues": None, "milestones": None,
            "docs": {}, "config": {}, "memory": {}, "not_found": not_found}

    # ---- git
    ok, branch = run(["git", "branch", "--show-current"])
    if ok:
        snap["git"]["branch"] = branch or "(detached HEAD)"
        validator = load_branch_validator()
        if validator and branch:
            problems, warnings, parts = validator.validate(branch)
            snap["git"].update({"branch_valid": not problems, "branch_parts": parts,
                                "branch_problems": problems, "branch_warnings": warnings})
        ok2, status = run(["git", "status", "--short"])
        snap["git"]["changed_files"] = status.splitlines() if ok2 and status else []
        ok3, log = run(["git", "log", "--oneline", "-5"])
        snap["git"]["recent_commits"] = log.splitlines() if ok3 else []
    else:
        not_found.append(f"git: {branch}")

    # ---- GitHub
    login = None
    ok, out = run(["gh", "auth", "status"])
    snap["github"]["authenticated"] = ok
    if not ok:
        not_found.append(f"github: not authenticated or gh missing ({out}); ask the user to run 'gh auth login'")
    else:
        ok, login = run(["gh", "api", "user", "--jq", ".login"])
        snap["github"]["login"] = login if ok else None
        ok, repo = run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])
        snap["github"]["repo"] = repo if ok else None
        if not ok:
            not_found.append(f"github repo: {repo}")
        ok, out = run(["gh", "issue", "list", "--assignee", "@me", "--state", "open", "--limit", "50",
                       "--json", "number,title,milestone,labels,url"])
        if ok:
            issues = json.loads(out or "[]")
            snap["assigned_issues"] = [{
                "number": i["number"], "title": i["title"], "url": i["url"],
                "milestone": (i.get("milestone") or {}).get("title"),
                "milestone_due": (i.get("milestone") or {}).get("dueOn"),
                "labels": [lb["name"] for lb in i.get("labels", [])],
            } for i in issues]
            if not issues:
                not_found.append("assigned issues: none open and assigned to you on GitHub")
        else:
            not_found.append(f"assigned issues: {out}")
        ok, out = run(["gh", "api", "repos/{owner}/{repo}/milestones?state=open&sort=due_on&direction=asc"])
        if ok:
            snap["milestones"] = [{
                "title": m["title"], "due_on": m.get("due_on"), "open_issues": m["open_issues"],
                "closed_issues": m["closed_issues"], "description": (m.get("description") or "")[:200],
            } for m in json.loads(out or "[]")]
            if not snap["milestones"]:
                not_found.append("milestones: the repository has no open GitHub milestones")
        else:
            not_found.append(f"milestones: {out}")

    # ---- docs (team folder), config, memory
    numbers = [i["number"] for i in (snap["assigned_issues"] or [])]
    needles = [rf"(?<![\w]){re.escape('#' + str(n))}\b" for n in numbers]
    needles += [re.escape(n) for n in ([login] if login else []) + args.name if n]
    snap["docs"] = scan_docs(config, needles, not_found)
    snap["config"] = {"project": config.get("project"), "teams": teams_of(config)[0],
                      "active_team": teams_of(config)[1], "packs": config.get("packs") or [],
                      "empty_commands": [k for k, v in (config.get("commands") or {}).items() if not v]}
    if teams_of(config)[1] not in teams_of(config)[0]:
        not_found.append("config.activeTeam: not listed in config.teams")
    for name in ("operating-rules.md", "operating-directives.md", "who-owns-what.md"):
        snap["memory"][name] = (ROOT / ".thunai" / "memory" / name).exists()

    json.dump(snap, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
