---
description: "MANDATORY for every agent. Branch naming convention for {{PROJECT_NAME}}: username, optional team, sprint, type, issue number, short name."
applyTo: "**"
---

# Branch Naming

## Format
```text
<username>/<prefix>[-team-<team>]-sprint-<NN>-<type>-<issue>-<short-name>
```
The `-team-<team>` segment is present **only** when `teams` in `.thunai/config/project.config.json` lists more than one team.

Examples (prefix `{{BRANCH_PREFIX}}`):
- single team: `jdoe/{{BRANCH_PREFIX}}-sprint-01-feat-123-login-form`
- multiple teams: `jdoe/{{BRANCH_PREFIX}}-team-web-sprint-01-feat-123-login-form`

| Segment | Rule | Where it comes from |
|---|---|---|
| `<username>` | The user's own GitHub login, lowercase; `_` becomes `-` | `gh api user --jq .login` |
| `<prefix>` | Fixed project prefix | `branch.prefix` in `project.config.json` |
| `team-<team>` | Multi-team projects only; a configured team, lowercase kebab-case | The issue's team; `activeTeam` in `project.config.json` unless the user says otherwise |
| `sprint-<NN>` | Two digits, `01` or higher | The sprint the issue is planned in, from `/orient` (team sprint docs or milestone). If not found, ask. Never guess |
| `<type>` | One of `branch.types` (default `feat`, `bug`, `enh`, `task`, `docs`, `hotfix`) | The issue Type: Feature=`feat`, Bug=`bug`, Enhancement=`enh`, Task=`task`, Documentation=`docs`. `hotfix` is for urgent production fixes and still needs an issue |
| `<issue>` | The issue number, digits only | The assigned issue. Required, so the PR can link its issue |
| `<short-name>` | 2 to 5 kebab-case words describing the work | The issue title, shortened |

## Conventions
- Lowercase letters, digits and hyphens only. No spaces, underscores, dots or uppercase.
- Exactly one `/` (after the username). No leading, trailing or double hyphens.
- At most `branch.maxLength` characters (default 100). Keep the short name short and meaningful.
- One branch per issue. Do not reuse the name of a merged branch.
- Never name a branch `main`, `master`, `develop` or `release`, and never use those as the username segment.
- Create it from an up-to-date `baseBranch` (see git-governance). Creating the branch is a git write: ask first.
- In a multi-team project, a branch for a team other than `activeTeam` is out of scope unless the user explicitly authorizes it.
- Delete a merged branch only when the user asks.

## Valid and invalid (single-team, prefix `{{BRANCH_PREFIX}}`)
| Branch | Verdict |
|---|---|
| `jdoe/{{BRANCH_PREFIX}}-sprint-01-feat-123-login-form` | valid |
| `jdoe/{{BRANCH_PREFIX}}-sprint-12-bug-1042-duplicate-records` | valid |
| `jdoe/123-login-form` | invalid: no prefix or sprint |
| `jdoe/{{BRANCH_PREFIX}}-sprint-1-feat-123-x` | invalid: sprint needs two digits |
| `jdoe/{{BRANCH_PREFIX}}-sprint-01-feature-123-x` | invalid: unknown type |
| `jdoe/{{BRANCH_PREFIX}}-sprint-01-feat-login-form` | invalid: no issue number |
| `JDoe/{{BRANCH_PREFIX}}-sprint-01-feat-123-login_form` | invalid: uppercase and underscore |

Validate every proposed name before creating it: `python skills/git-workflow/scripts/validate_branch.py <name> --expect-user <login>`. Settings (prefix, types, max length, issue requirement) live under `branch` in `.thunai/config/project.config.json`; teams live at the top level.