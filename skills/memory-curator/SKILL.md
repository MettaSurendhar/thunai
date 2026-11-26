---
name: memory-curator
description: Update Thunai's persistent memory when the user corrects behavior or states a standing preference. Trigger on any correction ("don't do that", "always do X"), "remember this", or when drift is noticed.
---

# Memory Curator

## Where things go
| Fact | File |
|---|---|
| A correction to Thunai's behavior | `.thunai/memory/operating-rules.md` (Corrections log) |
| A standing preference, routing or artifact format | `.thunai/memory/operating-directives.md` |
| Who owns which workstream or repo | `.thunai/memory/who-owns-what.md` |
| In-progress plan for this session | `.thunai/memory/session/plan.md` (git-ignored) |

## Workflow
1. In the same turn as the correction, add a dated line: `- [YYYY-MM-DD] Rule - why - how to apply`.
2. Never silently condense or delete existing content. Merge duplicates by showing the user.
3. Never store secrets, tokens or personal email addresses.
4. Tell the user in one line what was recorded and where.
