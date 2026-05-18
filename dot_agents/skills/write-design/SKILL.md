---
name: write-design
description: Use only when creating DESIGN.md from scratch. Never for editing existing files.
---

# Write DESIGN.md

Produces a compliant `DESIGN.md` per the `@google/design.md` spec: YAML front matter
(machine-readable tokens) + Markdown prose (human-readable rationale).

## Before Writing

- Inspect existing design docs, UI code, style config, component libraries,
  screenshots, and brand assets.
- Keep `DESIGN.md` limited to visual identity, tokens, components, motion, and
  accessibility. Do not include setup, architecture, or agent workflow content.

## File Structure

```
---
version: alpha
name: <string>
description: <string>
colors:
  <token-name>: "<hex>"
typography:
  <token-name>:
    fontFamily:
    fontSize:
    fontWeight:
    lineHeight:
    letterSpacing:
rounded:
  sm | md | lg | full: <dimension>
spacing:
  sm | md | lg: <dimension>
components:
  <component-name>:
    backgroundColor: "{colors.token}"
    textColor: "{colors.token}"
    rounded: "{rounded.token}"
    padding: <dimension>
---

## Overview
## Colors
## Typography
## Layout & Spacing
## Elevation & Depth
## Shapes
## Components
## Do's and Don'ts
```

## Token Rules

**Colors**
- Hex only (`"#1A1C1E"`). No `rgb()`, `rgba()`, or named colors.
- Role-based names: `primary`, `secondary`, `on-surface`, `surface-container`.
  Not: `blue`, `text-secondary`, `h1-color`.

**Typography**
- Semantic scale names: `headline-xl`, `body-md`, `label-sm`.
  Not: `h1`, `h2`, `body`.
- Single dimension notation: `1rem` not `1rem (16px)`.
- No `color` property inside typography tokens.

**Dimensions**
- Always include units: `8px`, `1.5rem`. Never bare numbers or descriptive text.

**Rounded / Spacing**
- Scale keys only: `sm`, `md`, `lg`, `full`. Not element names like `button`, `tag`.

**Token References**
- In prose and component values, reference tokens as `{colors.primary}`, `{rounded.sm}`.
  Never hardcode values in prose that are already defined as tokens.

**Components**
- Valid properties: `backgroundColor`, `textColor`, `typography`, `rounded`,
  `padding`, `size`, `height`, `width`.
- Variants (hover, active) are separate entries: `button-primary-hover`.

## Section Rules
- Use exactly the headers listed above, in that order.
- Do not number headers.
- Omit sections you have nothing to say about - no placeholder sections.
- Non-standard sections (`Design Philosophy`, `Animation`, `Breakpoints`) are not top-level.
  Fold them into the nearest canonical section as subsections.
- Put asset, iconography, motion, accessibility, and responsive guidance under
  the nearest canonical section instead of creating new top-level sections.

## After Writing

Validate:
```bash
npx @google/design.md lint DESIGN.md
```

Fix all `error` findings before delivering. Investigate `warning` findings -
especially `contrast-ratio` and `broken-ref` - and resolve or note them explicitly.
