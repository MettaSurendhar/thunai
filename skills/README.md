# Skills

This directory holds the **core** skills that every project gets. Optional stack skills live in `packs/<pack>/skills/` and are copied here by `python init.py --packs ...` (see `packs/README.md`).

It is also the single canonical project copy of two selected skills from the upstream `obra/superpowers` repository. OpenCode reads these files from the configured `./skills` source; Claude Code loads tiny `.claude/skills/` entry points that refer to the canonical files. Do not copy the full skill Markdown into runtime-specific directories. No symlinks or installer are required.

## Source and refresh

- Upstream: <https://github.com/obra/superpowers>
- License: MIT; see `LICENSE`.
- Source release: Superpowers plugin version `7.0.0`.
- Imported files: only `test-driven-development/SKILL.md` and `systematic-debugging/SKILL.md`.
- SHA-256 hashes below refer to the unmodified upstream skill files.

| Skill | SHA-256 |
| --- | --- |
| `test-driven-development/SKILL.md` | `64b03fce4aee5a97a93160cea8111f3ba13a17b7c001db4bd5836d67fd10705d` |
| `systematic-debugging/SKILL.md` | `51c6435d98c83c42c96ba7c35725a0b2c376cd487fb1a4e6bd0ddbe7e33ef202` |

To refresh on Windows, download or clone the desired upstream release, review its license and changes, then replace the canonical skill files. Recompute the hashes with `Get-FileHash -Algorithm SHA256`; update this file and reload the runtimes. Do not update automatically without reviewing upstream changes.

These skills are agent guidance, not permission to run commands or expand task scope. They should be loaded only when testing or debugging work calls for them.

## Thunai-authored skills (not from upstream)

All other folders in this directory are written for this project and are edited by hand here: `thunai`, `orient`, `plan`, `construct`, `code-review`, `git-workflow`, `memory-curator`, `web-security`, plus any installed pack skills. The hash table above covers only the two imported upstream skills. Their supporting files (for example `root-cause-tracing.md`, `writing-good-tests.md`) are also from upstream and are not hash-tracked.

## How the runtimes reach these files

`python .thunai/sync.py` generates tiny entry points in `.claude/skills/` (Claude Code, and OpenCode through its Claude compatibility path) and `.github/skills/` (Copilot). OpenCode also lists `./skills` in `opencode.jsonc`. After adding or renaming a skill here, run the sync; `python .thunai/sync.py --check` fails if the entry points drift.

## Line endings

The SHA-256 values above are for the upstream files with LF line endings. `.gitattributes` keeps `skills/` as LF so `Get-FileHash` reproduces them. A CRLF checkout changes the hash without changing the content.

## Upstream cross-references

The imported skills mention other upstream skills by their `superpowers:` names. In a project built from this template `superpowers:test-driven-development` means the local `test-driven-development` skill. `superpowers:verification-before-completion` and `superpowers:writing-skills` are not imported; Thunai's `verification-honesty` rule (no claim without a command that ran and its real result) covers the first. The upstream files are left unmodified so their hashes stay valid.

