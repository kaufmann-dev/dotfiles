---
name: ui-design-principles
description: Design principles for building or reviewing user interfaces. Use this whenever creating, editing, or critiquing any frontend UI — components, screens, layouts, or design systems — or when the user mentions responsive or mobile-first design, hover states, touch targets, empty / loading / error states, keyboard navigation, color contrast, accessibility, visual hierarchy, or component consistency. Apply these as defaults when generating UI, even if the user does not explicitly ask for a design review.
---

# UI Design Principles

Defaults for building interfaces that are accessible, responsive, and complete. Apply them as you build, and use them as a checklist when reviewing existing UI.

Two kinds of rules: **hard rules** (accessibility, states) have an objective bar — hold them unless there's a stated reason not to. **Defaults** (mobile-first, progressive disclosure) are strong starting points a clear product context can override. When a rule forbids something, prefer "do X instead of Y" over a bare "never Y."

## Responsive

1. **Default to mobile-first** — design the small screen first, then enhance for larger viewports. Exception: explicitly desktop-primary products (dashboards, IDEs, admin tools), which should still degrade gracefully on small screens.
2. **Don't rely on input that may be absent** — no hover-only actions, no two-handed or high-precision gestures without a simple single-pointer alternative.

## Accessibility (hard bar)

3. **Keyboard-operable** — every interactive element works with Tab / Enter / Space and shows a visible focus indicator. Focus order follows DOM order.
4. **Hover is never the only path** — every hover affordance also has a tap, click, or focus equivalent. Hover may enhance, never gate.
5. **Color is never the only signal** — back it with text, an icon, or a label.
6. **Contrast** — at least 4.5:1 for body text, 3:1 for large text, icons, and control borders.
7. **Target size** — interactive targets at least ~44px (24px is the absolute floor); space destructive actions away from confirming ones.

## States & data

8. **Design every state** — default, hover, focus, active, disabled, loading, error, success. Loading confirms input registered; error messages are human, specific, and tell the user how to recover.
9. **Handle zero, one, and unbounded items** — pick an explicit overflow strategy (truncate, wrap, scroll, paginate, or overflow menu). A component that only looks right with 3–5 items is unfinished.
10. **Always design a real empty state** — never a blank screen; confirm nothing is wrong and point to the next action.

## Hierarchy & consistency

11. **One clear hierarchy per screen** — the primary action is unmistakably dominant via size, weight, color, and spacing.
12. **Use shared tokens** for color, type, spacing, and motion — never hardcode values. Reuse existing components and patterns before inventing new ones.
13. **Progressive disclosure** — show the common path simply; tuck advanced options behind a secondary layer rather than removing them.

When reviewing, report each failure with the element, what's wrong, the rule it breaks, and the concrete fix.