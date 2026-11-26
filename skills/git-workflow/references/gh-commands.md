# GitHub CLI Reference

```text
gh auth status
gh api user --jq .login
gh issue list --assignee "@me"
gh issue list --state all --search "<keywords>"
gh issue view <n>
gh issue create --title "<t>" --body-file <file>     # only after user approval
gh pr create --base main --title "<t>" --body-file <file>   # only after user approval
gh issue comment <n> --body "PR: <url>"              # update the issue with the PR URL
```

Never pass personal email addresses or secrets in titles or bodies.
