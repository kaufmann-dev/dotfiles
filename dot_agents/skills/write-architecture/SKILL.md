---
name: write-architecture
description: "Use this skill when the user asks to create, improve, refresh, or audit a project ARCHITECTURE.md covering stack, system structure, data flow, persistence, integrations, runtime/deployment shape, security boundaries, or technical tradeoffs."
---

# Write ARCHITECTURE.md

## Purpose

Create or refresh `ARCHITECTURE.md` as the technical source of truth for how a project is built and how its parts fit together.

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
