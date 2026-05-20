---
name: add-subagents
description: Add or update project-scoped subagent definitions across multiple agent tools. Use when a user asks to install, add, change, or synchronize subagents for multiple agent tools.
---

# Add Subagents

Install subagents into project-scoped configuration when the harness supports it. Do not edit user-global subagent configuration unless the user explicitly asks for global setup.

Supported harnesses:

- Codex
- OpenCode
- Antigravity
- Claude Code

## Workflow

1. Discover existing project-local harness directories before creating new ones.
2. Use these project locations:
   - Codex: `.codex/agents/<agent-name>.toml`
   - OpenCode: `.opencode/agents/<agent-name>.md`
   - Antigravity: `.gemini/agents/<agent-name>.md`
   - Claude Code: `.claude/agents/<agent-name>.md`
3. If a harness uses a different project subagent path in the current repo, follow the existing repo convention.
4. Add the requested subagent to every supported harness the user asked for. If the user asks generally, update all supported harnesses that have project-local config or can safely receive one.
5. Preserve each harness schema and avoid relying on a plugin when the user asked for explicit project-local subagents.
6. Keep the subagent prompt behaviorally equivalent across harnesses, but adapt frontmatter and metadata to each schema.

## Schema Notes

Use the schema already present in the target file when updating existing subagents.

- Codex uses TOML with `name`, `description`, and a multiline `developer_instructions` string.
- OpenCode uses Markdown in `.opencode/agents/` with YAML frontmatter. Common fields include `description`, `mode: subagent`, `model`, `temperature`, and `maxSteps`.
- Antigravity uses Markdown in `.gemini/agents/` with YAML frontmatter. Common fields include `name`, `description`, `kind: local`, `model`, `temperature`, and `max_turns`. Prefer not to pin tool allowlists unless the exact tool names are known for the target version.
- Claude Code uses Markdown in `.claude/agents/` with YAML frontmatter. Common fields include `name`, `description`, `tools`, and `model`.

## Minimal Example

Subagent named `svelte-file-editor`:

Codex `.codex/agents/svelte-file-editor.toml`:

```toml
name = "svelte-file-editor"
description = "Specialized Svelte 5 code editor. Use proactively when creating, editing, or reviewing Svelte files."

developer_instructions = """
You are a Svelte 5 expert responsible for writing, editing, and validating Svelte components and modules.

Use the Svelte MCP server as the source of truth. Fetch current documentation before changing Svelte code, then validate changed Svelte code with the Svelte autofixer.
"""
```

OpenCode `.opencode/agents/svelte-file-editor.md`:

```md
---
description: Specialized Svelte 5 code editor. Use proactively when creating, editing, or reviewing Svelte files.
mode: subagent
model: inherit
temperature: 1
maxSteps: 30
---

You are a Svelte 5 expert responsible for writing, editing, and validating Svelte components and modules.

Use the Svelte MCP server as the source of truth. Fetch current documentation before changing Svelte code, then validate changed Svelte code with the Svelte autofixer.
```

Antigravity `.gemini/agents/svelte-file-editor.md`:

```md
---
name: svelte-file-editor
description: Specialized Svelte 5 code editor. Use proactively when creating, editing, or reviewing Svelte files.
kind: local
model: inherit
temperature: 1
max_turns: 30
---

You are a Svelte 5 expert responsible for writing, editing, and validating Svelte components and modules.

Use the Svelte MCP server as the source of truth. Fetch current documentation before changing Svelte code, then validate changed Svelte code with the Svelte autofixer.
```

Claude Code `.claude/agents/svelte-file-editor.md`:

```md
---
name: svelte-file-editor
description: Specialized Svelte 5 code editor. Use proactively when creating, editing, or reviewing Svelte files.
tools: Read, Glob, Grep, Edit, MultiEdit, Write, Bash
model: inherit
---

You are a Svelte 5 expert responsible for writing, editing, and validating Svelte components and modules.

Use the Svelte MCP server as the source of truth. Fetch current documentation before changing Svelte code, then validate changed Svelte code with the Svelte autofixer.
```

## Rules

1. Keep subagent names filesystem-safe and consistent across harnesses.
2. Keep prompts concise and specific to the delegated responsibility.
3. Do not add secrets, API keys, or user-specific paths to subagent files.
4. Do not overwrite an existing subagent with unrelated behavior; merge or update only the requested agent.
5. Prefer project-local subagents over user-global subagents.
6. Validate changed TOML with a parser when possible.
7. Validate Markdown frontmatter shape by inspection when no harness validator is available.
8. Update project documentation if the set of supported subagents or their locations changes.
