---
name: nextjs
description: Next.js App Router development for this project - Server and Client Components, Server Actions, route handlers, caching, proxy, metadata, performance. Trigger on Next.js, App Router, app/ directory, page.tsx, layout.tsx, route.ts, Server Action, middleware/proxy, next.config.
---

# Next.js (App Router)

**First:** read `package.json` for the installed `next` and `react` versions and follow that version's behavior. The notes below reflect Next.js 16; if the project is on 14 or 15, check what differs before applying them.

## Structure and components
- Components are **Server Components by default**. Add `'use client'` only for state, effects, event handlers or browser APIs, and push the boundary as far down the tree as possible.
- Fetch data in Server Components (or server functions), not in `useEffect`. Run independent requests in parallel (`Promise.all`); stream slow parts with `loading.tsx` or `<Suspense>`.
- Use the file conventions: `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `route.ts`. Co-locate feature code; keep shared UI in one place.
- Never import server-only code (DB, secrets) into a client component. Mark such modules with `import 'server-only'`.

## Next.js 16 specifics to get right
- **Async request APIs:** `params`, `searchParams`, `cookies()`, `headers()` and `draftMode()` are async and must be awaited. Type `params` as a `Promise` in pages and layouts.
- **`proxy.ts` replaces `middleware.ts`** (the function is named `proxy`; `middleware.ts` still works but is deprecated). Keep it thin: redirects, rewrites, header checks. Do not put authorization logic only here.
- **Caching is opt-in** with Cache Components (`cacheComponents: true` in `next.config.ts`) and the `'use cache'` directive. `revalidateTag` now takes a cache-life profile as a second argument; `updateTag` and `refresh` exist for Server Actions. Check the docs for the project's version before using them.
- Turbopack is the default bundler; Node 20.9 or newer is required. The codemod `npx @next/codemod@canary upgrade latest` handles most upgrade changes (propose it, do not run it unasked).

## Server Actions and route handlers
- Treat every Server Action and route handler as a **public HTTP endpoint**: validate input on the server (schema), authenticate, and authorize inside it. Never trust hidden fields or client state.
- Return typed results (`{ ok: true, data } | { ok: false, error }`) instead of throwing for expected failures.
- Revalidate affected paths or tags after a mutation.

## Config, env, assets
- Only variables prefixed `NEXT_PUBLIC_` reach the browser. Never put secrets there.
- Use `next/image` and `next/font`; set `width`/`height` or `fill`; use the `metadata` API for titles and SEO.

## Checklist
- [ ] No `'use client'` higher than needed
- [ ] Inputs validated and authorization checked server-side
- [ ] Async request APIs awaited
- [ ] `loading`/`error` states exist for new routes
- [ ] `npm run build` and `npm run lint` (or the project's commands) were run and reported

## Security specifics
- Authorize inside every Server Action and route handler; a `proxy.ts` redirect is not authorization.
- Validate every Server Action input with a schema; avoid `dangerouslySetInnerHTML`.
- Only `NEXT_PUBLIC_*` values reach the browser, so treat them as public.
- See also the core `web-security` skill.