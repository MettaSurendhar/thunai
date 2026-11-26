# Example tracking file (local-only)

Real tracking files are git-ignored. Create one per independent issue, for example `.thunai/tracking/issue-123-short-name.md`, to hold issue or PR drafts before you publish them. Delete this example if you do not need it.

## Issue draft

**Title:** feat: add CSV export to the orders list

**Context:** Support asked for a way to download the filtered orders list.

**Acceptance criteria**
- [ ] An "Export CSV" action downloads the rows matching the current filters.
- [ ] The file has a header row and one row per order.
- [ ] Empty results produce a header-only file.

**Out of scope:** scheduled exports, other formats.

## PR draft

**Title:** feat(orders): add CSV export (#123)

**Related Issue:** Closes #123

**What changed:** (summary)

**How it was verified:** (exact commands and real results)