# Agent Workflow Dotfiless

This repository is a chezmoi-managed global configuration for coding agents. It installs shared instructions, reusable skills, and MCP server configuration for Codex and OpenCode so both tools follow the same workflow.

The important idea is separation of scope:

- This repo owns global agent behavior and tool configuration.
- Individual projects own their own `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, and `DESIGN.md`.
- The global skills in this repo help agents create and maintain those project-scope files.

Root `README.md` is for humans. Root `AGENTS.md` is the shared operating manual for agents and is symlinked into the configured agent tools.

## Navigation

- [Agent Workflow](#agent-workflow)
- [Skill Catalog](#skill-catalog)
- [MCP Servers](#mcp-servers)
- [Setup](#setup)

## Agent Workflow

The global workflow is:

1. Ground in the target project before changing anything.
2. State assumptions, tradeoffs, and success criteria.
3. Use the right skill or MCP only when it fits the task.
4. Make the smallest change that solves the problem.
5. Verify with focused checks.
6. Report what changed, what was verified, and what remains uncertain.

Project-scope documentation follows this ownership model:

| File            | Scope   | Owns                                                            |
| --------------- | ------- | --------------------------------------------------------------- |
| `README.md`       | Project | Human overview, setup, usage, and navigation                    |
| `AGENTS.md`       | Project | Repo-specific agent instructions and workflow constraints       |
| `ARCHITECTURE.md` | Project | Stack, system structure, data flow, integrations, and tradeoffs |
| `DESIGN.md`       | Project | Visual identity, design tokens, UI rules, and interaction feel  |

This global configuration repo intentionally does not have root `ARCHITECTURE.md` or `DESIGN.md` files.

## Skill Catalog

Agents choose skills from the skill name and frontmatter `description`, because that metadata is visible before the skill body is loaded.

| Skill              | Description                                                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------- |
| `brainstorm`         | Refine rough product ideas through concept-level questioning before implementation planning.                          |
| `setup`              | Coordinate project documentation setup across `DESIGN.md`, `ARCHITECTURE.md`, `README.md`, and `AGENTS.md`.                   |
| `write-design`       | Create or update `DESIGN.md` with visual identity, design tokens, component styling, and interaction guidance.          |
| `write-architecture` | Create or update `ARCHITECTURE.md` with project technology, system structure, data flow, integrations, and tradeoffs.   |
| `write-readme`       | Create or update a human-facing project `README.md` with overview, setup, usage, and navigation.                        |
| `write-agents`       | Create or update a project `AGENTS.md` with concise, repo-specific operating instructions for coding agents.            |
| `frontend-design`    | Build or improve frontend interfaces with strong visual quality and project-appropriate design.                       |
| `audit`              | Perform a read-only pre-deployment review for security, correctness, spec alignment, and code quality.                |
| `md-table-formatter` | Format Markdown tables so columns are aligned and readable.                                                           |
| `find-skills`        | Discover, compare, vet, and optionally help install external agent skills.                                            |
| `find-mcps`          | Discover, compare, vet, and optionally help install Model Context Protocol servers or connectors.                     |
| `commit`             | Create a git commit with a message based on the actual diff when the user explicitly asks for a commit.               |
| `handoff`            | Create a concise handoff document when the user explicitly asks another agent or future session to continue the work. |

## MCP Servers

Both Codex and OpenCode are configured with the same MCP capabilities:

| MCP        | Purpose                                                       |
| ---------- | ------------------------------------------------------------- |
| `context7`   | Current library and framework documentation                   |
| `gh_grep`    | Real-world code examples from public GitHub repositories      |
| `playwright` | Browser automation, UI checks, and end-to-end verification    |
| `github`     | GitHub API workflows when the user authorizes repository work |

The MCP configuration is documented here, but the actual values live in:

- `dot_codex/config.toml`
- `dot_config/opencode/opencode.jsonc`

## Setup

Install chezmoi:

```bash
# macOS
brew install chezmoi

# Linux
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin

# Windows
winget install twpayne.chezmoi
```

Initialize and apply this source repo:

```bash
chezmoi init --apply https://github.com/kaufmann-dev/dotfiles.git
```

Every time this repository is updated, run:

```bash
chezmoi update
```
