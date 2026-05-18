---
name: write-design
description: Create or append to DESIGN.md with a focused design system: visual identity, tokens, typography, spacing, shapes, elevation, and UI component styling. Use when the user asks to generate, improve, correct, or refresh DESIGN.md while keeping architecture, README content, and agent instructions out of the design document.
---

# Write DESIGN.md

Create or update `DESIGN.md` as the source of truth for the project's design system and visual identity.

## Document Boundaries

Keep the four project docs distinct:

| File | Owns | Design behavior |
| --- | --- | --- |
| `DESIGN.md` | Visual identity, colors, typography, spacing, shape, elevation, UI component styling, interaction feel | Write this file |
| `ARCHITECTURE.md` | Technology stack, components, data flow, integrations, runtime topology | Do not duplicate |
| `README.md` | Human overview, setup, usage, contribution entrypoints | Do not duplicate |
| `AGENTS.md` | Agent-only operating instructions | Do not include |

If implementation details matter to design, state them as design constraints only and link to `ARCHITECTURE.md` for technical details.

## Preservation Rule

If `DESIGN.md` already exists:

- Read the full file before editing.
- Preserve existing content.
- Append missing tokens, rules, or corrections under existing relevant headings or a new `## Design Additions` section.
- Do not delete or rewrite old content unless the user explicitly asks for cleanup.
- Avoid duplicate token definitions. If an existing token conflicts with a new recommendation, append a note explaining the conflict instead of silently replacing it.

If `DESIGN.md` does not exist, create it.

## References

For new files or substantial additions, read only the needed reference files in this skill directory:

- `references/SPEC.md` for the `DESIGN.md` format and schema
- `references/BEST_PRACTICES.md` for token naming, Markdown conventions, and examples

## Required Focus

Include design-system information:

- Visual identity and product feel
- Color tokens using hex values
- Typography tokens and usage
- Spacing, layout rhythm, density, and responsive behavior
- Border radius, shape language, elevation, and depth
- Component-level styling rules for common UI controls
- Motion and interaction guidance when relevant
- Accessibility constraints tied to visual design, such as contrast and focus states

## What To Exclude

Exclude:

- Framework choice, service structure, data flow, API contracts, deployment, persistence, or infrastructure; put these in `ARCHITECTURE.md`
- Install commands, usage instructions, contribution guide, or screenshots walkthrough; put these in `README.md`
- Agent workflow, repo-specific test rules, or coding-assistant constraints; put these in `AGENTS.md`
- Generic design theory that does not translate into project-specific decisions

## New File Shape

For a new `DESIGN.md`, follow the local `DESIGN.md` specification:

- Use YAML frontmatter with `version: alpha` and a concise `description`.
- Define exact, machine-readable tokens for colors, typography, spacing, radius, elevation, and components when applicable.
- Use canonical sections from the spec, such as `## Overview`, `## Colors`, `## Typography`, `## Layout & Spacing`, `## Elevation & Depth`, `## Shapes`, `## Components`, and `## Do's and Don'ts`.
- Reference token values in prose with `{path.to.token}` syntax.
- Use hex colors, not RGB/RGBA.
- Keep typography tokens separate from color tokens.

For existing files that do not follow the spec, preserve the old content and append spec-aligned additions. Tell the user if full compliance would require a rewrite.

## Completion

Finish only after `DESIGN.md` exists and contains design-system guidance without architecture, README, or agent-instruction overlap.
