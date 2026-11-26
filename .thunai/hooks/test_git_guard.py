#!/usr/bin/env python3
"""Self-test for git_guard.evaluate. Run: python .thunai/hooks/test_git_guard.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from git_guard import evaluate  # noqa: E402

F = "jdoe/acme-sprint-01-feat-955-example-feature"  # feature branch
_tmp = Path(tempfile.mkdtemp())
GOOD = _tmp / "good.md"
GOOD.write_text("## Related Issue\nCloses #955\nRefs #970\n", encoding="utf-8")
BAD = _tmp / "bad.md"
BAD.write_text("## Related Issue\nNone\n", encoding="utf-8")

CASES = [
    # (command, branch, expected decision)
    ("git add .", F, "deny"), ("git add -A", F, "deny"), ("git add --all", F, "deny"),
    ("git add -Av", F, "deny"), ("cd x && git add .", F, "deny"),
    ("git push --force", F, "deny"), ("git push -f origin x", F, "deny"),
    ("git push --force-with-lease", F, "deny"), ("git push origin main", F, "deny"),
    ("git push origin HEAD:main", F, "deny"), ("git push origin +x:refs/heads/main", F, "deny"),
    ("git commit -m x", "main", "deny"), ("git push", "master", "deny"),
    ("git commit --no-verify -m x", F, "deny"),
    # writes that must ask
    ("git add src/a.py", F, "ask"), ("git commit -m x", F, "ask"), ("git push -u origin " + F, F, "ask"),
    ("git merge main", F, "ask"), ("git rebase main", F, "ask"), ("git reset --hard HEAD~1", F, "ask"),
    ("git checkout -b x/1-y", F, "ask"), ("git switch main", F, "ask"), ("git restore a.py", F, "ask"),
    ("git stash", F, "ask"), ("git stash pop", F, "ask"), ("git tag v1", F, "ask"),
    ("git branch -D old", F, "ask"), ("git branch new-one", F, "ask"), ("git pull", F, "ask"),
    ("git cherry-pick abc", F, "ask"), ("git revert abc", F, "ask"), ("git clean -fd", F, "ask"),
    ("git rm a.py", F, "ask"), ("git mv a b", F, "ask"), ("git remote add o url", F, "ask"),
    ("git config user.name x", F, "ask"),
    ("gh pr create --title x --body-file " + str(GOOD), F, "ask"),
    ("gh pr create --title x --body 'Closes #12'", F, "ask"),
    ("gh pr create --base main --head x -F " + str(GOOD), F, "ask"),
    ("gh pr create --title x --body-file " + str(BAD), F, "deny"),
    ("gh pr create --title x --body 'no issue here'", F, "deny"),
    ("gh pr create --title x --fill", F, "deny"),
    ("gh pr create --title x", F, "deny"),
    ("gh pr create --web", F, "deny"),
    ("gh pr create --title x --body-file " + str(_tmp / "missing.md"), F, "deny"),
("gh pr merge 5", F, "ask"), ("gh pr comment 5 -b x", F, "ask"),
    ("gh issue create --title x", F, "ask"), ("gh issue edit 3", F, "ask"), ("gh issue close 3", F, "ask"),
    ("gh issue comment 3 --body x", F, "ask"), ("gh api -X POST repos/o/r/issues", F, "ask"),
    ("gh api repos/o/r/issues -f title=x", F, "ask"), ("gh release create v1", F, "ask"),
    ("gh repo delete o/r", F, "ask"), ("gh workflow run ci.yml", F, "ask"),
    ("git status && git commit -m x", F, "ask"),
    # reads that must pass silently
    ("git status", "main", None), ("git diff main...HEAD", F, None), ("git log --oneline -5", F, None),
    ("git show HEAD", F, None), ("git branch --show-current", F, None), ("git branch -a", F, None),
    ("git branch", F, None), ("git stash list", F, None), ("git tag", F, None), ("git tag -l", F, None),
    ("git fetch origin", F, None), ("git rev-parse HEAD", F, None), ("git remote -v", F, None),
    ("git config --get user.name", F, None), ("git ls-files", F, None),
    ("gh auth status", F, None), ("gh issue list --assignee @me", F, None), ("gh issue view 3", F, None),
    ("gh pr list", F, None), ("gh pr view 5", F, None), ("gh pr diff 5", F, None),
    ("gh api user --jq .login", F, None), ("gh api repos/o/r/milestones", F, None),
    ("python .thunai/scripts/orient_snapshot.py", F, None), ("pytest -q", "main", None), ("ls -la", F, None),
    ("echo 'git add .'", F, None),
]
fails = 0
for cmd, br, want in CASES:
    got, why = evaluate(cmd, br)
    if got != want:
        print(f"FAIL: {cmd!r} on {br}: expected {want}, got {got} ({why})")
        fails += 1
print(f"{len(CASES) - fails}/{len(CASES)} passed")
sys.exit(1 if fails else 0)
