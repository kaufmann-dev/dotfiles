---
name: write-agents
description: Use only when creating AGENTS.md from scratch. Never for editing existing files.
---

# Write AGENTS

The global AGENTS.md covers general workflow. This file covers only what is specific to this project.

## Before Writing
Read: `package.json` / `pyproject.toml` / `Makefile` / CI config.
Derive all commands from these — do not invent.

## Structure

Mirror this layout. Include only sections where you have non-obvious content to add:

```
# Build & Test
<exact install, build, lint, test commands — always include, even if in README, so the agent never has to look them up>

# Tooling
<non-obvious tool choices, e.g. uv not pip, pnpm not npm>

# Conventions
<counterintuitive patterns not inferable from the code>

# Hard Limits
<repo-specific absolutes — phrased as "always X", not "never Y">
```

## Rules
- Include commands the agent needs to execute tasks, even if they appear in README.md. Omit all other content already covered by README.md or inferable from the codebase.
- Phrase all constraints as "always X" — positive framing gets higher compliance than "don't X".
- Leave style rules out — linters enforce those.
- Optimise for signal density, not line count. Every line must change agent behavior — if cutting it would leave the agent acting identically, cut it.
