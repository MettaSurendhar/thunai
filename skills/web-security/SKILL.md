---
name: web-security
description: Web application security checks - authentication, authorization, input validation, XSS, CSRF, injection, secrets, CORS, dependencies. Trigger on auth, login, permissions, security review, user input, cookies, CORS, secrets, "is this secure".
---

# Web Security

Apply on every change that touches auth, user input, data access, config or dependencies. Findings go into `code-review` output. Framework-specific hardening lives in the stack-pack skills you have installed (for example `nextjs`, `fastapi`).

## Authentication and authorization
- Authorize on the server for every request, in the framework's route, handler or action layer. A hidden button or a client-side redirect is not authorization.
- Check object-level access (does *this user* own *this record*), not only that they are logged in.
- Cookies for sessions: `HttpOnly`, `Secure`, `SameSite`. Never store tokens in `localStorage` unless the project already mandates it.

## Input and output
- Validate and constrain all input at the boundary with a schema. Whitelist, do not blacklist.
- Prevent injection: parameterized queries only; never pass user input to shell, `eval` or file paths unchecked.
- Prevent XSS: rely on the framework's output escaping; avoid raw-HTML sinks, and sanitize if unavoidable.
- Prevent SSRF: do not fetch user-supplied URLs without an allowlist.

## Secrets and config
- No secrets in code, logs, client bundles or commits. Anything shipped to the browser is public.
- CORS: explicit allowed origins, methods and headers; never `*` with credentials.
- Return generic errors to clients; log details server-side without personal data or secrets.

## Dependencies
- Do not add packages without approval. Run the audit tools the project uses (see `commands` in `.thunai/config/project.config.json`) and report results, or say they were not run.

## Report
For each concern: file and line, risk, fix. State what could not be verified.