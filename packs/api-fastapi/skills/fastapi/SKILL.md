---
name: fastapi
description: FastAPI service development for this project - routers, Pydantic v2 schemas, dependencies, lifespan, async, error handling and tests. Trigger on FastAPI, APIRouter, endpoint, Pydantic, pydantic-settings, Depends, lifespan, uvicorn, API route in Python.
---

# FastAPI

**First:** check the installed `fastapi`, `pydantic` and `sqlalchemy` versions in `pyproject.toml` or `requirements`. The notes assume current FastAPI with Pydantic v2.

## Structure
- Organize by domain: `router.py`, `schemas.py`, `service.py` (business logic), `dependencies.py`, `models.py` per feature, wired in `main.py`. Keep route functions thin; put logic in services.
- Use `APIRouter` with prefix and tags. Set `response_model`, explicit `status_code`, and documented error responses.

## Pydantic v2
- Separate schemas for create, update and read. Use `model_config = ConfigDict(from_attributes=True)` instead of an inner `Config`; `field_validator` / `model_validator`, not v1 `@validator`; `model_validate` / `model_dump`, not `parse_obj` / `.dict()`.
- Put constraints in `Annotated[..., Field(...)]`. Never return ORM objects or secrets directly; return a read schema.
- Configuration via `pydantic-settings` `BaseSettings` (separate package in v2), cached with `lru_cache`; no `os.getenv` scattered through the code.

## Dependencies and lifespan
- Use `Annotated[T, Depends(...)]` aliases (for example `DbSession = Annotated[AsyncSession, Depends(get_db)]`).
- Use the `lifespan` async context manager for startup and shutdown; `@app.on_event` is deprecated. Hold shared resources (DB engine, HTTP client) on `app.state`.
- Scope correctly: per-request (DB session, current user), router-level, application-level.

## Async rules
- `async def` for I/O-bound endpoints with async libraries; plain `def` for blocking or CPU-bound work (it runs in a threadpool). Never call blocking code inside `async def`.
- Long work goes to a background task or queue, not the request.

## Errors, security, tests
- Raise `HTTPException` or register exception handlers for domain errors; return a consistent error body (see `api-design`).
- Authenticate and authorize through dependencies on every protected route; restrict CORS to known origins (see `web-security`).
- Test with `TestClient` or `httpx.AsyncClient`; use `app.dependency_overrides` for fakes; cover success, validation failure (422), auth failure and not-found paths.

## Security specifics
- Enforce authorization with dependencies on routes, and check object-level ownership.
- Validate input with Pydantic schemas; use parameterized queries only (see `sqlalchemy-alembic`).
- Configure CORS with explicit origins; never `*` with credentials.
- See also the core `web-security` skill.