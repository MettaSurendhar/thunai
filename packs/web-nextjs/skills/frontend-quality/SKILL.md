---
name: frontend-quality
description: Frontend testing, accessibility, responsive design and performance checks for UI work in this project. Trigger on UI tests, React Testing Library, Vitest, Jest, Playwright, accessibility, a11y, responsive layout, Core Web Vitals, bundle size.
---

# Frontend Quality

## Testing
- Use the project's runner (commonly Vitest or Jest with React Testing Library; Playwright for end-to-end). Do not add a second runner.
- Test what the user sees and does: query by role, label and text, not by class name or implementation detail. Use `userEvent` for interactions.
- Test one behavior per test; cover loading, empty, error and success states. Mock the network boundary only.
- Follow `test-driven-development`: show the test failing first.
- Use Playwright for critical flows only (search, submit, auth); keep selectors role-based.

## Accessibility (WCAG 2.2 AA baseline)
- Semantic HTML first (`button`, `a`, `nav`, `main`, headings in order); ARIA only when HTML cannot express it.
- Every input has a visible label; errors are announced and linked (`aria-describedby`).
- Everything operable by keyboard with a visible focus state; no focus traps except in modals.
- Text contrast of at least 4.5:1; do not convey meaning by color alone; images have meaningful `alt` (empty for decorative).

## Responsive and performance
- Mobile-first layouts; verify at narrow, medium and wide widths. No horizontal page scroll.
- Optimize images with `next/image`, lazy-load below the fold, split heavy client code with dynamic imports, avoid large client-only dependencies.
- Watch LCP, INP and CLS: reserve space for media, avoid layout shift, keep interactions fast.

## Report
List tests run with results, plus any accessibility or performance check you could not run.
