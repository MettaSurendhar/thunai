---
description: "MANDATORY for every agent. Never store, print or publish secrets, credentials or personal email addresses."
applyTo: "**"
---

# Security and Privacy

- Never store, print or commit secrets, tokens, keys or connection strings. Config files hold none.
- Never publish personal email addresses in issues, PRs, commits or tracking files.
- Do not read `.env` files or credential stores unless the user explicitly asks.
- Do not add dependencies or generated artifacts to a commit without the user's approval.
- If a secret is found in the repo or in output, stop, tell the user, and do not repeat it.
