---
name: write-agents
description: Create or append to a project AGENTS.md with concise, repo-specific operating instructions for coding agents. Use when the user asks to generate, improve, or refresh AGENTS.md, agent instructions, Codex/OpenCode guidance, or repository AI-assistant context while keeping README.md, ARCHITECTURE.md, and DESIGN.md as the sources for human docs, technical architecture, and design system details.
---

# Write AGENTS.md

Create or update `AGENTS.md` for the repository. The file is for future coding agents, not for end users.

## Document Boundaries

Keep the four project docs distinct:

| File | Owns | Do not duplicate |
| --- | --- | --- |
| `DESIGN.md` | Visual identity, design tokens, UI component styling, interaction feel | Tech stack, commands, agent workflow |
| `ARCHITECTURE.md` | Technology stack, system structure, data flow, integrations, runtime topology | Design tokens, user onboarding, agent behavior |
| `README.md` | Human-facing overview, top navigation, setup, usage, common development commands | Deep architecture, design system specs, agent-only rules |
| `AGENTS.md` | Agent-specific repo guidance that prevents mistakes during automated work | Product overview, architecture reference material, design specs |

If a useful fact belongs in another file, link to that file instead of copying the content into `AGENTS.md`.

## Preservation Rule

If `AGENTS.md` already exists:

- Read the full file before editing.
- Preserve existing content.
- Append missing guidance under a clear section such as `## Agent Notes` or the nearest existing relevant heading.
- Do not delete or rewrite old content unless the user explicitly asks for cleanup.
- Avoid adding duplicate bullets; append only genuinely missing or corrected information.

If `AGENTS.md` does not exist, create a compact file from verified repository facts.

## Investigation

Read high-value sources first:

- `README.md`, `ARCHITECTURE.md`, and `DESIGN.md`
- Root manifests, workspace config, lockfiles, and task runner files
- Build, test, lint, formatter, typecheck, codegen, and package manager config
- CI workflows and pre-commit config
- Existing instruction files such as `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.cursorrules`, `.github/copilot-instructions.md`
- Repo-local agent config such as `opencode.json` or `.codex/`

If behavior is still unclear, inspect a small number of representative source files: entrypoints, package boundaries, generated-code boundaries, and tests. Prefer executable sources of truth over prose.

## What To Include

Include only high-signal, repo-specific guidance an agent would otherwise guess wrong:

- Exact commands for install, build, lint, typecheck, test, and focused tests
- Required command order when order matters
- Package manager and workspace boundaries
- Generated files, migrations, codegen, fixtures, snapshots, or other "do not edit by hand" areas
- Required services, environment files, secrets handling, or local setup gotchas
- Testing quirks, expensive suites, flaky tests, and safe focused verification paths
- Repo-specific style or workflow conventions that differ from defaults
- How agents should consult `README.md`, `ARCHITECTURE.md`, and `DESIGN.md` before making changes

## What To Exclude

Exclude anything better owned elsewhere:

- Product pitch, feature overview, or user onboarding: put this in `README.md`
- Technology stack, component architecture, data model, API contracts, deployment topology: put this in `ARCHITECTURE.md`
- Colors, typography, spacing, visual components, UI mood, design tokens: put this in `DESIGN.md`
- Generic coding advice, exhaustive tutorials, large file trees, or unverifiable guesses

When in doubt, omit or link to the owning file.

## Writing Style

- Keep sections short and practical.
- Prefer bullets over prose.
- Use exact commands in fenced code blocks only when multiple commands must be copied together; otherwise use inline code.
- State assumptions and unknowns explicitly.
- If a repo is small, keep `AGENTS.md` small.

## Completion

Finish only after `AGENTS.md` exists and either:

- Contains the appended agent guidance, or
- Already contained everything needed and no edit was necessary.
