#!/usr/bin/env python3
"""Claude Code PreToolUse hook: enforce Thunai's git/GitHub rules on every Bash command.

Decisions per command segment (split on && || ; | and newlines):
  DENY  (exit 2)        hard rule violations: add ./-A/--all, force-push, push to main,
                        commit/push while on main/master, --no-verify,
                        gh pr create without a PR body that references an issue (Closes/Fixes/Resolves/Refs #n)
  ASK   (JSON, exit 0)  any other git or gh command that can change state: the user must approve it
  ALLOW (exit 0)        read-only git/gh commands and everything that is not git/gh
"""
import json
import re
import os
import shlex
import subprocess
import sys

PROTECTED = ("main", "master")
ISSUE_REF = re.compile(r"(?i)\b(closes|fixes|resolves|refs?)\s+#\d+")
SPLIT = re.compile(r"\s*(?:&&|\|\||;|\||\n)\s*")

GIT_READ = {
    "status", "diff", "log", "show", "blame", "grep", "ls-files", "ls-tree", "rev-parse", "rev-list",
    "describe", "shortlog", "cat-file", "show-ref", "fetch", "whatchanged", "diff-tree", "name-rev",
    "merge-base", "check-ignore", "version", "help", "count-objects", "for-each-ref",
}
BRANCH_READ_FLAGS = {"-a", "--all", "-r", "--remotes", "-v", "-vv", "--verbose", "--list", "-l",
                     "--show-current", "--contains", "--merged", "--no-merged"}
GH_READ_VERBS = {"view", "list", "status", "diff", "checks"}
GH_GROUPS = {"pr", "issue", "repo", "release", "run", "workflow", "label", "project", "milestone",
             "gist", "cache", "secret", "variable", "ruleset", "search"}


def current_branch():
    try:
        return subprocess.check_output(["git", "branch", "--show-current"], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def tokens(segment):
    try:
        if os.name == "nt":  # posix mode would eat the backslashes of Windows paths
            return [x[1:-1] if len(x) > 1 and x[0] == x[-1] and x[0] in "'\"" else x for x in shlex.split(segment, posix=False)]
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def git_parts(toks):
    """Return (subcommand, args) after skipping git's global options."""
    i = 1
    while i < len(toks) and toks[i].startswith("-"):
        i += 2 if toks[i] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace") else 1
    return (toks[i], toks[i + 1:]) if i < len(toks) else ("", [])


def push_targets_protected(args):
    positional = [a for a in args if not a.startswith("-")]
    for ref in positional[1:]:  # first positional is the remote
        name = ref.lstrip("+").split(":")[-1]
        if name.removeprefix("refs/heads/") in PROTECTED:
            return True
    return False


def classify_git(toks, branch):
    sub, args = git_parts(toks)
    flags = [a for a in args if a.startswith("-")]
    if sub == "add":
        if any(a in (".", "-A", "--all") or (re.fullmatch(r"-[A-Za-z]+", a) and "A" in a) for a in args):
            return "deny", "git add ., -A and --all are forbidden: stage explicit paths."
        return "ask", "git add changes the index."
    if "--no-verify" in args and sub in ("commit", "push"):
        return "deny", "--no-verify is forbidden: do not skip hooks."
    if sub == "push":
        if any(a in ("--force", "-f") or a.startswith("--force-with-lease") for a in args):
            return "deny", "Force-push is forbidden unless the user runs it themselves."
        if push_targets_protected(args):
            return "deny", "Never push to main: open a pull request from a branch."
    if sub in ("commit", "push") and branch in PROTECTED:
        return "deny", f"You are on '{branch}': create a branch named per the branch-naming rule first. Never commit or push to main."
    if sub in GIT_READ:
        return None
    read_only = {
        "branch": all(a in BRANCH_READ_FLAGS for a in args) or not args,
        "tag": not args or args in (["-l"], ["--list"]),
        "stash": bool(args) and args[0] in ("list", "show"),
        "worktree": bool(args) and args[0] == "list",
        "submodule": not args or args[0] == "status",
        "remote": not args or args in (["-v"], ["show"]) or (args and args[0] == "show"),
        "config": any(f in ("--get", "--get-all", "--list", "-l") for f in flags),
        "reflog": not args or args[0] == "show",
    }
    if read_only.get(sub):
        return None
    return "ask", f"git {sub or '(unknown)'} can change the repository."


def pr_create_problem(rest):
    """Return a reason if `gh pr create` would open a PR without a related-issue reference, else None."""
    body, body_file = None, None
    for i, t in enumerate(rest):
        nxt = rest[i + 1] if i + 1 < len(rest) else None
        if t in ("--body-file", "-F"):
            body_file = nxt
        elif t.startswith("--body-file="):
            body_file = t.split("=", 1)[1]
        elif t in ("--body", "-b"):
            body = nxt
        elif t.startswith("--body="):
            body = t.split("=", 1)[1]
    if body_file and body_file != "-":
        try:
            with open(body_file, encoding="utf-8") as fh:
                body = fh.read()
        except OSError:
            return f"cannot read the PR body file '{body_file}'."
    if body is None:
        return ("gh pr create must pass the validated PR draft with --body-file; "
                "--fill, --web and interactive PRs are not allowed because they skip the related-issue check.")
    if not ISSUE_REF.search(body):
        return "the PR body must reference a related issue (for example 'Closes #123' or 'Refs #123')."
    return None


def classify_gh(toks):
    rest = toks[1:]
    if not rest:
        return None
    group, verb = rest[0], rest[1] if len(rest) > 1 else ""
    if group == "auth" and verb == "status":
        return None
    if group == "api":
        method = None
        for i, t in enumerate(rest):
            if t in ("-X", "--method") and i + 1 < len(rest):
                method = rest[i + 1].upper()
            elif t.startswith("--method="):
                method = t.split("=", 1)[1].upper()
        writes = any(t in ("-f", "-F", "--field", "--raw-field", "--input") for t in rest)
        if (method and method != "GET") or writes:
            return "ask", "gh api call that writes to GitHub."
        return None
    if group == "pr" and verb == "create":
        problem = pr_create_problem(rest[2:])
        if problem:
            return "deny", "A PR needs its related issue: " + problem
        return "ask", "gh pr create opens a pull request on GitHub."
    if group in GH_GROUPS and verb in GH_READ_VERBS:
        return None
    if group in ("search", "browse", "version", "help"):
        return None
    return "ask", f"gh {group} {verb}".strip() + " can change GitHub state."


def evaluate(command, branch):
    """Return ('deny'|'ask'|None, reason). Deny wins over ask."""
    asks = []
    for seg in (s for s in SPLIT.split(command) if s.strip()):
        toks = tokens(seg.strip())
        if not toks:
            continue
        if toks[0] == "git":
            res = classify_git(toks, branch)
        elif toks[0] == "gh":
            res = classify_gh(toks)
        else:
            res = None
        if res and res[0] == "deny":
            return res
        if res:
            asks.append(res[1])
    if asks:
        return "ask", " ".join(dict.fromkeys(asks))
    return None, ""


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command", "")
    decision, reason = evaluate(command, current_branch())
    if decision == "deny":
        print(f"Thunai guard blocked this command. {reason}", file=sys.stderr)
        return 2
    if decision == "ask":
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"Thunai: needs your approval. {reason}",
        }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
