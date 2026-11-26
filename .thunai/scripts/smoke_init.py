#!/usr/bin/env python3
"""Smoke test: copy the template to a temp dir, run init.py, and check the result.

Verifies that a fresh project gets no leftover placeholders, installs the chosen
pack skills, and that `sync.py --check` is clean afterwards. Standard library only.
Exit code 0 on success, 1 on failure.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc")
PLACEHOLDERS = ("{{PROJECT_NAME}}", "{{BRANCH_PREFIX}}")
EXPECTED_SKILLS = ("nextjs", "shadcn", "mapcn", "fastapi", "sqlalchemy-alembic")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def adopt_failures() -> list[str]:
    """adopt.py into a repo that already has a .gitignore and settings: merge, no clobber, in sync."""
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="thunai-adopt-") as tmp:
        kit = Path(tmp) / "kit"
        repo = Path(tmp) / "repo"
        shutil.copytree(ROOT, kit, ignore=IGNORE)
        (repo / ".vscode").mkdir(parents=True)
        (repo / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
        (repo / ".vscode" / "settings.json").write_text('{"editor.tabSize": 2}', encoding="utf-8")
        res = run(
            [sys.executable, "adopt.py", str(repo), "--non-interactive", "--name", "Adopt Test", "--packs", "web-nextjs"],
            kit,
        )
        if res.returncode != 0:
            return [f"adopt.py failed:\n{res.stdout}\n{res.stderr}"]
        gitignore = (repo / ".gitignore").read_text(encoding="utf-8")
        if "node_modules/" not in gitignore:
            failures.append("adopt.py clobbered the existing .gitignore")
        if ".thunai/tracking/*" not in gitignore:
            failures.append("adopt.py did not merge Thunai lines into .gitignore")
        if "editor.tabSize" not in (repo / ".vscode" / "settings.json").read_text(encoding="utf-8"):
            failures.append("adopt.py clobbered the existing .vscode/settings.json")
        if not (repo / "skills" / "nextjs" / "SKILL.md").is_file():
            failures.append("adopt.py: pack skill not installed")
        for leftover in ("init.py", "packs", "LICENSE", ".thunai/docs"):
            if (repo / leftover).exists():
                failures.append(f"adopt.py left template-only path: {leftover}")
        check = run([sys.executable, ".thunai/sync.py", "--check"], repo)
        if check.returncode != 0:
            failures.append(f"sync --check failed after adopt:\n{check.stdout}\n{check.stderr}")
    return failures


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="thunai-smoke-") as tmp:
        work = Path(tmp) / "project"
        shutil.copytree(ROOT, work, ignore=IGNORE)

        init = run(
            [sys.executable, "init.py", "--non-interactive", "--name", "Smoke Test",
             "--packs", "web-nextjs,api-fastapi", "--teams", "alpha,beta", "--active-team", "alpha"],
            work,
        )
        if init.returncode != 0:
            failures.append(f"init.py failed:\n{init.stdout}\n{init.stderr}")
        else:
            for skill in EXPECTED_SKILLS:
                if not (work / "skills" / skill / "SKILL.md").is_file():
                    failures.append(f"pack skill not installed: {skill}")

            for path in work.rglob("*"):
                if path.is_file() and path.suffix in {".md", ".json", ".jsonc"}:
                    try:
                        text = path.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        continue
                    # THIRD_PARTY/README docs may mention the tokens when explaining init
                    if path.name in {"README.md", "TEMPLATE.md", "CONTRIBUTING.md"}:
                        continue
                    for token in PLACEHOLDERS:
                        if token in text:
                            failures.append(f"leftover {token} in {path.relative_to(work)}")

            check = run([sys.executable, ".thunai/sync.py", "--check"], work)
            if check.returncode != 0:
                failures.append(f"sync --check failed after init:\n{check.stdout}\n{check.stderr}")

    failures += adopt_failures()

    if failures:
        print("smoke_init: FAILED")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("smoke_init: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
