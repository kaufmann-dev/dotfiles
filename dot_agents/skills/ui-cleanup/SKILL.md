---
name: ui-cleanup
description: Clean up duplicated and inconsistent frontend UI without redesigning or changing behavior. Use only when the user explicitly invokes this skill.
---

# UI Cleanup

Clean up a frontend that was built quickly or iteratively. Consolidate duplicated presentation patterns, finish use of the existing component system, and make screens feel coherent without changing product behavior or inventing a new design direction.

## Scope Guardrails

- Use this skill only after explicit user invocation. If this skill was loaded without that, stop applying it and follow the ordinary task instructions.
- Treat the task as cleanup, not a redesign or rewrite.
- Preserve user-visible functionality, routes, data flow, labels, copy, accessibility semantics, public APIs, and event behavior unless a small structural change is required to centralize equivalent UI.
- Use the codebase's existing design language. Do not add a dependency, replace the design system, create a new theme, or invent new token scales.
- Keep changes surgical. Delete redundant code only after all relevant usages are migrated.

## Audit First

Do not edit until the repeated or inconsistent UI patterns are concrete enough to name.

1. Read project docs and top-level config to identify the frontend framework, styling system, component directories, test commands, and visual verification path.
2. Map UI surfaces: shared components, page or route files, layouts, style files, theme or token files, stories, and tests.
3. Inventory existing primitives and variants for buttons, inputs, cards, lists, tables, navigation, headers, footers, dialogs, toasts, empty states, loading states, and error states.
4. Search for duplicated markup, class strings, inline styles, ad hoc constants, one-off wrappers, and component-like patterns implemented both as components and raw markup.
5. Rank findings by blast radius: shared primitives first, layout/navigation next, recurring page patterns next, rare local inconsistencies last.

## Consolidation Rules

- Prefer an existing component, helper, utility class, token, or theme value as the source of truth.
- If no source of truth exists, extract the smallest reusable component or utility that covers the repeated semantic pattern.
- Consolidate patterns that have the same role and behavior. Avoid abstractions for merely coincidental markup repetition when extraction would add complexity without improving consistency.
- Replace raw markup, inline styles, duplicated class strings, and local constants with the shared source of truth everywhere the same UI pattern appears.
- Support existing meaningful variants with explicit props, class composition, or documented token choices. Do not preserve accidental visual drift as a variant.
- Keep ownership local when repetition is confined to one feature area. Promote to shared components only for cross-feature or app-wide patterns.
- Remove unused components, styles, helpers, imports, and tests after migration.

## Visual Consistency Rules

- Normalize spacing, padding, typography, color, border, radius, shadow, focus, hover, active, selected, and disabled states by reusing established project tokens, classes, or variants.
- If existing patterns conflict, choose the documented pattern first, then the most-used shared component or token, then the simplest local pattern that already appears consistently.
- Make headers, footers, sidebars, navigation, forms, cards, lists, data displays, empty states, loading states, and error states follow the same structural logic where they serve the same purpose.
- Preserve intentional hierarchy and context-specific emphasis. Do not flatten all screens into identical layouts just for uniformity.
- Treat responsiveness as part of visual coherence. After consolidation, check that changed layouts do not overlap, clip, or shift unexpectedly at relevant breakpoints.

## Execution Order

1. Establish the source of truth for shared primitives and tokens.
2. Migrate repeated usages to existing or newly extracted components.
3. Normalize app-wide layout and navigation patterns.
4. Align recurring empty, loading, error, form, list, card, and data-display patterns.
5. Clean rare local inconsistencies only when they are clearly related to the same system.
6. Delete redundant code and update tests, stories, or snapshots that describe the changed presentation.

For large codebases, work in small batches and verify after each meaningful batch instead of waiting until the end.

## Verification

- Run the relevant formatter, linter, typecheck, unit tests, component tests, or build command available in the repo.
- For rendered UI changes in a runnable app, start the dev server and inspect affected screens with browser automation at desktop and mobile widths. Capture screenshots when useful for comparison.
- Review the diff for behavior changes, new dependencies, broad rewrites, unused code, and accidental design decisions.
- If root documentation files exist, update them when the cleanup changes setup, public usage, tooling, conventions, or visual design decisions.
- In the final response, report the main audit themes, the consolidation work completed, verification performed, and any known residual risk.

## Stop And Ask Before

- Changing product direction, information architecture, content strategy, or brand identity.
- Adding, removing, or reinterpreting user-facing functionality.
- Replacing the styling system, component library, or theme architecture.
- Adding dependencies or large generated assets.
- Applying a broad restyle without an established source of truth in the codebase.
- Deleting a component or style module whose ownership or active usage is unclear.
