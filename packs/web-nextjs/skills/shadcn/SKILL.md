---
name: shadcn
description: Manages shadcn components and projects — adding, searching, fixing, debugging, styling, and composing UI, including chat interfaces. Provides project context, component docs, and usage examples. Applies when working with shadcn/ui, component registries, presets, or any project with a components.json file.
---

# shadcn/ui

Components for React and Next.js built on Tailwind CSS. Everything lives directly in the project codebase (`frontend/src/components/ui/`), giving full ownership and customization.

## Core Rules

1. **Check `components.json` first**:
   Always inspect `components.json` in `frontend/` to determine path aliases (e.g. `@/components/ui`), Tailwind setup, icon libraries (`lucide-react`), and base components.

2. **Compose, Don't Reinvent**:
   - Before writing custom UI elements, check available components in `frontend/src/components/ui/` (`Card`, `Badge`, `Button`, `Input`, `Skeleton`, `Field`, `Table`, etc.).
   - Combine primitives cleanly (e.g., Metric Card = `Card` + `CardHeader` + `CardTitle` + `CardDescription` + `CardContent` + `Badge`).

3. **Semantic Theming Tokens**:
   - Always use design tokens: `bg-background`, `text-foreground`, `bg-muted`, `text-muted-foreground`, `bg-primary`, `text-primary-foreground`, `border-border`, `bg-card`, etc.
   - Do NOT use hardcoded colors (`bg-blue-500`, `text-gray-400`) unless explicitly required for status semantics (e.g., green for delivered, amber for delay, red for exception).

4. **Component Addition**:
   To add new shadcn components, use the project package runner from `frontend/`:
   ```bash
   npx shadcn@latest add <component-name>
   ```

5. **Accessibility**:
   - Ensure all interactive elements have accessible labels (`aria-label`, `aria-describedby`).
   - Retain focus rings (`focus-visible:ring-2 focus-visible:ring-ring`).
