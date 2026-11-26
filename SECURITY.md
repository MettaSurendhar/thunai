# Security policy

## Scope

Thunai is a template of Markdown, JSON and Python files. The security-relevant parts are:

- `.thunai/hooks/git_guard.py`: the hook that blocks unsafe git/`gh` commands from AI agents.
- `init.py` and `.thunai/sync.py`: scripts that read and write files in your project.
- Rules and skills that tell AI assistants what they may do (for example, the git governance and security rules).

A bypass of the git guard, a path-traversal or arbitrary-write issue in the scripts, or a rule or skill that instructs an assistant to expose secrets is in scope.

## Supported versions

Only the latest release receives fixes.

## Reporting a vulnerability

Please **do not open a public issue**. Report privately using GitHub's [private vulnerability reporting](https://github.com/MettaSurendhar/thunai/security/advisories/new) on this repository.

Include what you found, how to reproduce it, and the impact. You can expect an acknowledgement as soon as the maintainer is able, a fix or mitigation plan after triage, and credit in the release notes unless you prefer otherwise.

## What not to include

Do not send real secrets, tokens or personal data in a report. Use redacted examples.

## Using the template safely

Thunai guides AI assistants; it is not a security boundary. The git guard reduces risk but does not replace branch protection, code review, or least-privilege credentials. Review what your assistant proposes before approving it.
