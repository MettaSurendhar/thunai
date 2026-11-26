---
name: sqlalchemy-alembic
description: Database access with SQLAlchemy 2.0 and Alembic migrations for this project. Trigger on SQLAlchemy, Alembic, migration, ORM model, database schema, query, N+1, transaction, index.
---

# SQLAlchemy and Alembic

Check the project's SQLAlchemy and Alembic versions and whether it uses sync or async sessions; match it.

## Queries and sessions
- Use 2.0 style: `select(...)`, `session.execute` / `scalars`, typed `Mapped[...]` models. Use `AsyncSession` with `async_sessionmaker` in async apps.
- One session per request via a dependency; commit or roll back at a clear transaction boundary; never share sessions across tasks.
- Avoid N+1: use `selectinload` / `joinedload` for relationships you will read. Paginate large result sets.
- Parameterize everything. Never build SQL with f-strings or string concatenation.

## Schema and migrations
- Every schema change ships with an Alembic migration in the same PR. Generate with `alembic revision --autogenerate`, then **read and edit it**: autogenerate misses renames, data moves and some constraints.
- Never edit a migration that has been applied or merged; add a new one. Provide a working `downgrade` where feasible.
- Make migrations safe for live data: add nullable columns first, backfill, then add constraints; avoid long locks on large tables.
- Add indexes for columns used in filters, joins and ordering; add unique and foreign-key constraints in the database, not only in code.

## Testing
- Test against a real database engine matching production where possible; roll back per test. Test migrations upgrade and downgrade cleanly.

## Report
State which migration files were added and whether upgrade/downgrade were actually run.
