---
name: write-architecture
description: Create or update ARCHITECTURE.md with project technology, system structure, data flow, integrations, and tradeoffs.
---

# Write ARCHITECTURE.md

## Purpose

Create or refresh `ARCHITECTURE.md` as the technical source of truth for how a project is built and how its parts fit together.

## Use When

- The user asks for architecture documentation.
- The stack, runtime topology, data flow, integrations, or technical boundaries need to be explained.
- Existing architecture docs are missing, stale, or contradictory.

## Do Not Use When

- The user wants setup or usage docs; use `write-readme`.
- The user wants agent workflow instructions; use `write-agents`.
- The user wants visual design guidance; use `write-design`.
- The target is this global dotfiles repo and the user did not explicitly request project-scope architecture docs.

## Document Boundary

| File | Owns |
| --- | --- |
| `ARCHITECTURE.md` | Stack, components, data flow, persistence, integrations, runtime/deployment shape, tradeoffs |
| `README.md` | Human setup, usage, and navigation |
| `AGENTS.md` | Agent-specific commands, constraints, and workflow rules |
| `DESIGN.md` | Visual identity, design tokens, and UI styling guidance |

## Workflow

1. Inspect manifests, framework config, source entrypoints, route definitions, services, schemas, tests, CI, and deployment config.
2. Use executable sources of truth over prose.
3. Document verified architecture only.
4. Explain component responsibilities and boundaries at the level needed for future engineering work.
5. Capture unknowns in `Open Questions` instead of inventing details.
6. Link to README or DESIGN.md for non-architecture details.

## Suggested Shape

```markdown
# Architecture

## Overview

## Technology Stack

## System Components

## Data Flow

## Data and State

## Interfaces and Integrations

## Runtime and Deployment

## Security and Trust Boundaries

## Tradeoffs

## Open Questions
```

Omit sections that do not apply.

## Output

An `ARCHITECTURE.md` that describes verified technical structure, important constraints, and open technical questions.

## Completion Rules

Finish only when architecture facts are grounded in the repository or clearly marked as assumptions/open questions.
