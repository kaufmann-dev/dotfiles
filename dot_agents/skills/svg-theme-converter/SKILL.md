---
name: svg-theme-converter
description: Convert a standard SVG icon into a self-theming SVG that adapts to light and dark mode via an embedded CSS prefers-color-scheme media query. Handles fill-based and stroke-based icons with any number of shapes. Use only when the user explicitly invokes this skill or asks to make an SVG icon theme-aware / dark-mode aware.
---

# SVG Theme Converter

Convert a standard SVG icon into a **self-theming** SVG: one file that renders in
a light color in light mode and a light color in dark mode, with no external
stylesheet or JavaScript. Theming is driven entirely by an embedded `<style>`
block with a `prefers-color-scheme: dark` media query.

This is for **standalone** SVGs — favicons, README images, files opened directly,
or icons embedded via `<img>`/`<object>` — where no host page CSS applies. For an
icon inlined in HTML and themed by the page, prefer `currentColor` (see
*Alternative* below) instead of this skill.

## Scope Guardrails

- Use this skill only after explicit user invocation. If it was loaded without
  that, stop applying it and follow the ordinary task instructions.
- Preserve the icon's geometry exactly. The output must render identically to the
  original in light mode — same shapes, same `viewBox`, same size.
- Never invent or drop shapes. Convert only color paint; leave everything else.

## Core Technique

Do **not** tag a single element with an `id`. Instead, set the paint property on
the **`<svg>` root** via embedded CSS and let SVG inheritance cascade it to every
child shape. This works for any number of `<path>` and shape elements with no
per-element edits beyond stripping their hardcoded colors.

- **Fill icons** (solid glyphs): theme the `fill` property.
- **Stroke icons** (outline glyphs — Lucide, Feather, Tabler; usually have
  `fill="none"` and a `stroke` color): theme the `stroke` property.
- **Mixed icons** (both filled and stroked parts): theme both `fill` and
  `stroke`.

## Procedure

1. **Detect the icon type.** If shapes carry a `stroke` color and/or the `<svg>`
   has `fill="none"`, treat it as a stroke icon. Otherwise treat it as a fill
   icon. If it has both colored fills and colored strokes, theme both properties.

2. **Strip color paint only.** Remove color paint declarations from the `<svg>`
   and every shape (`path`, `circle`, `rect`, `line`, `polygon`, `polyline`,
   `ellipse`, `g`): `fill="#..."`, `fill="black"`, `stroke="#..."`, and any
   `fill`/`stroke` inside an inline `style="..."`. **Do not remove:**
   - `fill="none"` — it is structural for stroke icons, not a color.
   - geometry attributes — `d`, `cx`, `cy`, `r`, `x`, `y`, `width`, `height`,
     `points`, etc.
   - stroke-shape attributes — `stroke-width`, `stroke-linecap`,
     `stroke-linejoin`, `stroke-dasharray`.
   - `xmlns`, `viewBox`, and the root `width`/`height`.

3. **Insert one `<style>` block** as the first child of `<svg>`.

4. **Set light then dark.** Set the default (light) color on the `svg` selector,
   then override it inside `@media (prefers-color-scheme: dark)`.

5. **Colors.** Default to light `#000000` and dark `#ffffff`. These are defaults —
   if the user names specific light/dark colors, use those instead.

## Templates

Fill icon:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <style>
    svg { fill: #000000; }
    @media (prefers-color-scheme: dark) { svg { fill: #ffffff; } }
  </style>
  <path d="..." />
</svg>
```

Stroke icon (note the preserved `fill="none"` and stroke-shape attributes):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <style>
    svg { stroke: #000000; }
    @media (prefers-color-scheme: dark) { svg { stroke: #ffffff; } }
  </style>
  <path d="..." />
  <circle cx="12" cy="12" r="3" />
</svg>
```

Mixed icon — theme both properties:

```xml
<style>
  svg { fill: #000000; stroke: #000000; }
  @media (prefers-color-scheme: dark) { svg { fill: #ffffff; stroke: #ffffff; } }
</style>
```

## Alternative: currentColor

When the icon is inlined directly in HTML and you want it to follow the host
page's text color, skip the embedded media query. Instead set the paint to
`currentColor` (`fill="currentColor"` or `stroke="currentColor"`) and let the
surrounding CSS `color` drive it. Use the embedded-media-query approach in this
skill only for standalone SVGs where no host stylesheet is in effect.

## Validation Checklist

Before finishing, confirm:

- Output is well-formed SVG (`xmlns="http://www.w3.org/2000/svg"`, balanced tags).
- Light-mode rendering is identical to the original — no shapes added or lost,
  geometry unchanged.
- Every previously colored element now inherits color from the root (no leftover
  hardcoded `fill`/`stroke` colors override the cascade).
- `fill="none"` and stroke-shape attributes are intact on stroke icons.
- The icon recolors when the color scheme switches (verify by opening the file
  and toggling the OS/browser dark mode).
