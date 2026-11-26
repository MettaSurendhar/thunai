# Review Checklist

## Scope
- [ ] Diff touches only the issue's assigned paths; no `outOfScope` paths changed without authorization
- [ ] Every acceptance criterion is met; nothing extra was added

## Correctness and tests
- [ ] New behavior has tests that would fail without the change
- [ ] No tests weakened, skipped or deleted
- [ ] Edge cases and error paths covered
- [ ] Results reported in the PR match what was actually run

## Quality
- [ ] Follows existing patterns (DRY, SOLID, KISS); no unneeded abstraction
- [ ] No dead code, debug output or commented-out blocks
- [ ] Public behavior changes are documented

## Security and privacy
- [ ] No secrets, tokens or connection strings
- [ ] No personal email addresses
- [ ] Inputs validated at boundaries; no new injection or path-traversal risk
- [ ] No unapproved dependencies

## Git hygiene
- [ ] Branch name passes `skills/git-workflow/scripts/validate_branch.py` (username, team, sprint, type, issue number)
- [ ] No unrelated files, generated artifacts or tracking files staged
