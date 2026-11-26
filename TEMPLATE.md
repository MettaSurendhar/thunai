# Manual setup checklist

Same result as `python init.py`, done by hand. Run commands from the repo root.

## 1. Name the project
- [ ] Replace `{{PROJECT_NAME}}` in `AGENTS.md` (title and persona line), `.thunai/src/agents/thunai.md` (description) and `.thunai/config/project.config.json` (`project`).
- [ ] Replace `{{BRANCH_PREFIX}}` in `.thunai/src/rules/branch-naming.md` and in the config (`branch.prefix`). Use a short lowercase slug, for example `acme-shop`.

## 2. Teams and scope (`.thunai/config/project.config.json`)
- [ ] `teams`: one entry (default `core`) keeps branch names as `<user>/<prefix>-sprint-<NN>-<type>-<issue>-<name>`. Several entries add a `-team-<team>` segment.
- [ ] `activeTeam`: the team you work for (must be in `teams`).
- [ ] `scope` and `outOfScope`: what Thunai may touch and what it must not (list other teams' modules or paths).

## 3. Stack packs
- [ ] Pick packs from [packs/](./packs/README.md). For each: copy `packs/<pack>/skills/*` into `skills/`.
- [ ] Add the pack names to `packs` and the stack text to `stack` in the config.
- [ ] No pack for your stack? Copy the nearest one, rewrite the skills, or write a new pack.

## 4. Commands and docs
- [ ] `commands.install`, `build`, `test`, `lint`: exact commands. Thunai asks instead of guessing while they are empty.
- [ ] `docs.root` (default `docs`): where specs, architecture and sprint plans live. With several teams, each team has a folder under it (for example `docs/<team>` or `docs/team-<team>`); set `docs.teamFolder` if yours is named differently. `docs.shared` lists extra common paths.

## 5. Memory
- [ ] `.thunai/memory/who-owns-what.md`: replace the TBD row with real owners.
- [ ] `.thunai/memory/operating-rules.md`: starts empty; Thunai adds corrections here.

## 6. Generate and verify
- [ ] `python .thunai/sync.py` (writes `.github/`, `.claude/`, `.opencode/`, `CLAUDE.md`)
- [ ] `python .thunai/sync.py --check` prints `in sync`
- [ ] `python .thunai/hooks/test_git_guard.py` passes
- [ ] `python skills/git-workflow/scripts/validate_branch.py <a-branch-name>` accepts a correctly named branch

## 7. Tool setup
- Copilot: pick `*Thunai` (default set in `.vscode/settings.json`), run `/orient`.
- Claude Code: `claude`, then `/orient`.
- OpenCode: `opencode`, then `/orient`. (Create an `opencode.jsonc` if you use OpenCode; see `.thunai/README.md`.)

## 8. Housekeeping
- [ ] Delete `.thunai/tracking/EXAMPLE.md` if not wanted (other tracking files are git-ignored).
- [ ] Commit the generated files so teammates and CI get them; run `sync.py --check` in CI.
- [ ] Optional: delete `init.py`, `TEMPLATE.md` and unused `packs/` once set up.