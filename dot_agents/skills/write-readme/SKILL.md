---
name: write-readme
description: Create or update a human-facing project README.md with overview, setup, usage, and navigation.
---

# Write README.md

## Purpose

Create or refresh `README.md` for humans who need to understand, run, use, or contribute to a project.

## Use When

- The user asks for a README.
- Setup, usage, command, or project-navigation information is stale or missing.
- The project docs need a human-friendly entrypoint.

## Do Not Use When

- The user wants agent-only instructions; use `write-agents`.
- The user wants architecture details; use `write-architecture`.
- The user wants design-system guidance; use `write-design`.
- The user wants a full docs setup; use `setup`.

## Document Boundary

| File | Owns |
| --- | --- |
| `README.md` | Human overview, setup, usage, commands, navigation, troubleshooting |
| `AGENTS.md` | Agent-only workflow and repo constraints |
| `ARCHITECTURE.md` | Deep technical structure, data flow, integrations, and deployment shape |
| `DESIGN.md` | Design tokens, visual identity, UI rules, and component styling |

Summarize adjacent docs in one sentence when useful, then link to them.

## Workflow

1. Read the existing README and nearby project docs.
2. Inspect manifests, scripts, configs, and entrypoints for verified setup and commands.
3. Add or repair top navigation when the README is more than a small stub.
4. Replace stale placeholders, broken diagrams, and inaccurate file trees.
5. Keep the README human-facing and avoid agent-only rules.
6. Preserve useful existing content unless the user requested cleanup.

## Suggested Shape

For a new or fully refreshed README, prefer:

```markdown
# Project Name

## Navigation

## Overview

## Quick Start

## Usage

## Development

## Project Docs
```

Adjust headings to match the project. Include Mermaid only when it makes the project easier to understand.

## Output

A README with:

- Clear project purpose
- Setup and prerequisites
- Common commands
- Basic usage
- Links to project docs when they exist
- Honest troubleshooting or unknowns

## Completion Rules

Finish only when `README.md` exists, is accurate from verified facts, and contains no stale placeholders.
