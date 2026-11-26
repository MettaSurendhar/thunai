# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

Versioning policy: breaking changes to the config schema (`project.config.json`), `pack.json`, the `init.py` flags, or the generated file layout bump the major version. New packs, skills and options bump the minor version. Fixes and wording changes bump the patch version.

## [Unreleased]

### Added
- `adopt.py`: one-command install into an existing repository (copies the kit, merges shared config files, runs `init.py`, never runs git).

## [0.1.0] - 2026-11-25

First public release.

### Added
- Orchestrator agent (Thunai) and five specialists (planning, coding, testing, debugging, review), core skills, rules, commands, persistent memory and a git guard.
- Generator (`.thunai/sync.py`) producing native configuration for GitHub Copilot, Claude Code and OpenCode from one source.
- `init.py` bootstrap with opt-in packs `web-nextjs` and `api-fastapi`, and configurable teams.
- Open-source scaffolding: MIT `LICENSE`, `THIRD_PARTY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, issue and pull request templates, CODEOWNERS, Dependabot for GitHub Actions.
- CI on Linux, Windows and macOS: sync check, git guard tests, template validation, `init.py` smoke test.
- `.thunai/scripts/validate_template.py` and `.thunai/scripts/smoke_init.py`.
- Docs: `.thunai/docs/adding-a-pack.md`, `.thunai/docs/using-the-template.md`.