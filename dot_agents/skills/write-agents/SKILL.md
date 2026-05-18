---
name: write-agents
description: Create or update a project AGENTS.md with concise, repo-specific operating instructions for coding agents.
---

# Write AGENTS.md

## Purpose

Create or refresh `AGENTS.md` for coding agents. The file should prevent likely mistakes during automated work in the target repository.

## Use When

- The user asks for agent instructions, Codex/OpenCode guidance, or `AGENTS.md`.
- Repo-specific commands, constraints, generated-file rules, or workflow gotchas need to be documented.
- A project has human docs but lacks clear agent operating rules.

## Do Not Use When

- The user wants human onboarding; use `write-readme`.
- The user wants stack or system architecture; use `write-architecture`.
- The user wants visual design guidance; use `write-design`.
- The user wants the global dotfiles workflow updated; edit this repo's root `AGENTS.md` directly with the global scope in mind.

## Document Boundary

| File | Owns |
| --- | --- |
| `AGENTS.md` | Agent-only repo instructions, exact commands, verification paths, generated-file warnings, local workflow constraints |
| `README.md` | Human overview, setup, usage, and contribution entrypoints |
| `ARCHITECTURE.md` | Technical structure, runtime topology, data flow, integrations, and tradeoffs |
| `DESIGN.md` | Visual identity, tokens, components, and interaction guidance |

Link to the owning file instead of copying long reference material.

## Workflow

1. Read existing `AGENTS.md` and nearby instruction files.
2. Inspect README, architecture/design docs, manifests, task runner config, tests, CI, and generated-code boundaries.
3. Include only repo-specific guidance an agent would otherwise guess wrong.
4. Document exact commands for install, build, lint, typecheck, tests, and focused verification when known.
5. State unknowns explicitly instead of inventing commands.
6. Keep the file compact and practical.

## Output

An `AGENTS.md` with:

- Project-specific operating rules
- Commands and verification paths
- Tool or skill usage notes when relevant
- Files or directories agents should avoid editing by hand
- Open questions only when needed

## Completion Rules

Finish only when `AGENTS.md` exists and reflects verified project facts. Do not add generic coding advice unless it prevents a real repo-specific mistake.
