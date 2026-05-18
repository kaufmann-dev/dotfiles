---
name: add-mcp-configs
description: Add or update project-scoped MCP server configuration entries. Use when a user asks to install, add, change, or synchronize MCP configs for multiple agent tools.
---

# Add MCP Configs

Install MCP servers into project-scoped config when the harness supports it. Do not edit user-global config unless the user explicitly asks for global setup.

Supported harnesses:

- Codex
- OpenCode
- Gemini CLI
- Claude Code

## Workflow

1. Discover existing project-local harness config files before creating new ones.
2. Use these config locations:
   - Codex: `.codex/config.toml`
   - OpenCode: `opencode.json` in the project root; use `opencode.jsonc` only if it already exists.
   - Gemini CLI: `.gemini/settings.json`
   - Claude Code: `.mcp.json`
3. If a harness uses a different project config path in the current repo, follow the existing repo convention.
4. Add the requested server to every supported harness the user asked for. If the user asks generally, update all supported harnesses that have project-local config or can safely receive one.
5. Preserve each harness schema.

## Schema Notes

Use the schema already present in the target file. Common shapes:

- Codex: `[mcp_servers.<name>]` TOML tables with `url` or `command`/`args`.
- OpenCode: `mcp.<name>` with `type: "remote"` plus `url`, or `type: "local"` plus a `command` array.
- Gemini CLI: `mcpServers.<name>` with `httpUrl` for remote servers, or `command`/`args` for local servers.
- Claude Code: `mcpServers.<name>` with `type: "http"` plus `url`, or `type: "stdio"` plus `command`/`args`.

## Minimal Examples

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

Gemini CLI `.gemini/settings.json`:

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

Local stdio server named `playwright` using `npx @playwright/mcp@latest`:

Codex `.codex/config.toml`:

```toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]
```

OpenCode `opencode.json`:

```json
{
  "mcp": {
    "playwright": {
      "type": "local",
      "command": ["npx", "@playwright/mcp@latest"]
    }
  }
}
```

Gemini CLI `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

Claude Code `.mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## Rules

1. Do not add credentials or tokens to config files; reference environment variables instead.
2. Keep ordering consistent with existing MCP entries.
3. Validate changed JSON, JSONC, and TOML with an appropriate parser or harness command when available.
