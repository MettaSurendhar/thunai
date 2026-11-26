---
description: "MANDATORY for every agent. Work only on the assigned issue and paths; modules listed in outOfScope are off limits."
applyTo: "**"
---

# Scope and Boundaries

- Work only on the issue and paths the user explicitly provided.
- Read the project `AGENTS.md`, the relevant specification and architecture documents from the team docs folder (`docs.root` and `docs.teamFolder` in `.thunai/config/project.config.json`, or the folder named after `activeTeam`), and the issue before acting.
- Do not read another team's docs folder unless the user explicitly authorizes it. This only applies when `teams` lists more than one team.
- Teams, modules or paths listed in `outOfScope` are out of scope unless the user explicitly authorizes otherwise.
- Out-of-scope findings (bugs, smells, refactors) are reported to the user, not fixed.
- If the issue or the paths are missing or ambiguous, ask. Do not infer.