# Thunai Hook Registry

Guardrails that enforce rules mechanically instead of relying on the model.

## Policy
- **Deny (hard stop):** `git add .`/`-A`/`--all`, force-push, push to `main`/`master`, commit or push while on `main`/`master`, `--no-verify`, and `gh pr create` without a PR body that references an issue (`--fill`, `--web` and interactive PRs are denied because they skip that check).
- **Ask (user approves each time):** every other git or `gh` command that can change state (add, commit, push, merge, rebase, reset, checkout/switch, restore, rm, mv, stash, tag, cherry-pick, revert, clean, pull, `gh pr|issue` create/edit/comment/close/merge, non-GET `gh api`, and similar).
- **Allow:** read-only git/gh (status, diff, log, show, fetch, branch --show-current, gh auth status, issue/pr list and view) and the read-only `.thunai/scripts/orient_snapshot.py`.

## Per tool
| Tool | Mechanism | Strength |
|---|---|---|
| Claude Code | `PreToolUse` hook `.thunai/hooks/git_guard.py` (classifies every Bash command; deny = exit 2, ask = permission prompt) plus `permissions.allow/ask/deny` in `.claude/settings.json` | Strongest: includes the "not on main" branch check and compound commands (`a && git add .`) |
| OpenCode | `permission.bash` patterns in `opencode.jsonc` and each generated agent | Pattern-based. Deny/ask are enforced; the "not on main" check and the PR related-issue check are rule-based (`validate_doc.py`) only |
| Copilot | `chat.tools.terminal.autoApprove` set to `false` for git/gh writes in `.vscode/settings.json` | Forces an approval prompt in the terminal tool; no branch or PR-issue check (rule-based only) |

Test the Claude hook: `python .thunai/hooks/test_git_guard.py`.
