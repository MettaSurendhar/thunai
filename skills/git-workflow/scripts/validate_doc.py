#!/usr/bin/env python3
"""Validate an issue or PR draft.

Usage: validate_doc.py --kind pr|issue <file> [--branch NAME]
  --branch  (pr only) the PR's source branch; its issue number must appear under "Related Issue".
Exit 0 ok, 1 invalid, 2 error.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_branch  # noqa: E402

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
ANGLE = re.compile(r"<[^>\n]+>")
TYPES = ["bug", "feature", "enhancement", "task", "documentation"]

PR_SECTIONS = ["Summary", "Changes", "Related Issue", "Testing and Verification", "Risks and Performance"]
ISSUE_REQUIRED = ["Type", "Description", "Expected Outcome", "Acceptance Criteria"]
BUG_REQUIRED = ["Environment", "Steps to Reproduce", "Actual Behavior", "Expected Behavior"]

# Guidance text from the template that must be replaced with real content.
GUIDANCE = [
    "Short and clear summary of the issue",
    "Describe the problem, requirement, or work to be done",
    "What should the final result look like?",
    "Criterion 1", "Criterion 2", "Criterion 3",
    "What happens today?", "What should happen instead?",
    "Include any helpful information such as",
    "Environment: Dev / Test / UAT / Prod",
]


def norm(heading):
    """'Type * (Required)' -> 'Type'."""
    h = re.sub(r"\((?:Required|Optional)[^)]*\)", "", heading)
    return h.replace("*", "").strip()


def split_sections(text):
    """Return ({name: body}, title_body) using '# ' and '## ' headings; '---' lines are ignored."""
    sections, current, title = {}, None, None
    for line in text.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^(#{1,2})\s+(.*)$", line)
        if m:
            current = norm(m.group(2))
            if m.group(1) == "#" and current.lower() == "title" and title is None:
                title = current
                sections["Title"] = ""
                current = "Title"
            else:
                sections.setdefault(current, "")
            continue
        if current is not None and line.strip() != "---":
            sections[current] += line + "\n"
    return sections


ISSUE_REF = re.compile(r"(?i)\b(closes|fixes|resolves|refs?)\s+#(\d+)")


def check_pr(text, branch=None):
    problems = []
    headings = {norm(h) for h in re.findall(r"^##\s+(.+)$", text, re.M)}
    for sec in PR_SECTIONS:
        if sec not in headings:
            problems.append(f"missing section: ## {sec}")
    related = split_sections(text).get("Related Issue", "")
    refs = [int(n) for _, n in ISSUE_REF.findall(related)]
    if "Related Issue" in headings and not refs:
        problems.append("Related Issue must list at least one issue, e.g. 'Closes #123' (use 'Refs #n' for issues that stay open)")
    if branch:
        cfg = validate_branch.load_config()
        _, _, parts = validate_branch.validate(branch, cfg)
        if parts and parts.get("issue") and int(parts["issue"]) not in refs:
            problems.append(f"Related Issue must include #{parts['issue']}, the issue in the branch name '{branch}'")
    for ph in sorted(set(ANGLE.findall(text)))[:5]:
        problems.append(f"unfilled placeholder: {ph}")
    return problems


def check_issue(text):
    problems = []
    sec = split_sections(text)
    body = lambda name: sec.get(name, "").strip()  # noqa: E731

    if "Title" not in sec or not body("Title"):
        problems.append("missing '# Title' with a one-line summary")
    for s in ISSUE_REQUIRED:
        if s not in sec:
            problems.append(f"missing required section: ## {s}")
        elif not body(s):
            problems.append(f"section is empty: ## {s}")

    checked = []
    for line in body("Type").split("\n"):
        m = re.match(r"^\s*-\s*\[([ xX])\]\s*(.+?)\s*$", line)
        if m and m.group(1).lower() == "x":
            checked.append(m.group(2).lower())
    if len(checked) != 1 or checked[0] not in TYPES:
        problems.append("Type: tick exactly one of Bug, Feature, Enhancement, Task, Documentation")
    is_bug = checked == ["bug"]

    ac = [ln for ln in body("Acceptance Criteria").split("\n") if re.match(r"^\s*-\s*\[[ xX]\]\s*\S", ln)]
    if not ac:
        problems.append("Acceptance Criteria: add at least one '- [ ] criterion'")

    if is_bug:
        for s in BUG_REQUIRED:
            if s not in sec:
                problems.append(f"Bug issues require section: ## {s}")
            elif not body(s) or body(s).strip() in ("1.\n2.\n3.", "1.\n2.\n3"):
                problems.append(f"Bug section is empty: ## {s}")
        env = body("Environment")
        for key in ("Repo", "Branch"):
            if not re.search(rf"^-\s*{key}:\s*\S", env, re.M):
                problems.append(f"Environment: fill in '{key}'")
        m = re.search(r"^-\s*Environment:\s*(.+)$", env, re.M)
        if not m or "/" in m.group(1):
            problems.append("Environment: choose one of Dev, Test, UAT, Prod")
        steps = [ln for ln in body("Steps to Reproduce").split("\n") if re.match(r"^\s*\d+\.\s*\S", ln)]
        if not steps:
            problems.append("Steps to Reproduce: add at least one numbered step")

    for g in GUIDANCE:
        if g in text:
            problems.append(f"unfilled template text: {g!r}")
    for ph in sorted(set(ANGLE.findall(text)))[:5]:
        problems.append(f"unfilled placeholder: {ph}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["pr", "issue"], required=True)
    ap.add_argument("file")
    ap.add_argument("--branch")
    args = ap.parse_args()
    try:
        text = open(args.file, encoding="utf-8").read()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    problems = check_pr(text, args.branch) if args.kind == "pr" else check_issue(text)
    if EMAIL.search(text):
        problems.append("contains an email address; never publish personal emails")
    if problems:
        print("INVALID:\n- " + "\n- ".join(problems))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
