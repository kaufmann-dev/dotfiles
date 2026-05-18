# Dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

This repository currently focuses on installing shared instructions, reusable skills, and MCP server configurations for Codex and OpenCode. While it is kept lightweight to ensure global agent behaviors live here, it serves as a flexible foundation that can grow to manage other configurations and dotfiles as needed.

- **Codex Settings** (`~/.codex/`): Configures web search, MCP servers, and shared instructions.
- **OpenCode Settings** (`~/.config/opencode/`): Configures tool defaults, interface styling, and shared instructions.
- **Shared Skills** (`~/.agents/skills/`): Installs reusable, specialized skills that agents can use.

## Contents

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

For a local checkout:

```bash
chezmoi init --source-path .
chezmoi apply
```

Every time this repository is updated, run:

```bash
chezmoi update
```

## Automating Updates

A simple pattern for keeping tools like OpenCode in sync is to wrap their launch command with a background update. This triggers `chezmoi update` asynchronously every time you open the tool — no waiting, no manual syncing.

### macOS and Linux

Add a shell function that runs the update silently in the background before launching:

```bash
echo 'opencode() { chezmoi update > /dev/null 2>&1 & command opencode "$@"; }' >> ~/.bashrc && source ~/.bashrc
```

> **Note:** Replace `~/.bashrc` with `~/.zshrc` (or your shell's profile file) if you're not using Bash.

### Windows (PowerShell)

```powershell
if (!(Test-Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }; Add-Content -Path $PROFILE -Value "`nfunction opencode { Start-Process -WindowStyle Hidden -FilePath 'chezmoi' -ArgumentList 'update'; & 'opencode.exe' @args }"; . $PROFILE
```

### How It Works

The wrapper function intercepts calls to `opencode` and:

1. Fires `chezmoi update` in the background (no terminal output, doesn't block)
2. Immediately launches the real `opencode` with any arguments you passed

You can adapt this pattern to **any CLI tool** — just replace `opencode` with the command you want to trigger updates on.

### Removing the Auto-Update

- **macOS / Linux:** Open your shell profile (`nano ~/.bashrc`), remove the `opencode()` function line, and save.
- **Windows:** Run `notepad $PROFILE`, delete the `function opencode { ... }` block, and save.

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

Skills are installed under `~/.agents/skills/`.

| Skill              | Purpose                                                                        |
| ------------------ | ------------------------------------------------------------------------------ |
| `commit`             | Stage and commit changes using structured, conventional git commit guidelines. |
| `md-table-formatter` | Format Markdown tables after any table is created or modified.                 |
| `write-agents`       | Create a project `AGENTS.md` from scratch.                                       |
| `write-design`       | Create a project `DESIGN.md` from scratch.                                       |
| `write-readme`       | Create a project `README.md` from scratch.                                       |

## MCP Servers

Codex and OpenCode are configured with the same MCP servers:

| MCP        | Configuration | Purpose                                                     |
| ---------- | ------------- | ----------------------------------------------------------- |
| `context7`   | Remote URL    | Current library and framework documentation.                |
| `gh_grep`    | Remote URL    | Real-world code examples from public GitHub repositories.   |
| `playwright` | Local `npx`     | Browser automation, UI checks, and end-to-end verification. |
| `github`     | Local `npx`     | GitHub API workflows when repository work is authorized.    |