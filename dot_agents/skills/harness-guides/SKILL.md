---
name: harness-guides
description: Add or update project-scoped MCP server entries and subagent definitions across agent harnesses (Codex, OpenCode, Antigravity, Claude Code). Use only when the user explicitly invokes this skill.
---

# Harness Guides

Install MCP servers and subagents into project-scoped harness configuration. Do not edit
user-global configuration unless the user explicitly asks for global setup.

Supported harnesses:

- Codex
- OpenCode
- Antigravity
- Claude Code

## Workflow

1. Discover existing project-local harness config files and directories before creating new ones.
2. Use the project locations listed in the relevant section below. If a harness uses a different
   project path in the current repo, follow the existing repo convention.
3. Apply the change to every supported harness the user asked for. If the user asks generally,
   update all supported harnesses that have project-local config or can safely receive one.
4. Preserve each harness schema. When updating an existing file, use the schema already present in
   it.

## MCP Servers

Locations:

- Codex: `.codex/config.toml`
- OpenCode: `opencode.json` in the project root; use `opencode.jsonc` only if it already exists.
- Antigravity: `.gemini/settings.json`
- Claude Code: `.mcp.json`

Schema notes:

- Codex: `[mcp_servers.<name>]` TOML tables with `url` or `command`/`args`.
- OpenCode: `mcp.<name>` with `type: "remote"` plus `url`, or `type: "local"` plus a `command` array.
- Antigravity: `mcpServers.<name>` with `httpUrl` for remote servers, or `command`/`args` for local
  servers.
- Claude Code: `mcpServers.<name>` with `type: "http"` plus `url`, or `type: "stdio"` plus
  `command`/`args`.

Remote server named `context7` at `https://mcp.context7.com/mcp`:

Codex `.codex/config.toml`:

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
```

OpenCode `opencode.json`:

```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

Antigravity `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "context7": {
      "httpUrl": "https://mcp.context7.com/mcp"
    }
  }
}
```

Claude Code `.mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

Rules:

1. Do not add credentials or tokens to config files; reference environment variables instead.
2. Keep ordering consistent with existing MCP entries.

## Subagents

Locations:

- Codex: `.codex/agents/<agent-name>.toml`
- OpenCode: `.opencode/agents/<agent-name>.md`
- Antigravity: `.gemini/agents/<agent-name>.md`
- Claude Code: `.claude/agents/<agent-name>.md`

Schema notes:

- Codex uses TOML with `name`, `description`, and a multiline `developer_instructions` string.
- OpenCode uses Markdown in `.opencode/agents/` with YAML frontmatter. Common fields include
  `description`, `mode: subagent`, `model`, `temperature`, and `maxSteps`. Omit `model` to use the
  invoking agent's model.
- Antigravity uses Markdown in `.gemini/agents/` with YAML frontmatter. Common fields include
  `name`, `description`, `kind: local`, `model`, `temperature`, and `max_turns`. Prefer not to pin
  tool allowlists unless the exact tool names are known for the target version.
- Claude Code uses Markdown in `.claude/agents/` with YAML frontmatter. Common fields include
  `name`, `description`, `tools`, and `model`. Omit `tools` to inherit every tool; pin a list only
  when the exact tool names are known for the installed version.

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
model: inherit
---

You are a Svelte 5 expert responsible for writing, editing, and validating Svelte components and modules.

Use the Svelte MCP server as the source of truth. Fetch current documentation before changing Svelte code, then validate changed Svelte code with the Svelte autofixer.
```

Rules:

1. Keep subagent names filesystem-safe and consistent across harnesses.
2. Keep the prompt behaviorally equivalent across harnesses; adapt only frontmatter and metadata to
   each schema.
3. Keep prompts concise and specific to the delegated responsibility.
4. Do not add secrets, API keys, or user-specific paths to subagent files.
5. Do not overwrite an existing subagent with unrelated behavior; merge or update only the
   requested agent.
6. Do not rely on a plugin when the user asked for explicit project-local subagents.
7. Update project documentation if the set of supported subagents or their locations changes.

## Validation

- Validate changed JSON, JSONC, and TOML with an appropriate parser or harness command when
  available.
- Validate Markdown frontmatter shape by inspection when no harness validator is available.
