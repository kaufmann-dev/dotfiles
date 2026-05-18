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
```
# Build & Test
<exact commands to install, build, lint, test>

# Tooling
<non-obvious tool choices, e.g. uv not pip>

# Conventions
<counterintuitive patterns not inferable from the code>

# Hard Limits
<things never to do in this repo>
```

## Rules
- Omit any section where you have nothing non-obvious to say.
- Do not repeat what is in README.md or discoverable by reading the code.
- No style rules — linters handle those.
- Keep it under 60 lines.