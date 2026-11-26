---
name: orient
description: Session briefing and progress check for Thunai. Reads the team's docs folder (`docs/<team>`) for sprints, architecture, project plan and specifications, then reports where the user is, what their next milestone or sprint item is, citing sources, and says explicitly when something cannot be found. Trigger on /orient, session start, after a context reset, "what's next for me", "where are we", "what should I work on".
---

# Orient

**Purpose:** tell the user, from evidence, where they are and what their next piece of work is. Never guess.

## Workflow
1. Read `.thunai/memory/operating-rules.md`, `operating-directives.md`, `who-owns-what.md`.
2. Run the read-only fact gatherer: `python .thunai/scripts/orient_snapshot.py` (add `--name <first name>` if the docs refer to the user by name). It reports:
   - git state, with the branch name parsed into team (if multi-team), sprint, type and issue (see the branch-naming rule);
   - GitHub login, your assigned open issues with milestones, and open milestones with progress;
   - **the team docs inventory** (below);
   - `not_found`: everything it could not determine, with the reason.
3. **Read the team's docs.** The script finds the folder for the active team under `docs.root` (name from `docs.teamFolder`, else `activeTeam`; `Team-X`, `Team X`, `Team_X`, `TeamX`, `x`, any casing) and groups its files as `sprints`, `architecture`, `specifications`, `project_plan` and `other`. Read what the briefing needs, in this order:
   1. the sprint documents: the latest first, plus any listed in `hits` (lines that mention your issues, your login or your name);
   2. the project plan (milestones, schedule, roadmap);
   3. the architecture and specification documents, enough to understand the area of the user's next work.

   Also read shared docs (`scope: shared`: files directly in `docs/`, `docs/Shared`, `docs/Common`, and `docs.shared` paths). **Do not read another team's folder** (`other_team_folders_not_read`); mention that it exists and was not read. Files marked `readable_by_script: false` (`.pdf`, `.docx`, `.pptx`, `.xlsx`) are listed but not searched: open them with the matching skill or tool when needed, and say if you could not.
4. If the script cannot run, fall back to read-only commands (`git branch --show-current`, `git status --short`, `gh auth status`, `gh issue list --assignee "@me"`, listing `docs/`) and say the script failed.
5. Produce the briefing below.

## How to decide "your next work" (in this order)
1. **A team sprint document says so explicitly:** it names the user (login or name from `who-owns-what.md`) or their issue number as next, in progress or planned. This wins. Cite `file:line`.
2. **The team project plan says so:** a milestone or schedule entry for the user's issue or area. Cite it.
3. **GitHub says so:** otherwise, from the user's assigned open issues, take the milestone with the earliest due date and, within it, the lowest issue number. Label it **suggested from GitHub milestones, not stated in a plan document**.
4. **None of these:** say **"Not able to find your next milestone or sprint item"** and list what is missing and how to fix it (add the sprint or plan docs under the team folder, assign issues, attach milestones).

## Current sprint
Report a *current* sprint only when evidence says so: a sprint document whose dates include today's date, a milestone named after the sprint, or a doc that states it. Otherwise write **"Not able to find the current sprint"** and give the latest sprint document found (for example "latest sprint document: Sprint 02") as a fact, not as the current sprint. The highest sprint number is not automatically the current one.

## Hard rules
- Report only what the snapshot or the documents show. If a field is missing, write "Not able to find: <field>" and the reason. Do not fill gaps from memory, naming patterns or assumptions.
- GitHub has no native sprint field: take a sprint only from the team docs, an issue label or a milestone name, and cite where.
- ADO or Jira links (for example `AB#12345`) cannot be queried from here. If the plan depends on them, say so.
- Team scope: the work must fall under the configured team. If the next item belongs to another team, flag it instead of recommending it.
- "My current change": use the parsed branch (`branch_parts`). If the branch does not follow the convention (`branch_problems`), say so and list the problems.
- The sprint number for a new branch comes from this briefing. If it is "Not able to find", ask the user.

## Output
```
**Where you are**
Branch `<name>`: team <team>, sprint <NN>, <type>, issue #<n>   (or: does not follow the branch convention: <problem>)
Working tree: clean / <n> changed | GitHub: <login> on <repo>
Current change: #<n> <title> (milestone <m>)   or   Not able to find: <reason>

**Your team docs** (`docs/<team>`)
Sprints: 01, 02 (latest document: 02) | Architecture: <n> | Specifications: <n> | Project plan: <n>
Not read: docs/<other-team> (other team)   Could not open: <binary files, if any>

**Your next work**
Next: #<n> <title>
Milestone: <name> (due <date>)   Sprint: <name, source>   or   Not able to find
Why: <one line: doc cite `file:line`, or "suggested from GitHub milestones">

**Team progress**
<milestone>: <closed> closed / <open> open (<pct>%)   (max 3 lines)

**Not able to find**
- <item>: <reason>

**Next step** (options, one Recommended)
```
Keep it under about 30 lines. Always include "Not able to find" when the snapshot's `not_found` list is non-empty.
