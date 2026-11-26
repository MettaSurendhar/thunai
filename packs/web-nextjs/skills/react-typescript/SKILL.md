---
name: react-typescript
description: React and TypeScript component and state conventions for frontend work in this project. Trigger on .tsx/.ts files, React component, hook, props, state, forms, TypeScript types, "refactor this component".
---

# React and TypeScript

Follow the project's existing libraries (forms, data fetching, UI kit, styling) before introducing any new one.

## TypeScript
- `strict` mode on. No `any`; use `unknown` and narrow. Prefer `type` for props and unions, `interface` for extendable object shapes.
- Derive types from a single source (schema or API contract) instead of re-declaring them. Validate untrusted data at the boundary (API responses, form input, URL params).
- Use discriminated unions for states (`{status: 'loading'} | {status: 'error', error} | {status: 'ok', data}`) rather than parallel booleans.

## Components
- Small, single-purpose components with explicit typed props; no prop drilling past two levels (lift to context or compose).
- Derive values during render; do not mirror props into state or use an effect to compute derived data.
- Effects are for synchronizing with external systems only. Include correct dependencies; clean up subscriptions and timers.
- Stable `key`s from data ids, never array index for dynamic lists.
- Do not memoize by default. Measure first; the React Compiler (stable in Next.js 16) handles most cases when enabled.

## State and data
- Keep state as local as possible; server state belongs in the server or the project's data-fetching library, not in global client state.
- Forms: controlled inputs or the project's form library; show field-level errors; disable submit while pending; keep server validation as the source of truth.

## Quality
- [ ] No type errors (`tsc --noEmit` or the project's check)
- [ ] No unused state, props or exports
- [ ] Loading, empty and error states handled
- [ ] Tests cover behavior (see `frontend-quality`)
