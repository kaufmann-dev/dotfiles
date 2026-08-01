---
name: ui-design-principles
description: Apply context-sensitive UI design guardrails. Use when creating, modifying, or reviewing interfaces. Preserve existing themes; apply personal visual defaults only to greenfield websites and applications or when explicitly requested.
---

# UI Design Principles

Use these principles as guardrails, not as a mandate to redesign. Preserve the existing interaction model, visual language, and information density unless the task or a concrete usability defect requires a change. Do not invent states, flows, components, abstractions, or design-system work unrelated to the request.

Prefer native platform behavior and the smallest change that fully solves the problem.

## Scope and precedence

- Treat a project as established when it already has a visual language, theme, design tokens, shared components, or implemented UI. A new page, feature, or component inside such a project is not greenfield.
- In an established project, follow its present theme and patterns. Do not restyle, audit, or rewrite existing UI to match the personal visual defaults below unless the user explicitly asks to apply them. Even then, limit changes to the requested scope unless the user requests a broader redesign.
- Apply the personal visual defaults when creating a genuinely new website or application without an established visual system. Also apply them when the user explicitly requests them for an existing project.
- Follow explicit product, brand, and user requirements. Preserve accessibility, usability, and correct state communication when applying any visual preference.

## Personal visual defaults

Apply these defaults only within the scope defined above:

1. **Use square geometry** — do not use border radius. Keep surfaces and controls rectangular so adjacent elements can align cleanly without artificial gaps.
2. **Keep surfaces flat** — do not use box shadows. Use borders sparingly and only when a boundary, state, or interaction would otherwise be unclear. Establish separation through page structure, hierarchy, scale, spacing, contrast, and background color. Use a visible outline or another static, non-shadow cue for keyboard focus.
3. **Use absolute base backgrounds** — use `#000000` for a dark main background and `#ffffff` for a light main background.
4. **Use color functionally** — introduce color only when it helps users distinguish hierarchy, categories, states, actions, or groups. Keep the interface monochrome otherwise, and never rely on color alone to convey meaning.
5. **Keep every element purposeful** — omit elements and copy that are purely decorative or add no useful information or action. Avoid eyebrow headings, nonessential disclaimers, meaningless taglines, and stacks of buzzwords. Retain disclosures and guidance required for safe, correct, accessible, or lawful use.
6. **Use motion only for functional feedback** — keep hover, focus, pressed, page, and view state changes immediate. Do not add transitions, parallax, auto-moving content, decorative animation, or other motion that does not communicate useful information. Allow restrained motion when it clearly communicates an active process, such as a loading spinner or progress indicator. Give animated status indicators an accessible name, respect reduced-motion preferences, and prefer a static indicator when motion adds no useful information.
7. **Constrain single-line text** — when text must fit within a bounded component, truncate it with an ellipsis instead of allowing it to overflow, resize the component, or break the surrounding layout. Ensure flex and grid children can shrink as needed. Preserve wrapping where displaying the complete text is the purpose.

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

When reviewing, report only relevant failures. For each one, identify the element, provide concrete evidence of the problem, and recommend the smallest effective fix. Distinguish objective accessibility defects from contextual design preferences. In an established project, do not report departures from the personal visual defaults as failures unless the user asks for an evaluation against those defaults.
