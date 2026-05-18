---
name: write-architecture
description: Create or append to ARCHITECTURE.md with only the application technology stack and technical architecture: components, data flow, integrations, runtime topology, and key tradeoffs. Use when the user asks to generate, improve, correct, or refresh architecture docs without mixing in README, DESIGN.md, roadmap, planning, or agent-instruction content.
---

# Write ARCHITECTURE.md

Create or update `ARCHITECTURE.md` as the technical source of truth for how the application is built and how its parts fit together.

## Document Boundaries

Keep the four project docs distinct:

| File | Owns | Architecture behavior |
| --- | --- | --- |
| `ARCHITECTURE.md` | Technology stack, components, data flow, integrations, runtime topology, persistence, deployment shape, technical tradeoffs | Write this file |
| `README.md` | Human overview, setup, usage, contribution entrypoints | Link to it; do not duplicate onboarding |
| `DESIGN.md` | Design tokens, visual system, UI component styling | Mention only if the frontend consumes it |
| `AGENTS.md` | Agent-only workflow and repo instructions | Do not include |

Do not mention extra planning documents unless they actually exist in the project.

## Preservation Rule

If `ARCHITECTURE.md` already exists:

- Read the full file before editing.
- Preserve existing content.
- Append missing or corrected architecture information under existing relevant headings or a new `## Architecture Notes` section.
- Do not delete or rewrite old content unless the user explicitly asks for cleanup.
- Avoid duplicate component lists, duplicate stack tables, and stale guesses.

If `ARCHITECTURE.md` does not exist, create it from verified project facts.

## Investigation

Use executable and structural sources first:

- Package manifests, lockfiles, workspace config, framework config, Docker/compose files, deployment config
- Source entrypoints, route definitions, server startup files, client bootstrap files
- Database schema, migrations, ORM config, API clients, queue/event config
- CI and build scripts when they reveal runtime or deployment assumptions
- Existing `README.md` for human context only
- Existing `DESIGN.md` only to note design-system consumption, not visual details

If the project is empty or the architecture cannot be verified, do not invent details. Ask for the intended stack or write an `Open Questions` section.

## What To Include

Include technical architecture only:

- Stack summary with each major technology and why it is used
- Runtime topology: app/server/client/workers/jobs/services
- Component responsibilities and boundaries
- Data flow and state ownership
- Persistence layer, storage, cache, queues, and external integrations
- API/interface contracts at the level needed to understand component communication
- Authentication, authorization, secrets, and trust boundaries
- Build, deployment, and environment shape when architecturally relevant
- Important constraints, tradeoffs, risks, and open architecture questions

## What To Exclude

Exclude:

- User-facing setup or usage instructions; put them in `README.md`
- Visual design tokens or UI style guidance; put them in `DESIGN.md`
- Agent workflow, exact test commands, or coding-assistant behavior; put them in `AGENTS.md`
- Product roadmap, feature backlog, implementation task plan, sprint plan, or speculative future architecture
- Exhaustive endpoint or schema dumps unless they are the simplest way to explain the architecture

## Suggested Structure

For a new file, use this shape and omit sections that do not apply:

```markdown
# Architecture

## Overview

## Technology Stack

| Layer | Choice | Purpose |
| --- | --- | --- |

## System Components

| Component | Responsibility | Notes |
| --- | --- | --- |

## Data Flow

## Data & State

## Interfaces & Integrations

## Runtime & Deployment

## Security & Trust Boundaries

## Tradeoffs

## Open Questions
```

Use Mermaid for system or data-flow diagrams when it clarifies architecture. Keep diagrams technical and current.

## Completion

Finish only after `ARCHITECTURE.md` exists and contains verified architecture information or clearly marked open questions.
