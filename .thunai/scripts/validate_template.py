#!/usr/bin/env python3
"""Validate the Thunai template itself (skills, packs, hygiene).

Checks:
  - every skill folder has SKILL.md whose frontmatter `name` equals the folder name
    and has a non-empty `description`
  - every pack has a valid pack.json: required fields, listed skills exist, no listed
    skill collides with a core skill, every skill folder is listed
  - no email addresses (other than noreply/example) and no obvious secret tokens in
    tracked text files

Exit code 0 when clean, 1 otherwise. Standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK_FIELDS = ("name", "description", "skills", "detect", "stack", "routing")
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
TEXT_SUFFIXES = {".md", ".json", ".jsonc", ".py", ".yml", ".yaml", ".txt", ".toml", ""}
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}\b")
ALLOWED_EMAIL_PARTS = ("noreply", "example.com", "example.org", "users.noreply.github.com")
SECRET_RES = (
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9]{32,}"),
)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def check_skill_dir(skills_dir: Path, errors: list[str]) -> list[str]:
    names: list[str] = []
    if not skills_dir.is_dir():
        return names
    for folder in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill = folder / "SKILL.md"
        rel = skill.relative_to(ROOT)
        if not skill.is_file():
            errors.append(f"{rel}: missing SKILL.md")
            continue
        meta = frontmatter(skill)
        if meta.get("name") != folder.name:
            errors.append(f"{rel}: frontmatter name {meta.get('name')!r} != folder {folder.name!r}")
        if not meta.get("description"):
            errors.append(f"{rel}: empty or missing description")
        names.append(folder.name)
    return names


def check_packs(core: set[str], errors: list[str]) -> None:
    packs_dir = ROOT / "packs"
    for pack in sorted(p for p in packs_dir.iterdir() if p.is_dir()):
        manifest = pack / "pack.json"
        rel = manifest.relative_to(ROOT)
        if not manifest.is_file():
            errors.append(f"{rel}: missing pack.json")
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON ({exc})")
            continue
        for field in PACK_FIELDS:
            if field not in data:
                errors.append(f"{rel}: missing field {field!r}")
        if data.get("name") != pack.name:
            errors.append(f"{rel}: name {data.get('name')!r} != folder {pack.name!r}")
        present = set(check_skill_dir(pack / "skills", errors))
        listed = set(data.get("skills", []))
        for name in sorted(listed - present):
            errors.append(f"{rel}: lists skill {name!r} with no folder")
        for name in sorted(present - listed):
            errors.append(f"{rel}: skill folder {name!r} not listed in pack.json")
        for name in sorted(listed & core):
            errors.append(f"{rel}: skill {name!r} collides with a core skill")
        for role, names in (data.get("routing") or {}).items():
            for name in names:
                if name not in listed:
                    errors.append(f"{rel}: routing.{role} references unknown skill {name!r}")


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def check_hygiene(errors: list[str]) -> None:
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(ROOT)
        for email in EMAIL_RE.findall(text):
            if not any(part in email.lower() for part in ALLOWED_EMAIL_PARTS):
                errors.append(f"{rel}: possible personal email {email!r}")
        for pattern in SECRET_RES:
            if pattern.search(text):
                errors.append(f"{rel}: possible secret matching {pattern.pattern!r}")


def main() -> int:
    errors: list[str] = []
    core = set(check_skill_dir(ROOT / "skills", errors))
    check_packs(core, errors)
    check_hygiene(errors)
    if errors:
        print(f"validate_template: {len(errors)} problem(s)")
        for line in errors:
            print(f"  - {line}")
        return 1
    print(f"validate_template: OK ({len(core)} core skills, packs valid, hygiene clean)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
