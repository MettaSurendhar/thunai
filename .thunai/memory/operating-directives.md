# Thunai Operating Directives

Standing instructions: routing rules, repo rules, artifact formats, preferences.

- Branch format: `<username>/<prefix>[-team-<team>]-sprint-<NN>-<type>-<issue>-<short-name>` (rule: branch-naming). The team segment exists only when `teams` lists more than one team.
- Issue and PR formats: templates in the `git-workflow` skill.
- Base branch: `baseBranch` in `.thunai/config/project.config.json` (default `main`). All changes go through a PR.
- Test and build commands live in `.thunai/config/project.config.json`.