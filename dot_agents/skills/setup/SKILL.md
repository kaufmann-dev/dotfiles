---
name: setup
description: Initialize or refresh a project's core documentation by coordinating write-design, write-architecture, write-readme, and write-agents. Use when the user asks to set up project docs, create the standard DESIGN.md/ARCHITECTURE.md/README.md/AGENTS.md files, or make those docs work together for an empty or existing project.
---

# Setup Project Docs

Set up the four standard project documents so they work together without overlap:

- `DESIGN.md`: design system and visual identity
- `ARCHITECTURE.md`: technology stack and application architecture
- `README.md`: human-facing navigation, setup, and usage
- `AGENTS.md`: agent-only repo instructions not already covered elsewhere

## Core Rule

Use the dedicated write skills for the actual document work:

1. Use `write-design` for `DESIGN.md`.
2. Use `write-architecture` for `ARCHITECTURE.md`.
3. Use `write-readme` for `README.md`.
4. Use `write-agents` for `AGENTS.md`.

Load those four skill instructions before editing files. If the runtime does not automatically load named skills, find the sibling skill folders and read their `SKILL.md` files directly. Run them in that order so later docs can link to earlier sources instead of duplicating them.

## Preservation Rule

For existing projects:

- Read any existing `DESIGN.md`, `ARCHITECTURE.md`, `README.md`, and `AGENTS.md`.
- Preserve existing content in each file.
- Append missing information or non-destructively insert README navigation at the top if needed.
- Do not delete or rewrite old content unless the user explicitly asks for cleanup.
- Avoid copying the same information between files; link to the owning file instead.

For projects with no matching docs, create the missing files.

## Empty Projects

If the project has no source files and no clear product or stack context:

- Do not invent a detailed architecture or design system.
- Ask one concise batch of questions if the user is available: project purpose, intended stack, and desired design direction.
- If the user asked to proceed without questions, create minimal starter docs with clear `Open Questions` sections.
- Keep placeholders honest and easy to replace.

## Existing Projects Without Docs

If source files exist but the four docs do not:

- Infer only what can be verified from manifests, config, source entrypoints, and tests.
- Create each document with the appropriate scope.
- Put unknowns in the owning file's `Open Questions` section.
- Prefer links over duplicated summaries.

## Existing Projects With Some Docs

If only some docs exist:

- Read existing docs first to learn naming and project intent.
- Create missing docs from verified facts.
- Append cross-links to existing docs where useful.
- Do not move content between files unless the user explicitly asks; instead, add a note in the correct file and link to the old location if needed.

## Setup Workflow

1. Inventory the repository: docs, manifests, configs, source entrypoints, tests, and CI.
2. Decide whether the project is empty, existing without docs, or existing with partial docs.
3. Establish document ownership using the four-file boundary.
4. Apply `write-design`, `write-architecture`, `write-readme`, and `write-agents` in order.
5. Verify each file exists and preserves previous content.
6. Report created files, appended sections, and any open questions.

## Completion

Finish only after all four files either exist or the user has explicitly declined one. The final report should name the changed files and call out any information that remained unknown.
