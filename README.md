# Dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

Supported agent tools: Codex, OpenCode, Antigravity, and Claude Code.

This repository focuses on installing shared instructions, reusable skills, and MCP server configurations for supported agent tools. While it is kept lightweight to ensure global agent behaviors live here, it serves as a flexible foundation that can grow to manage other configurations and dotfiles as needed.

- **Tool Settings** (`~/.codex/`, `~/.config/opencode/`, `~/.gemini/config/`, `~/.gemini/antigravity-cli/`, `~/.claude/`, `~/.claude.json`): Configures native settings, MCP servers, and shared instructions.
- **Shared Skills** (`~/.agents/skills/`): Installs reusable, specialized skills that agents can use.

## Contents

- [Dotfiles](#dotfiles)
  - [Contents](#contents)
  - [Prerequisites](#prerequisites)
  - [Install](#install)
  - [Automating Updates](#automating-updates)
  - [Structure](#structure)
  - [Agent Instructions](#agent-instructions)
  - [Skills](#skills)
  - [MCP Servers](#mcp-servers)

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

For a local checkout, run `chezmoi init --source-path . --apply` instead.

**Optional**: enable the GitHub MCP server by copying the example data file, adding
your GitHub personal access token, and applying again:

```bash
cp ~/.config/chezmoi/chezmoi.toml.example ~/.config/chezmoi/chezmoi.toml
$EDITOR ~/.config/chezmoi/chezmoi.toml
chezmoi apply
```

Every time this repository is updated, run:

```bash
chezmoi update
```

## Automating Updates

A simple pattern for keeping a CLI tool in sync is to wrap its launch command with a background update. This triggers `chezmoi update` asynchronously every time you open the tool — no waiting, no manual syncing.

Add a shell function that runs the update silently in the background before launching:

```bash
# macOS & Linux (Add to ~/.bashrc or ~/.zshrc)
echo 'agenttool() { chezmoi update > /dev/null 2>&1 & command agenttool "$@"; }' >> ~/.bashrc && source ~/.bashrc

# Windows (PowerShell - Add to $PROFILE)
if (!(Test-Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }; Add-Content -Path $PROFILE -Value "`nfunction agenttool { Start-Process -WindowStyle Hidden -FilePath 'chezmoi' -ArgumentList 'update'; & 'agenttool.exe' @args }"; . $PROFILE
```

Replace `agenttool` with the command you want to keep synced. The wrapper function fires `chezmoi update` in the background without blocking or outputting text, then launches the tool itself.

To remove the auto-update wrapper:
- **macOS / Linux:** Open your shell profile (`nano ~/.bashrc`), remove the wrapper function line, and save.
- **Windows:** Run `notepad $PROFILE`, delete the wrapper function block, and save.

## Structure

```text
dotfiles/
|-- .gitignore
|-- AGENTS.md
|-- README.md
|-- dot_agents/
|   `-- skills/
|       |-- add-mcp-servers/
|       |-- add-subagents/
|       |-- audit-complete/
|       |-- audit-defect/
|       |-- audit-rubric/
|       |-- authentik-oidc-migration/
|       |-- autofixer/
|       |-- autofixer-graphify/
|       |-- autofixer-yolo/
|       |-- build-brief-generator/
|       |-- coolify/
|       |-- create-datatable/
|       |-- debugging/
|       |-- distill-agents-md/
|       |-- humanizer/
|       |-- humanizer-german/
|       |-- improve-goal/
|       |-- improve-implementation-plan/
|       |-- improve-prompt/
|       |-- md-table-formatter/
|       |-- svg-theme-converter/
|       |-- ui-cleanup/
|       |-- ui-design-principles/
|       |-- write-agents-md/
|       |-- write-design-md/
|       `-- write-readme-md/
|-- dot_codex/
|   |-- config.toml.tmpl
|   `-- AGENTS.md.tmpl
|-- dot_claude/
|   `-- CLAUDE.md.tmpl
|-- dot_claude.json.tmpl
|-- dot_gemini/
|   |-- antigravity/
|   |   `-- symlink_skills.tmpl
|   |-- antigravity-cli/
|   |   `-- settings.json.tmpl
|   |-- config/
|   |   `-- mcp_config.json.tmpl
|   `-- GEMINI.md.tmpl
`-- dot_config/
    |-- chezmoi/
    |   `-- chezmoi.toml.example
    `-- opencode/
        |-- opencode.jsonc.tmpl
        |-- AGENTS.md.tmpl
        `-- tui.jsonc
```

## Agent Instructions

`AGENTS.md` is the shared operating guide. Native instruction filenames are generated from it as templates by chezmoi:

- `dot_codex/AGENTS.md.tmpl` maps to `~/.codex/AGENTS.md`.
- `dot_config/opencode/AGENTS.md.tmpl` maps to `~/.config/opencode/AGENTS.md`.
- `dot_gemini/GEMINI.md.tmpl` maps to `~/.gemini/GEMINI.md`.
- `dot_claude/CLAUDE.md.tmpl` maps to `~/.claude/CLAUDE.md`.

The global instructions emphasize simple, surgical changes, repo-first discovery, focused verification, and documentation ownership. Project-local `AGENTS.md` files remain more specific and should override these global defaults when they apply.

## Skills

Skills are installed under `~/.agents/skills/`.

| Skill                         | Purpose                                                                                        |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| `add-mcp-servers`             | Add or update project-scoped MCP server configuration entries.                                 |
| `add-subagents`               | Add or update project-scoped subagent definitions across multiple agent tools.                 |
| `audit-complete`              | Perform a comprehensive, stateless codebase audit before a major release.                      |
| `audit-defect`                | Directly audit a codebase for concrete, actionable defects.                                    |
| `audit-rubric`                | Create a bounded, project-specific rubric and immediately audit against it.                    |
| `authentik-oidc-migration`    | Migrate Kaufmann apps from local authentication to Authentik OIDC.                             |
| `autofixer`                   | Coordinate a bounded audit-fix-verify loop using fresh-context subagents.                      |
| `autofixer-graphify`          | Like `autofixer` but with Graphify-backed repository graph context.                            |
| `autofixer-yolo`              | Coordinate a bounded audit-fix-verify loop that proceeds without approval for dangerous fixes. |
| `build-brief-generator`       | Turns a product idea into a clear, complete, and practical AI Build Brief.                     |
| `coolify`                     | Generate a project's Coolify/Nixpacks deployment config (nixpacks.toml + README).              |
| `create-datatable`            | Create, extend, or review production-quality tabular data views.                               |
| `debugging`                   | Debug bugs by reproducing behavior, confirming root cause, and documenting fixes.              |
| `distill-agents-md`           | Distill bloated instruction files (AGENTS.md, etc.) into lean versions.                        |
| `humanizer`                   | Remove signs of AI-generated writing from text.                                                |
| `humanizer-german`            | Rewrite German text to sound natural and idiomatic without flattening it.                      |
| `improve-goal`                | Improve goals, persistent objectives, and long-running task contracts.                         |
| `improve-implementation-plan` | Improve implementation plans by recovering intent and re-deriving solutions.                   |
| `improve-prompt`              | Improve prompt and instruction files using general prompt-quality guidance.                    |
| `md-table-formatter`          | Format Markdown tables after any table is created or modified.                                 |
| `svg-theme-converter`         | Convert an SVG icon into a self-theming light/dark SVG via embedded CSS.                       |
| `ui-cleanup`                  | Clean up duplicated and inconsistent frontend UI when explicitly requested.                    |
| `ui-design-principles`        | Apply accessible, responsive, and complete UI design defaults.                                 |
| `write-agents-md`             | Create a repository- or subtree-scoped `AGENTS.md` from codebase evidence.                     |
| `write-design-md`             | Create a project `DESIGN.md` from scratch.                                                     |
| `write-readme-md`             | Create a project `README.md` from scratch.                                                     |

## MCP Servers

All supported agent tools are configured with the same MCP servers:

| MCP          | Configuration | Purpose                                                     |
| ------------ | ------------- | ----------------------------------------------------------- |
| `context7`   | Remote URL    | Current library and framework documentation.                |
| `gh_grep`    | Remote URL    | Real-world code examples from public GitHub repositories.   |
| `playwright` | Local `npx`   | Browser automation, UI checks, and end-to-end verification. |
| `github`     | Local `npx`   | GitHub API workflows when repository work is authorized.    |

The `github` MCP server needs local GitHub authentication. This public repository
does not store tokens or other credentials. The MCP config files are chezmoi
templates that read `github_pat` from `~/.config/chezmoi/chezmoi.toml` when it
exists. Without that local file, the GitHub MCP server is omitted.

Use a fine-grained GitHub personal access token with only the permissions needed
for the repositories or organizations you work with.

The `playwright` MCP server needs its browser installed once per machine. The
configs pass `--browser chromium`, so install Playwright's bundled Chromium:

```sh
npx --yes playwright install --with-deps chromium  # Linux (omit --with-deps on macOS/Windows)
```
