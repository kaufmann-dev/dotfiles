---
name: create-design-md
description: Generates a project-agnostic DESIGN.md file based on a specific visual identity, strictly adhering to the @google/design.md specification. Use this skill whenever you need to document a design system, visual identity, or create a DESIGN.md file.
---

# Create DESIGN.md

You are an expert at creating `DESIGN.md` files that comply with the official `@google/design.md` specification. Your goal is to translate a desired visual identity or design description into a robust, machine-readable, and human-friendly `DESIGN.md`.

## Instructions

When the user asks you to create or generate a `DESIGN.md` file, you must follow these steps:

1. **Understand the Requirements**: Analyze the user's design requirements, color preferences, and typography choices.
2. **Review Specifications**: 
   - Read [the official specification](references/SPEC.md) for the format details and schemas.
   - Read [the best practices](references/BEST_PRACTICES.md) for conventions, naming schemas, and Markdown formatting.
3. **Draft the YAML Front Matter**:
   - Include `version: alpha` and a `description`.
   - Define exact, machine-readable tokens for `colors` (hex only), `typography`, `rounded`, `spacing`, and `components`.
   - Ensure all dimension values include exact units (e.g., `px`, `rem`) and avoid dual notations.
4. **Draft the Markdown Prose**:
   - Use strictly the canonical section headers: `## Overview`, `## Colors`, `## Typography`, `## Layout & Spacing`, `## Elevation & Depth`, `## Shapes`, `## Components`, `## Do's and Don'ts`.
   - Bind design values in the text to tokens using `{path.to.token}` syntax (e.g., `{colors.primary}`, `{rounded.sm}`).
5. **Final Output**: Present the generated `DESIGN.md` content clearly to the user.

## Key Rules
- **No RGB/RGBA**: Colors must be hex.
- **Semantic Naming**: Use role-based names (`primary`, `surface`, `headline-xl`); avoid generic HTML element names (e.g., `h1`).
- **Token References**: Hardcoded values in prose must be replaced with `{token}` references.
- **Section Order**: Sections must appear exactly in the defined order. Do not number the headers.
- **No Color in Typography**: Typography tokens must not contain a `color` property.

For edge cases or detailed examples, always refer to the reference files included in this skill directory.
