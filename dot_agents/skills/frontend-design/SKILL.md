---
name: frontend-design
description: Build or improve frontend interfaces with strong visual quality and project-appropriate design.
---

# Frontend Design

## Purpose

Create production-quality frontend interfaces that feel intentionally designed for the project, audience, and workflow.

## Use When

- The user asks to build a web page, component, app screen, poster, artifact, or interactive UI.
- A frontend implementation needs visual polish, layout decisions, or component styling.
- The project has a `DESIGN.md` or visual system that must be followed.

## Do Not Use When

- The task is backend-only, documentation-only, or pure refactoring.
- The user asks only for architecture or planning.
- The requested output is a generated bitmap image rather than frontend code.

## Rules

- If a `DESIGN.md`, style guide, or existing design system exists, follow it exactly.
- If no design system exists, choose a clear aesthetic direction instead of generic defaults.
- Match the product domain: operational tools should be dense and restrained; games and creative work can be more expressive.
- Build the actual usable experience first, not a marketing landing page, unless the user asked for one.
- Avoid decorative clutter that does not serve the interface.
- Verify responsive layout and text fit across relevant viewports.

## Workflow

1. Inspect the existing frontend stack, components, styles, routes, and design docs.
2. Identify the primary user workflow and the first screen the user should see.
3. Make scoped UI changes using existing components and conventions where possible.
4. Add or adjust states users naturally expect: loading, empty, active, disabled, error, and success when relevant.
5. Run the project's build, lint, tests, or typecheck as appropriate.
6. Use browser automation or screenshots for visual verification when a runnable UI is available.

## Output

Deliver working frontend code with:

- Clear information hierarchy
- Responsive layout
- Accessible controls and focus states
- Consistent spacing, color, typography, and icon use
- Verification notes

## Completion Rules

Finish only after implementation and visual verification are complete, or after explaining why the UI could not be run locally.
