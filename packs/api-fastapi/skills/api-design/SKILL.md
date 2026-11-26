---
name: api-design
description: HTTP API design and the contract between the Next.js frontend and the FastAPI backend for this project. Trigger on API design, endpoint naming, status codes, pagination, error format, OpenAPI, API contract, versioning, request/response shape.
---

# API Design

## Contract first
- The FastAPI OpenAPI schema is the source of truth between backend and frontend. When the project generates TypeScript types or a client from it, regenerate instead of hand-writing types. If it does not, keep frontend types in one place and match the schema.
- A change to a response shape is a contract change: update both sides in the same plan and call it out in the PR.

## Endpoints
- Resource-oriented nouns, plural, lowercase (`/policies`, `/policies/{policy_id}`); verbs only for true actions (`POST /policies/{id}/cancel`).
- Correct methods and status codes: 200, 201 (with `Location`), 204, 400, 401, 403, 404, 409, 422, 429, 5xx. Do not return 200 with an error body.
- `GET` is safe and idempotent; make `PUT` and `DELETE` idempotent; consider idempotency keys for payment-like `POST`s.

## Lists
- Paginate every list endpoint (cursor or `limit`/`offset` with a maximum). Support explicit filtering and sorting fields; whitelist sort keys.
- Return pagination metadata in a consistent envelope.

## Errors
- One error shape across the API (for example RFC 9457 problem details, or the project's existing format) with a stable machine-readable code, a human message and field errors for validation. Never leak stack traces or internals.

## Compatibility
- Prefer additive changes. Breaking changes need versioning (`/v2/...`) or a deprecation path agreed in the issue.
- Document every endpoint through its schema (summary, response models, error responses).
