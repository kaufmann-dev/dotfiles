---
name: ui-design-principles
description: Context-sensitive design guardrails for building or reviewing user interfaces. Use this whenever creating, editing, or critiquing frontend UI, or when the user mentions responsive design, interaction states, keyboard navigation, accessibility, visual hierarchy, or component consistency. Preserve the product's intent, established patterns, and appropriate density; do not turn these guardrails into an unrelated redesign.
---

# UI Design Principles

Use these principles as guardrails, not as a mandate to redesign. Preserve the existing interaction model, visual language, and information density unless the task or a concrete usability defect requires a change. Do not invent states, flows, components, abstractions, or design-system work unrelated to the request.

Prefer native platform behavior and the smallest change that fully solves the problem.

## Accessibility

1. **Preserve native keyboard semantics** — use native interactive elements whenever possible. Make every control keyboard-reachable with a visible focus indicator, and support the standard keys for that control: for example, Enter activates links, while Enter and Space activate buttons. Keep focus order aligned with DOM order unless the interface has a deliberate, accessible alternative.
2. **Do not gate functionality by input method** — provide a click, tap, or keyboard path for hover affordances and gestures that require precision or multiple pointers. Allow hover to enhance an interaction without duplicating purely decorative effects.
3. **Do not use color as the only meaningful signal** — pair status and meaning with text, an icon, shape, pattern, or accessible name.
4. **Meet applicable contrast requirements** — target WCAG AA: 4.5:1 for normal text and 3:1 for large text. Provide 3:1 non-text contrast for visual information needed to identify controls, states, or meaningful icons; do not apply this requirement to decorative elements or redundant boundaries.
5. **Size targets for the interaction context** — favor targets around 44px for touch-primary interfaces. Dense pointer-primary interfaces may use smaller visible controls when targets remain at least 24px, have adequate spacing, and are comfortably operable. Separate destructive actions from likely confirmation actions.

## Responsive behavior

6. **Support the product's relevant viewport range** — use mobile-first construction when it fits the product, but preserve desktop-primary density and workflows for dashboards, editors, admin tools, and similar interfaces. Make those interfaces degrade gracefully on smaller screens without restructuring them solely to satisfy a mobile-first pattern.
7. **Choose an explicit overflow behavior when content can exceed its bounds** — wrap, truncate, scroll, paginate, or use an overflow menu according to the content and workflow. Do not add pagination or virtualization without evidence that the expected data scale requires it.

## States & data

8. **Implement states that can actually occur** — cover the reachable default, interaction, disabled, loading, error, and success states relevant to the component's lifecycle. Do not invent state or supporting logic merely to complete a checklist. Make asynchronous feedback timely and errors specific, human-readable, and recoverable.
9. **Handle realistic cardinality** — verify zero, one, typical, and plausible high-volume content according to product constraints. Do not treat all collections as unbounded.
10. **Use an empty state when absence could be confusing** — explain empty data-backed views and offer a next step when one exists. Allow a region to remain visually quiet when its emptiness is already clear or intentional.

## Hierarchy & consistency

11. **Reflect the workflow's actual hierarchy** — emphasize a primary action only when the screen genuinely has one. Keep peer actions visually equal when the workflow does not establish a single dominant choice.
12. **Reuse established patterns before creating new ones** — use shared components and tokens for repeated or system-level decisions. Allow justified component-local values; do not expand or refactor the design system unless the task benefits from it.
13. **Apply progressive disclosure selectively** — move genuinely infrequent or cognitively expensive options behind a secondary layer only when that improves the common workflow. Keep important and frequent functionality visible and preserve discoverability.

When reviewing, report only relevant failures. For each one, identify the element, provide concrete evidence of the problem, and recommend the smallest effective fix. Distinguish objective accessibility defects from contextual design preferences.
