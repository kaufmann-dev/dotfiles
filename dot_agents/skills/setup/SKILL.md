---
name: setup
description: Coordinate project documentation setup across DESIGN.md, ARCHITECTURE.md, README.md, and AGENTS.md.
---

# Setup Project Docs

## Purpose

Create or refresh the standard project documentation set so the files work together without duplicating each other.

Project-scope documents:

- `DESIGN.md`: visual identity, design tokens, components, and interaction feel
- `ARCHITECTURE.md`: stack, system structure, data flow, integrations, and tradeoffs
- `README.md`: human overview, setup, usage, and navigation
- `AGENTS.md`: repo-specific instructions for coding agents

## Use When

- The user asks to set up project docs.
- The user asks to create or refresh several of the standard docs together.
- Existing docs contradict each other and need a coordinated pass.

## Do Not Use When

- The user asks for only one document; use the matching `write-*` skill.
- The target is this global dotfiles repo and the user only wants root `README.md` or `AGENTS.md`.
- The user is asking for product ideation; use `brainstorm`.

## Workflow

1. Inventory existing docs, manifests, source entrypoints, tests, and config.
2. Decide which of the four docs exist and which are missing.
3. Load and apply the dedicated skills in this order:
   - `write-design`
   - `write-architecture`
   - `write-readme`
   - `write-agents`
4. Keep each fact in its owning document and link instead of duplicating.
5. Preserve existing useful content unless the user requested cleanup.
6. Verify the docs exist, agree with each other, and contain no stale placeholders.

## Output

Report:

- Which docs were created or updated
- Any important assumptions
- Any open questions that remain in the docs
- Verification performed

## Completion Rules

Finish only when the requested project docs are coherent as a set, or when a blocker is clearly stated. Do not create root `ARCHITECTURE.md` or `DESIGN.md` in this global dotfiles repo unless the user explicitly changes that scope.
