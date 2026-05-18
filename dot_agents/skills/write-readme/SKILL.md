---
name: write-readme
description: Create or append to a simple human-facing README.md with top navigation, clear setup and usage instructions, and links to DESIGN.md, ARCHITECTURE.md, and AGENTS.md instead of duplicating their contents. Use when the user asks to generate, improve, correct, or refresh a project README.
---

# Write README.md

Create or update `README.md` for humans who want to understand, run, use, or contribute to the project.

## Document Boundaries

Keep the four project docs distinct:

| File | Owns | README behavior |
| --- | --- | --- |
| `README.md` | Human overview, navigation, setup, usage, common commands, contribution entrypoints | Write this file |
| `ARCHITECTURE.md` | Technology stack, components, data flow, integrations, deployment architecture | Link to it for details |
| `DESIGN.md` | Design tokens, visual identity, UI component styling | Link to it for details |
| `AGENTS.md` | Agent-only operating instructions | Link to it only when useful for contributors using agents |

Do not copy architecture or design-system reference material into `README.md`. Summarize in one sentence at most, then link.

## Preservation Rule

If `README.md` already exists:

- Read the full file before editing.
- Preserve existing content.
- Insert a compact navigation block near the top if it is missing. This is the only preferred non-append placement because navigation belongs at the top.
- Append missing sections or corrections under existing relevant headings or at the end.
- Do not delete or rewrite old content unless the user explicitly asks for cleanup.
- Avoid duplicate sections and duplicate commands.

If `README.md` does not exist, create it.

## Required Shape

Keep the README simple. Prefer this structure for new files:

```markdown
# Project Name

## Navigation

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Project Docs](#project-docs)

## Overview

## Quick Start

## Usage

## Development

## Project Docs
```

Adjust section names to fit the project, but always include top navigation unless the file is intentionally tiny.

## What To Include

Include human-facing information:

- What the project is and who it is for
- Current status when obvious, such as prototype, library, app, or production service
- Prerequisites and supported runtime versions
- Install, run, test, build, and lint commands that a human needs
- Configuration and environment variables, without secrets
- Basic usage examples or screenshots when already available
- Links to `ARCHITECTURE.md`, `DESIGN.md`, and `AGENTS.md` if those files exist or are being created
- Troubleshooting notes for common setup failures

## What To Exclude

Exclude:

- Deep component diagrams, data models, endpoint inventories, deployment topology, or stack tradeoffs; put those in `ARCHITECTURE.md`
- Design tokens, palettes, typography scales, visual rules, or component styling specs; put those in `DESIGN.md`
- Agent-only tool rules, coding-agent workflow, or repository-specific automation instructions; put those in `AGENTS.md`
- Marketing filler, long tutorials, speculative roadmap, or generic open-source boilerplate

## Diagrams

Use Mermaid when a diagram makes the README clearer. Keep diagrams small and human-oriented, such as a simple workflow or user journey. Put technical system diagrams in `ARCHITECTURE.md`.

## Completion

Finish only after `README.md` exists, has top navigation when appropriate, and preserves any existing content.
