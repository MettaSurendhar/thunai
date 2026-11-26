# Memory Operating Protocol - READ AT SESSION START

## 0. Why this exists
Agents lose context between sessions. Memory files keep corrections and standing facts so behavior stays consistent.

## 1. Taxonomy
| File | Holds |
|---|---|
| `operating-rules.md` | Corrections and anti-drift rules |
| `operating-directives.md` | Standing preferences, routing, formats |
| `who-owns-what.md` | Ownership of workstreams and repos |
| `session/plan.md` | Current session plan (git-ignored) |

## 2. Read order at session start
operating-rules -> operating-directives -> who-owns-what -> session/plan (if present).

## 3. Update rules
- Add corrections in the same turn they are given (`memory-curator`).
- Never silently condense or delete content.
- Never store secrets, tokens or personal email addresses.
