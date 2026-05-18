---
name: find-mcps
description: Helps users discover, compare, vet, and install Model Context Protocol (MCP) servers or connectors. Use when the user asks to find an MCP for a tool, service, workflow, client, or capability; asks whether an MCP exists; wants MCP recommendations; or wants help adding an MCP server safely to Codex, Claude, Cursor, VS Code, or another MCP-compatible client.
---

# Find MCPs

Help users find MCP servers that solve a specific integration need, then verify they are trustworthy enough to recommend or install.

## Core Rule

Do not recommend an MCP just because it exists. MCP servers can read data, call APIs, run local commands, or mutate external systems. Treat every recommendation as a lightweight security review.

## Workflow

### 1. Clarify the Need

Identify:

- The target service or capability
- The MCP client the user wants to use, if relevant
- Whether they need local stdio, remote HTTP, or a hosted connector
- Whether the server needs credentials or access to sensitive data
- Whether tools must be read-only or may perform writes

If the client, write permissions, or credential scope materially changes the recommendation and cannot be inferred, ask one concise question before installing. For simple discovery, proceed with reasonable assumptions and state them.

### 2. Search Current Sources

Use current sources because MCP registries and server quality change quickly.

Start with:

- Official MCP Registry: `https://registry.modelcontextprotocol.io/`
- Official registry docs: `https://modelcontextprotocol.io/registry/about`
- Glama: `https://glama.ai/`
- PulseMCP: `https://www.pulsemcp.com/servers`
- Smithery: `https://smithery.ai/`
- GitHub search and curated lists, especially when the registry result points to source code

Prefer the official registry for canonical metadata. Use aggregators for search quality, tool-level discovery, health signals, usage signals, security notes, and install snippets.

When the user names a specific package or repo, inspect that source directly instead of relying only on registry metadata.

### 3. Screen Candidates

Shortlist 2-4 candidates when possible. For each candidate, check:

- Maintainer identity: official vendor, known organization, verified namespace, or reputable individual
- Source availability: public repo, package registry page, Docker image, or hosted endpoint docs
- Maintenance: recent commits or releases, open issue health, version history
- Install path: exact command, package name, Docker image, or remote URL
- Permissions: tools exposed, read/write behavior, file/network/API access
- Authentication: required secrets, OAuth scopes, token storage, credential handling
- Client compatibility: Codex, Claude Desktop, Claude Code, Cursor, VS Code, ChatGPT, or other requested host
- License and cost: open-source license, hosted pricing, rate limits

Reject or warn about candidates with unclear ownership, broad write tools, unpinned install commands from unknown sources, abandoned repos, opaque hosted endpoints, missing docs, or credential scopes broader than the task requires.

### 4. Inspect Tools Before Trusting

When a registry exposes tool metadata, inspect the tool list and schemas. Look for:

- Narrow, task-specific tool names and descriptions
- Clear input schemas
- Safety annotations such as read-only, destructive, or idempotent hints
- Separation between read tools and write tools
- Absence of surprising capabilities such as arbitrary shell execution, unrestricted filesystem access, or broad database mutation

If tool metadata is unavailable, say so and treat the recommendation as lower confidence.

### 5. Present Recommendations

Give the user a compact comparison:

```text
Best fit: <server>
Why: <one sentence>
Trust notes: <maintainer/source/maintenance/security notes>
Access needed: <credentials/scopes/local access>
Install: <command or config>
Risk: <low/medium/high with reason>
```

If multiple options are credible, explain the tradeoff:

- Official/vendor MCP: prefer for production or sensitive accounts
- Popular community MCP: acceptable for low-risk workflows after source review
- Hosted connector: convenient, but adds a third-party control plane
- Local server: more setup, but credentials stay local if implemented correctly

Do not bury risk notes after the install command.

### 6. Install Only With Consent

Before installing or editing MCP config, state exactly what will change:

- Target config file or client
- Server name
- Command, args, URL, or package
- Required environment variables or secrets
- Whether it can perform writes or destructive actions

Never invent credentials. If secrets are required, tell the user which environment variables to set and avoid printing real token values.

When editing config, preserve existing MCP entries and match the client's existing format. After editing, validate the config syntax.

### 7. Verify

Use the safest verification available:

- Run the client or MCP inspector only if appropriate for the environment
- List tools before calling any tool
- Prefer read-only calls for smoke tests
- Avoid calls that send emails, modify issues, write files, delete data, purchase items, deploy code, or otherwise mutate external state unless the user explicitly requested that test

Report what was verified and what was not.

## Recommendation Standards

Prefer:

- Official servers from the service provider
- Servers listed in the official MCP Registry with verified namespaces
- Repos with recent maintenance, clear docs, and explicit tool descriptions
- Install commands that can be pinned to a version
- Narrow OAuth scopes or read-only tokens
- Servers that separate read and write capabilities

Be cautious with:

- `npx -y` install snippets from unknown packages
- Packages without a source repo
- Broad access tokens
- Servers that expose shell, browser, filesystem, database, or cloud admin tools
- Hosted connectors without clear privacy, logging, or credential docs
- Unmaintained repos or tiny packages with many powerful tools

## Response Patterns

When a good MCP exists:

```text
I found a good fit: <name>. It is maintained by <source>, supports <client/capability>, and exposes <summary of tools>. The main risk is <risk>. Use this install/config:

<command or JSON>
```

When no good MCP exists:

```text
I found MCPs adjacent to this, but none I would recommend for <need>. The gap is <reason>. The safer path is <alternative>, or I can help build a small purpose-specific MCP.
```

When the user asks for "the best" MCP:

```text
Assumption: "best" means safest and most maintainable for <need>, not just most popular. Based on that, I would choose <name> because <reason>.
```

## Installation Snippets

Use snippets from the MCP's own docs or verified registry page. Adapt only the minimum needed for the user's client.

Typical local MCP shape:

```json
{
  "mcpServers": {
    "name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "API_TOKEN": "${API_TOKEN}"
      }
    }
  }
}
```

Typical remote MCP shape:

```json
{
  "mcpServers": {
    "name": {
      "url": "https://example.com/mcp"
    }
  }
}
```

Confirm the exact schema for the target client before editing because MCP client config formats differ.
