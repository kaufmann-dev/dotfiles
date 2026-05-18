---
name: write-design
description: Create or update DESIGN.md with visual identity, design tokens, component styling, and interaction guidance.
---

# Write DESIGN.md

## Purpose

Create or refresh `DESIGN.md` as the project-scope source of truth for design systems and visual identity.

## Use When

- The user asks for `DESIGN.md`, design tokens, visual identity, or UI style rules.
- A frontend project needs a persistent design system for agents to follow.
- Existing visual guidance is missing, scattered, or inconsistent.

## Do Not Use When

- The user wants setup or usage docs; use `write-readme`.
- The user wants technical architecture; use `write-architecture`.
- The user wants agent workflow rules; use `write-agents`.
- The target is this global dotfiles repo and no project-scope design system was requested.

## Document Boundary

| File | Owns |
| --- | --- |
| `DESIGN.md` | Visual identity, colors, typography, spacing, shape, elevation, components, motion, accessibility constraints |
| `ARCHITECTURE.md` | Stack, runtime structure, data flow, integrations, and deployment shape |
| `README.md` | Human setup, usage, and navigation |
| `AGENTS.md` | Agent-specific workflow and repo constraints |

## Workflow

1. Read existing design docs, UI code, style config, component libraries, screenshots, and brand assets.
2. For new or substantial docs, consult the local references:
   - `references/SPEC.md`
   - `references/BEST_PRACTICES.md`
3. Define machine-readable tokens in YAML front matter when creating a full `DESIGN.md`.
4. Keep prose tied to tokens using `{path.to.token}` references where practical.
5. Use hex colors, exact dimensions, semantic typography tokens, and component token references.
6. Avoid architecture, setup, and agent workflow content.

## Suggested Shape

```markdown
---
version: alpha
description: Project design system for coding agents.
colors:
  primary: "#1A1C1E"
typography:
  body-md:
    fontFamily: Inter
    fontSize: 1rem
spacing:
  md: 16px
rounded:
  md: 8px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
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

## Output

A `DESIGN.md` that gives agents exact visual rules and enough rationale to apply them consistently.

## Completion Rules

Finish only when the design guidance is specific, token-backed where appropriate, and free of architecture or README content.
