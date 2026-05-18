---
name: find-mcps
description: Discover, compare, vet, and optionally help install Model Context Protocol servers or connectors.
---

# Find MCPs

## Purpose

Help the user find MCP servers or connectors that fit a tool, service, or workflow, while treating each recommendation as a lightweight security review.

## Use When

- The user asks whether an MCP exists.
- The user wants MCP recommendations.
- The user wants help adding an MCP server to Codex, OpenCode, Claude, Cursor, VS Code, or another MCP-compatible client.
- A workflow would benefit from a new external integration.

## Do Not Use When

- The user is asking to use an MCP that is already configured and available.
- The user wants a normal library recommendation rather than an MCP.
- The task can be solved safely with existing tools and no new connector.

## Rules

- Current MCP availability changes often; use current sources when making recommendations.
- Do not recommend a server solely because it exists.
- Prefer official or clearly maintained servers.
- Treat broad write access, shell access, filesystem access, cloud admin tools, and opaque hosted endpoints as higher risk.
- Do not install, edit config, or request credentials without explicit user consent.
- Never invent tokens or secrets.

## Workflow

1. Clarify the target service, client, access needs, and whether writes are required.
2. Search current sources:
   - Official MCP Registry
   - Official service docs
   - Maintainer repositories
   - Reputable aggregators such as Glama, PulseMCP, or Smithery
3. Shortlist two to four candidates when possible.
4. Vet each candidate:
   - Maintainer identity
   - Source availability
   - Recent maintenance
   - Install path
   - Tool list and schemas
   - Read/write behavior
   - Credential scope
   - License and cost
5. Recommend the safest fit and explain tradeoffs.
6. Install or edit config only after the user approves the exact change.
7. Verify with tool listing or a read-only smoke test when possible.

## Output

For each credible candidate, include:

- Name and source
- Why it fits
- Access required
- Install/config shape
- Trust notes
- Risk level

When no good option exists, say so and suggest a safer alternative.

## Completion Rules

Finish after a recommendation, a safe config proposal, or a verified install. Separate recommendation from installation consent.
