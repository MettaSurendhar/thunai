---
name: tailwindcss
description: Tailwind CSS v4 architecture, styling patterns, and utility-first conventions. Use when writing, modifying, or refactoring CSS/Tailwind classes, responsive layouts, theme tokens, OKLCH colors, or CSS animations in Next.js.
---

# Tailwind CSS v4

Tailwind CSS v4 conventions for Next.js App Router in this project.

## Core Rules

1. **CSS-First Configuration**:
   - Tailwind v4 eliminates `tailwind.config.js`. Theme definitions, custom utilities, and color tokens live in `globals.css` using `@theme` and OKLCH color spaces.
   - Do not add or reference legacy `tailwind.config.js` or `tailwind.config.ts`.

2. **Semantic Design Tokens over Arbitrary Values**:
   - Use semantic design tokens: `bg-background`, `text-foreground`, `bg-card`, `text-card-foreground`, `bg-muted`, `text-muted-foreground`, `bg-primary`, `text-primary-foreground`, `border-border`.
   - Avoid arbitrary pixel values like `w-[287px]` when standard grid/flex or Tailwind spacing scale (`w-72`, `max-w-md`) suffices.

3. **Responsive Design**:
   - Mobile-first breakpoints: default (mobile), `sm:`, `md:`, `lg:`, `xl:`.
   - Use CSS Grid and Flexbox for dashboards (`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4`).

4. **Class Composition with `cn()`**:
   - Always merge dynamic classes using the project's `cn(...)` utility (`import { cn } from "cn"`).
   - Never manually concatenate strings with ternary expressions without `cn()`.

5. **Motion and Micro-Interactions**:
   - Use `transition-all duration-200 hover:scale-[1.01] hover:shadow-md` for interactive cards.
   - Use `animate-pulse`, `animate-spin`, or `animate-ping` for live operational states.
