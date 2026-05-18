# Agent Workflow Dotfiles

Personal agent workflow dotfiles managed with [chezmoi](https://www.chezmoi.io/).

This repository installs shared instructions, reusable skills, and MCP server configuration for Codex and OpenCode. It is intentionally small: global behavior lives here, while each project keeps its own project-specific documentation and constraints.

## Contents

- [What This Manages](#what-this-manages)
- [Prerequisites](#prerequisites)
- [Install](#install)
- [Daily Usage](#daily-usage)
- [Structure](#structure)
- [Agent Instructions](#agent-instructions)
- [Skills](#skills)
- [MCP Servers](#mcp-servers)
- [Chezmoi Mapping](#chezmoi-mapping)

## What This Manages

- `~/.codex/config.toml` with Codex web search and MCP server settings.
- `~/.codex/AGENTS.md` as a symlink to this repo's root `AGENTS.md`.
- `~/.config/opencode/opencode.jsonc` with OpenCode defaults, tools, and MCP server settings.
- `~/.config/opencode/tui.jsonc` with OpenCode TUI preferences.
- `~/.config/opencode/AGENTS.md` as a symlink to this repo's root `AGENTS.md`.
- `~/.agents/skills/` with shared skill definitions for agents.

The root `README.md` is source-repository documentation only. It is ignored by chezmoi and is not installed into the home directory.

## Prerequisites

Install chezmoi:

```bash
# macOS
brew install chezmoi

# Linux
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin

# Windows
winget install twpayne.chezmoi
```

Some configured MCP servers run through `npx`, so Node.js/npm must also be available for full MCP support.

## Install

Initialize and apply this repository:

```bash
chezmoi init --apply https://github.com/kaufmann-dev/dotfiles.git
```

For a local checkout:

```bash
chezmoi init --source-path .
chezmoi apply
```

Preview changes before applying them:

```bash
chezmoi diff
```

## Daily Usage

| Command             | Description                                                    |
| ------------------- | -------------------------------------------------------------- |
| `chezmoi diff`        | Preview changes that would be applied to the home directory.   |
| `chezmoi apply`       | Apply the current source state to the home directory.          |
| `chezmoi update`      | Pull the latest remote changes and apply them.                 |
| `chezmoi edit <file>` | Edit a managed target file through chezmoi's source directory. |
| `chezmoi re-add`      | Import target-side changes back into the source directory.     |

## Structure

```text
dotfiles/
|-- AGENTS.md
|-- README.md
|-- dot_agents/
|   `-- skills/
|       |-- commit/
|       |-- md-table-formatter/
|       |-- write-agents/
|       |-- write-design/
|       `-- write-readme/
|-- dot_codex/
|   |-- config.toml
|   `-- symlink_AGENTS.md.tmpl
`-- dot_config/
    `-- opencode/
        |-- opencode.jsonc
        |-- symlink_AGENTS.md.tmpl
        `-- tui.jsonc
```

## Agent Instructions

`AGENTS.md` is the shared operating guide. Both Codex and OpenCode receive it through symlinks created by chezmoi:

- `dot_codex/symlink_AGENTS.md.tmpl` maps to `~/.codex/AGENTS.md`.
- `dot_config/opencode/symlink_AGENTS.md.tmpl` maps to `~/.config/opencode/AGENTS.md`.

The global instructions emphasize simple, surgical changes, repo-first discovery, focused verification, and documentation ownership. Project-local `AGENTS.md` files remain more specific and should override these global defaults when they apply.

## Skills

Skills are installed under `~/.agents/skills/`. Each skill exposes a short frontmatter description that agents can use before loading the full instructions.

| Skill              | Purpose                                                         |
| ------------------ | --------------------------------------------------------------- |
| `commit`             | Commit changes only when the user explicitly asks for a commit. |
| `md-table-formatter` | Format Markdown tables after any table is created or modified.  |
| `write-agents`       | Create a project `AGENTS.md` from scratch.                        |
| `write-design`       | Create a project `DESIGN.md` from scratch.                        |
| `write-readme`       | Create a project `README.md` from scratch.                        |

These skills are deliberately narrow. Existing project documentation should be edited directly unless a skill's instructions say otherwise.

## MCP Servers

Codex and OpenCode are configured with the same MCP servers:

| MCP        | Configuration | Purpose                                                     |
| ---------- | ------------- | ----------------------------------------------------------- |
| `context7`   | Remote URL    | Current library and framework documentation.                |
| `gh_grep`    | Remote URL    | Real-world code examples from public GitHub repositories.   |
| `playwright` | Local `npx`     | Browser automation, UI checks, and end-to-end verification. |
| `github`     | Local `npx`     | GitHub API workflows when repository work is authorized.    |

OpenCode also enables `websearch` and `codesearch`, sets `default_agent` to `build`, enables `autoupdate`, and uses the `vercel` TUI theme.

## Chezmoi Mapping

Chezmoi translates source names into target paths in the home directory:

| Source prefix | Destination behavior                                |
| ------------- | --------------------------------------------------- |
| `dot_`          | Becomes a hidden file or directory, such as `.codex`. |
| `symlink_`      | Creates a symlink instead of a regular file.        |
| `.tmpl`         | Renders the file as a chezmoi template.             |

For example, `dot_config/opencode/opencode.jsonc` maps to `~/.config/opencode/opencode.jsonc` on macOS/Linux and `%USERPROFILE%\.config\opencode\opencode.jsonc` on Windows.
