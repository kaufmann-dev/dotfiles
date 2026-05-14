---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications. Generates creative, polished code and UI design that respects provided design systems or invents striking aesthetics when none are given.
license: Complete terms in LICENSE.txt
---

This skill guides the creation of production-grade frontend interfaces. Implement real working code with exceptional attention to aesthetic details, spatial composition, and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, technical constraints, or a specific DESIGN.md file.

## 1. Guideline Adherence & Design Thinking

Before coding, analyze the context and establish the design rules:
* **Design System First:** If the user provides a DESIGN.md, style guide, or strict constraints, you MUST follow them perfectly. Do not invent colors outside the provided palette. Do not add ornaments, gradients, or shadows if the guide forbids them. Execute the provided vision with absolute precision.
* **Creative Autonomy:** If no strict design system is provided, commit to a BOLD aesthetic direction. Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, high-contrast glassmorphism, editorial, or industrial. What makes this unforgettable?
* **Purpose & Tone:** Understand what problem the interface solves. A B2B utility tool requires a different tone than a creative portfolio.

## 2. Frontend Aesthetics Guidelines

Apply these principles appropriately based on the chosen or provided aesthetic:

* **Typography:** If a design guide exists, use its exact font stack and scaling rules. If inventing an aesthetic, avoid default fonts. Opt instead for distinctive choices that elevate the design. Pair a characterful display font with a highly legible body font.
* **Color & Theme:** Commit to a cohesive aesthetic using CSS variables. If inventing a palette, favor dominant colors with sharp accents over timid, evenly distributed colors. Ensure high accessibility and contrast.
* **Motion:** Use animations purposefully. Minimalist utilitarian designs need zero to minimal motion. Expressive designs should utilize staggered reveals, scroll-triggering, and surprising hover states. Prioritize CSS-only solutions for HTML.
* **Spatial Composition:** Match the layout to the tone. Use unexpected layouts, asymmetry, and grid-breaking elements for creative projects. Use strict 12-column grids, generous whitespace, and predictable hierarchy for neutral or utility projects.
* **Visual Details:** Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with gradient meshes, noise textures, and deep shadows. Minimalist designs require extreme restraint, relying entirely on typography scale, negative space, and 1px borders.

CRITICAL: Elegance comes from executing the vision well. Never default to generic, uninspired layouts unless explicitly instructed to build a standard template. Make unexpected choices that feel genuinely designed for the specific context.