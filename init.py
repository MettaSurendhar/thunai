#!/usr/bin/env python3
"""Bootstrap this template for a project.

Usage:
  python init.py                       interactive
  python init.py --non-interactive --name "Acme Shop" --packs web-nextjs,api-fastapi
  python init.py --list-packs

What it does (all local, no git or network):
  1. replaces {{PROJECT_NAME}} and {{BRANCH_PREFIX}} in AGENTS.md, .thunai/src and .thunai/config
  2. writes name, teams, packs and stack into .thunai/config/project.config.json
  3. copies packs/<pack>/skills/* into skills/
  4. runs `python .thunai/sync.py` to generate the Copilot, Claude Code and OpenCode files

Each step is safe to re-run except the name: placeholders are consumed on first use, so to rename
the project later, edit the places listed in .thunai/README.md.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / ".thunai" / "config" / "project.config.json"
PACKS = ROOT / "packs"
SKILLS = ROOT / "skills"
PLACEHOLDER_FILES = [ROOT / "AGENTS.md", ROOT / ".thunai" / "src", ROOT / ".thunai" / "config"]
TEXT_SUFFIXES = {".md", ".json", ".jsonc", ".py", ".txt"}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_packs():
    packs = {}
    for manifest in sorted(PACKS.glob("*/pack.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["_dir"] = manifest.parent
        packs[data["name"]] = data
    return packs


def ask(prompt, default=""):
    suffix = f" [{default}]" if default else ""
    answer = input(f"{prompt}{suffix}: ").strip()
    return answer or default


def split_csv(value):
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def iter_text_files():
    for entry in PLACEHOLDER_FILES:
        files = [entry] if entry.is_file() else sorted(entry.rglob("*"))
        for f in files:
            if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES:
                yield f


def substitute(values):
    """Replace placeholders; return the number of files changed."""
    changed = 0
    for f in iter_text_files():
        text = f.read_text(encoding="utf-8")
        new = text
        for key, val in values.items():
            new = new.replace("{{" + key + "}}", val)
        if new != text:
            f.write_text(new, encoding="utf-8", newline="")
            changed += 1
    return changed


def remaining_placeholders():
    rx = re.compile(r"\{\{(PROJECT_NAME|BRANCH_PREFIX)\}\}")
    return [f for f in iter_text_files() if rx.search(f.read_text(encoding="utf-8"))]


def update_config(name, prefix, teams, active, chosen, packs):
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if name:
        cfg["project"] = name
    if prefix:
        cfg["branch"]["prefix"] = prefix
    cfg["teams"] = teams
    cfg["activeTeam"] = active
    if len(teams) > 1:
        cfg["outOfScope"] = [f"{t} modules" for t in teams if t != active]
        cfg["scope"] = f"{active} modules"
    cfg["packs"] = sorted(set(cfg.get("packs") or []) | set(chosen))
    stack = cfg.get("stack") or {}
    for pack_name in chosen:
        pack = packs[pack_name]
        area = next((a for a in ("frontend", "backend") if a in pack.get("routing", {})), pack_name)
        stack[area] = pack["stack"]
    cfg["stack"] = stack
    CONFIG.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8", newline="")


def install_packs(chosen, packs, force):
    for pack_name in chosen:
        for skill in packs[pack_name]["skills"]:
            src = packs[pack_name]["_dir"] / "skills" / skill
            dst = SKILLS / skill
            if not src.is_dir():
                print(f"  ! {pack_name}: skill folder missing: {src}")
                continue
            if dst.exists():
                if not force:
                    print(f"  = {skill} already installed (use --force to overwrite)")
                    continue
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
            print(f"  + {skill}  ({pack_name})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", help="project name, e.g. 'Acme Shop'")
    ap.add_argument("--prefix", help="branch prefix (default: slug of the name)")
    ap.add_argument("--packs", help="comma-separated pack names, or 'none'")
    ap.add_argument("--teams", help="comma-separated team names (default: core)")
    ap.add_argument("--active-team", help="your team (default: first team)")
    ap.add_argument("--non-interactive", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite already installed pack skills")
    ap.add_argument("--no-sync", action="store_true", help="skip running .thunai/sync.py")
    ap.add_argument("--list-packs", action="store_true")
    args = ap.parse_args()

    packs = load_packs()
    if args.list_packs:
        for p in packs.values():
            print(f"{p['name']}: {p['description']}\n    skills: {', '.join(p['skills'])}")
        return 0

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    has_placeholders = bool(remaining_placeholders())
    interactive = not args.non_interactive

    name = args.name
    if interactive and not name and has_placeholders:
        name = ask("Project name", "My Project")
    if has_placeholders and not name:
        print("error: --name is required (placeholders are still present)", file=sys.stderr)
        return 2
    prefix = args.prefix or (slug(name) if name else None)
    if interactive and not args.prefix and has_placeholders:
        prefix = ask("Branch prefix", prefix)

    teams_arg = args.teams
    if interactive and teams_arg is None:
        teams_arg = ask("Teams, comma-separated (one team = no team segment in branch names)", ",".join(cfg.get("teams") or ["core"]))
    teams = [slug(t) for t in split_csv(teams_arg)] or cfg.get("teams") or ["core"]
    active = slug(args.active_team) if args.active_team else None
    if interactive and not active and len(teams) > 1:
        active = ask("Your team", teams[0])
    active = active or teams[0]
    if active not in teams:
        print(f"error: active team '{active}' is not in {teams}", file=sys.stderr)
        return 2

    if args.packs is not None:
        chosen = [] if args.packs.strip().lower() == "none" else split_csv(args.packs)
    elif interactive:
        print("Available packs:")
        for p in packs.values():
            print(f"  {p['name']}: {p['description']}")
        chosen = split_csv(ask("Packs to install, comma-separated (blank = none)", ""))
    else:
        chosen = []
    unknown = [c for c in chosen if c not in packs]
    if unknown:
        print(f"error: unknown pack(s): {', '.join(unknown)}. Use --list-packs.", file=sys.stderr)
        return 2

    if has_placeholders:
        n = substitute({"PROJECT_NAME": name, "BRANCH_PREFIX": prefix})
        print(f"Replaced placeholders in {n} file(s).")
    else:
        print("No placeholders left; keeping the existing project name and prefix.")
    update_config(name if has_placeholders else None, prefix if has_placeholders else None, teams, active, chosen, packs)
    print(f"Config updated: teams={teams}, activeTeam={active}, packs={chosen or 'none'}")
    if chosen:
        print("Installing packs:")
        install_packs(chosen, packs, args.force)

    if not args.no_sync:
        res = subprocess.run([sys.executable, str(ROOT / ".thunai" / "sync.py")], cwd=ROOT)
        if res.returncode != 0:
            print("sync.py failed; fix the error above and re-run it.", file=sys.stderr)
            return res.returncode

    print("\nNext: fill commands.* and docs.* in .thunai/config/project.config.json and the table in")
    print(".thunai/memory/who-owns-what.md, then open your AI tool and run /orient.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
