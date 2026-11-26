---
name: magicui
description: UI animation and visual effects library designed for React, Next.js, and Tailwind CSS. Use when adding animated components, bento grids, number tickers, border beams, pulsing status beacons, particle effects, or interactive hero/dashboard sections.
---

# Magic UI

Visual animation and interactive micro-interaction components for Next.js, React, and Tailwind CSS, built to complement `shadcn/ui`.

## Core Guidelines

1. **Copy-and-Paste Architecture**:
   Like `shadcn/ui`, Magic UI components live directly in your source code under your components folder (for example `components/magicui/` or `ui/`).

2. **Recommended Patterns**:
   - **Bento Grid**: Structured, responsive grid system for dashboards (`BentoGrid`, `BentoCard`).
   - **Number Ticker**: Animated rolling counter for metrics, counts, and percentages.
   - **Border Beam / Shimmer**: Perimeter light animation highlighting priority or critical alert cards.
   - **Pulsing Status Beacon**: Radar / live pulse ping (`animate-ping`) for live status, active sessions, and real-time updates.
   - **Marquee / Animated Stream**: Smooth ticker tape for activity feeds and incoming events.

3. **Tailwind 4 & Motion Integration**:
   - Built with Tailwind CSS and CSS animations (`tw-animate-css`).
   - Where motion animations are needed, use lightweight CSS keyframes or standard React 19 transitions.

4. **Performance & Dignity**:
   - Animations must be subtle, purposeful, and enhance comprehension (status changes, priority, live data).
   - Respect `prefers-reduced-motion` at all times.
