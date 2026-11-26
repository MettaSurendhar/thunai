# Contributing to Thunai

Thanks for helping. Thunai is a stack-agnostic template of agents, skills and rules for AI coding assistants. Contributions that make it clearer, safer or more portable are welcome.

By participating you agree to the [Code of Conduct](./CODE_OF_CONDUCT.md). Contributions are licensed under the [MIT licence](./LICENSE).

## Where things live

| Path | What it is | Edit by hand? |
|---|---|---|
| `.thunai/src/` | **Source of truth**: agents, commands, rules | Yes |
| `skills/` | Canonical skills (`<name>/SKILL.md`) | Yes |
| `packs/<pack>/` | Opt-in stack packs (`pack.json` plus `skills/`) | Yes |
| `AGENTS.md`, `.thunai/memory/`, `.thunai/config/` | Project guidance and config | Yes |
| `.claude/`, `.github/agents`, `.github/instructions`, `.github/prompts`, `.github/skills`, `.opencode/`, `CLAUDE.md`, `.github/copilot-instructions.md` | **Generated** runtime files | **No** |

Never edit generated files. Change the source and regenerate:

```powershell
python .thunai/sync.py          # regenerate
python .thunai/sync.py --check  # fail if anything is out of date (CI runs this)
```

## Setup

You need Python 3.10 or newer. There are no third-party dependencies.

```powershell
git clone https://github.com/MettaSurendhar/thunai.git
cd thunai
python .thunai/sync.py --check
python .thunai/hooks/test_git_guard.py
```

## Before you open a pull request

1. Open or find an issue first for anything larger than a typo.
2. Branch from `main`. Use a short descriptive name such as `feat/pack-django`.
3. Make the change in the **source** locations above.
4. Run `python .thunai/sync.py` and commit the regenerated output with your change.
5. Run the checks and report their real results in the PR:
   - `python .thunai/sync.py --check`
   - `python .thunai/hooks/test_git_guard.py`
   - `python .thunai/scripts/validate_template.py` (skill and pack validation)
6. Update docs that describe what you changed (`README.md`, `TEMPLATE.md`, `.thunai/README.md`, `packs/README.md`) and add a line under `Unreleased` in [CHANGELOG.md](./CHANGELOG.md).

## Conventions

- **Stack-agnostic core.** Anything specific to a framework belongs in a pack, not in `skills/` or `.thunai/src/`.
- **Skill format.** Folder name equals the `name` in the `SKILL.md` frontmatter. Include a `description` with trigger phrases. Keep skills focused and short.
- **No placeholders left behind.** Use only `{{PROJECT_NAME}}` and `{{BRANCH_PREFIX}}`; `init.py` replaces them.
- **Never include secrets, personal email addresses, or employer-specific names or data.** See [SECURITY.md](./SECURITY.md).
- **Honest verification.** Do not claim a check passed unless you ran it. This applies to PR descriptions too.
- **Line endings.** `skills/` is kept as LF so the recorded hashes hold (see `.gitattributes`).

## Adding a pack

Follow [.thunai/docs/adding-a-pack.md](./.thunai/docs/adding-a-pack.md).

## Adding or updating third-party material

Only add content whose licence allows redistribution. Record it in [THIRD_PARTY.md](./THIRD_PARTY.md) with the upstream URL, licence, copyright holder and relationship (copied, adapted, original). Copied files stay unmodified, or the modification is documented.

## Reporting bugs and requesting features

Use the issue templates. For security problems, follow [SECURITY.md](./SECURITY.md) and do not open a public issue.
