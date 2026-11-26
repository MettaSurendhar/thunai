---
name: git-workflow
description: Branch naming, issue and pull request preparation for Thunai, with templates and validators. Trigger on /pr, "create a branch", "name this branch", "draft the PR", "write the issue", "ready to commit".
---

# Git Workflow

**Purpose:** compliant branches, issues and PRs. The rules live in the git-governance, branch-naming and issue-and-pr instructions; this skill is the procedure. Every git or `gh` write below needs the user's approval first.

## 1. Issue
1. Verify GitHub CLI auth (see `orient`).
2. Find the issue, or draft one from [templates/issue-template.md](./templates/issue-template.md) (delete the four bug-only sections for non-bug issues) and ask before creating it.
3. Validate the draft: `python skills/git-workflow/scripts/validate_doc.py --kind issue <file>`.

## 2. Branch
Build the name from the branch-naming rule: `<username>/<prefix>[-team-<team>]-sprint-<NN>-<type>-<issue>-<short-name>`. The `-team-<team>` segment exists only when `teams` in `.thunai/config/project.config.json` lists more than one team.
1. `username`: `gh api user --jq .login`, lowercased (`_` becomes `-`).
2. `team` (multi-team projects only): the owning team from `teams`; `activeTeam` from `.thunai/config/project.config.json` unless the user says otherwise.
3. `sprint`: from `/orient` (team sprint docs or milestone). If it says "Not able to find", **ask the user**; never guess.
4. `type`: from the issue Type: Feature=`feat`, Bug=`bug`, Enhancement=`enh`, Task=`task`, Documentation=`docs`; urgent production fix=`hotfix`.
5. `issue` number and a 2 to 5 word kebab `short-name` from the issue title.
6. Validate: `python skills/git-workflow/scripts/validate_branch.py <name> --expect-user <login>`. Exit 0 required.
7. Show the exact `git checkout -b <name>` (from an up-to-date `main`) and wait for approval.

## 3. Commit
Inspect `git status` and `git diff`. Stage explicit paths only, never `.`, `-A` or `--all`. Ask before each of `git add` and `git commit`.

## 4. Pull request
1. Draft from [templates/pr-template.md](./templates/pr-template.md), saved under `.thunai/tracking/` (git-ignored).
2. **Related Issue is mandatory:** `Closes #<n>` (or `Refs #<n>` for issues that stay open), one line per issue, including the issue number from the branch name.
3. Validate: `python skills/git-workflow/scripts/validate_doc.py --kind pr <file> --branch <current-branch>`. Exit 0 required.
4. Ask the user to approve, then `gh pr create --base main --title "<t>" --body-file <file>`. Never `--fill`, `--web` or an interactive PR; the guard hook blocks them.
5. After the PR opens, ask before updating the issue with the PR URL. Commands: [references/gh-commands.md](./references/gh-commands.md).

## Quality gates
- Validators exit 0. The PR's Testing section lists real commands and real results.
- No personal email addresses or secrets in any draft.
