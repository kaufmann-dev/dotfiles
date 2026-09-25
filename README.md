# Dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

Supported agent tools: Codex, OpenCode, Antigravity, Claude Code, and Muse Code.

This repository focuses on installing shared instructions, reusable skills, and MCP server configurations for supported agent tools. While it is kept lightweight to ensure global agent behaviors live here, it serves as a flexible foundation that can grow to manage other configurations and dotfiles as needed.

- **Tool Settings** (`~/.codex/`, `~/.config/opencode/`, `~/.gemini/config/`, `~/.gemini/antigravity-cli/`, `~/.claude/`, `~/.claude.json`, `~/.config/muse/`): Configures native settings, MCP servers, and shared instructions.
- **Shared Skills** (`~/.agents/skills/`): Installs reusable, specialized skills that agents can use.

## Contents

- [Dotfiles](#dotfiles)
  - [Contents](#contents)
  - [Prerequisites](#prerequisites)
  - [Install](#install)
  - [Automating Updates](#automating-updates)
  - [Shell Aliases](#shell-aliases)
  - [Structure](#structure)
  - [Agent Instructions](#agent-instructions)
  - [Skills](#skills)
  - [MCP Servers](#mcp-servers)
  - [Browser Automation](#browser-automation)

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

Some configured MCP servers run through `npx`, so Node.js/npm must be available for full MCP
support. Purelymail also needs [Astral UV](https://docs.astral.sh/uv/) (`uvx`) on `PATH`.
Install `agent-browser` separately when browser automation is needed. The dotfiles
configure agents to use the command but do not install programs.

## Install

Initialize and apply this repository:

```bash
chezmoi init --apply https://github.com/kaufmann-dev/dotfiles.git
```

For a local checkout, run `chezmoi init --source-path . --apply` instead.

**Optional**: authenticate Context7 or enable the GitHub, Massive, Portfolio Arena, Executive Arena, and Purelymail MCP servers
by copying the example data file, adding your credentials, and applying again:

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

## Shell Aliases

`dot_config/shell/agent-aliases.sh` (→ `~/.config/shell/agent-aliases.sh`) defines
unrestricted launchers: `muse` runs with `--yolo`, while `agy` and `claude` run with
`--dangerously-skip-permissions`. Codex needs no wrapper because
`dot_codex/private_config.toml.tmpl` already sets `approval_policy = "never"`.
On Linux and macOS, chezmoi adds the source line to existing `~/.bashrc` and
`~/.zshrc` files without replacing their other settings. Fish loads the managed
`~/.config/fish/conf.d/agent-aliases.fish` automatically. The source line is:

```bash
source ~/.config/shell/agent-aliases.sh
```

On Windows, chezmoi adds a source line to the PowerShell 7 current-user,
all-hosts profile at `~/Documents/PowerShell/Profile.ps1` without replacing
other profile settings. It loads the managed
`~/.config/powershell/agent-aliases.ps1` functions.

These wrappers disable real protections. Do not use them on untrusted checkouts
(forks, PR branches).

## Agent Instructions

`.chezmoitemplates/AGENTS.md` is the shared operating guide. Chezmoi renders it only into
tool-specific instruction files:

- `dot_codex/AGENTS.md.tmpl` maps to `~/.codex/AGENTS.md`.
- `dot_config/opencode/AGENTS.md.tmpl` maps to `~/.config/opencode/AGENTS.md`.
- `dot_gemini/GEMINI.md.tmpl` maps to `~/.gemini/GEMINI.md`.
- `dot_claude/CLAUDE.md.tmpl` maps to `~/.claude/CLAUDE.md`.

No home-level `~/AGENTS.md` is installed.

The global instructions emphasize simple, surgical changes, repo-first discovery, focused verification, and documentation ownership. Project-local `AGENTS.md` files remain more specific and should override these global defaults when they apply.

Set `is_web_terminal = true` under `[data]` in `~/.config/chezmoi/chezmoi.toml` on the hosted web
terminal. This renders additional instructions for its nested rootless Podman architecture,
diagnostic workflow, and intentional security limitations. The example configuration defaults the
flag to `false` for other machines.

## Skills

Skills are installed under `~/.agents/skills/`.

The Auto-invoke column shows whether an agent may select a skill implicitly when it is relevant.
Skills marked No require explicit invocation with `$skill-name`.

| Skill                         | Purpose                                                                                        | Auto-invoke |
| ----------------------------- | ---------------------------------------------------------------------------------------------- | ----------- |
| `add-compliance-links`        | Add centralized imprint and privacy links to appropriate public website surfaces.              | No          |
| `add-mcp-servers`             | Add or update project-scoped MCP server configuration entries.                                 | No          |
| `add-subagents`               | Add or update project-scoped subagent definitions across multiple agent tools.                 | No          |
| `audit-complete`              | Perform a comprehensive, stateless codebase audit before a major release.                      | No          |
| `audit-defect`                | Directly audit a codebase for concrete, actionable defects.                                    | No          |
| `audit-rubric`                | Create a bounded, project-specific rubric and immediately audit against it.                    | No          |
| `oidc-migration`              | Migrate applications from local authentication to an OpenID Connect provider.                  | No          |
| `autofixer`                   | Coordinate a bounded audit-fix-verify loop using fresh-context subagents.                      | No          |
| `autofixer-graphify`          | Like `autofixer` but with Graphify-backed repository graph context.                            | No          |
| `autofixer-yolo`              | Coordinate a bounded audit-fix-verify loop that proceeds without approval for dangerous fixes. | No          |
| `build-brief-generator`       | Turns a product idea into a clear, complete, and practical AI Build Brief.                     | No          |
| `coolify`                     | Configure and diagnose Coolify/Nixpacks deployments.                                           | Yes         |
| `create-datatable`            | Guide context-sensitive decisions for creating, changing, or reviewing data tables.            | Yes         |
| `debloat`                     | Remove over-engineered security, testing, and complexity when explicitly requested.            | No          |
| `debugging`                   | Debug bugs by reproducing behavior, confirming root cause, and documenting fixes.              | Yes         |
| `distill-agents-md`           | Distill bloated instruction files (AGENTS.md, etc.) into lean versions.                        | Yes         |
| `humanizer`                   | Remove signs of AI-generated writing from text.                                                | No          |
| `humanizer-german`            | Rewrite German text to sound natural and idiomatic without flattening it.                      | No          |
| `improve-goal`                | Improve goals, persistent objectives, and long-running task contracts.                         | No          |
| `improve-implementation-plan` | Improve implementation plans by recovering intent and re-deriving solutions.                   | No          |
| `improve-prompt`              | Improve prompt and instruction files using general prompt-quality guidance.                    | No          |
| `md-table-formatter`          | Format Markdown tables after any table is created or modified.                                 | Yes         |
| `medsurface`                  | Convert medical volumes, fuse scans, and extract surface meshes.                               | Yes         |
| `proven-cash-yield`           | Calculate and quality-rank factual owner-cash yields using SEC and Massive data.               | Yes         |
| `svg-theme-converter`         | Convert an SVG icon into a self-theming light/dark SVG via embedded CSS.                       | Yes         |
| `ui-cleanup`                  | Clean up duplicated and inconsistent frontend UI when explicitly requested.                    | No          |
| `ui-design-principles`        | Apply accessible UI guardrails and scoped greenfield visual defaults.                          | Yes         |
| `write-agents-md`             | Create a repository- or subtree-scoped `AGENTS.md` from codebase evidence.                     | Yes         |
| `write-design-md`             | Create a project `DESIGN.md` from scratch.                                                     | Yes         |
| `write-readme-md`             | Create a project `README.md` from scratch.                                                     | Yes         |

## MCP Servers

All supported agent tools are configured with the same MCP servers:

| MCP               | Configuration | Purpose                                                   |
| ----------------- | ------------- | --------------------------------------------------------- |
| `context7`        | Remote HTTP   | Current library and framework documentation.              |
| `gh_grep`         | Remote HTTP   | Real-world code examples from public GitHub repositories. |
| `github`          | Local `npx`   | GitHub API workflows when repository work is authorized.  |
| `massive`         | Local stdio   | Financial market data when `mcp_massive` is installed.    |
| `portfolio_arena` | Remote HTTP   | Portfolio Arena admin data and operations.                |
| `executive_arena` | Remote HTTP   | Executive research tasks and profile publishing.          |
| `cv_resume`       | Remote HTTP   | Shared CV/resume content and visibility editing.          |
| `purelymail`      | Local `uvx`   | Read, organize, and send email through Purelymail.        |

Context7 can use an optional API key, while the `github`, `massive`, `portfolio_arena`, `executive_arena`, `cv_resume`, and `purelymail` MCP
servers require local credentials. This public repository does not store tokens or other
credentials. The MCP config files are chezmoi templates that read the following keys from
`~/.config/chezmoi/chezmoi.toml` when it exists:

- `is_web_terminal` — set to `true` only in the hosted web terminal to render its Podman-specific
  operating and diagnostic instructions; defaults to `false`.
- `context7_api_key` — a [Context7 API key](https://context7.com/dashboard). Context7 always
  remains configured and runs unauthenticated when this key is absent.
- `github_pat` — a fine-grained GitHub personal access token with only the
  permissions needed for the repositories or organizations you work with.
- `massive_api_key` — a [Massive.com API key](https://massive.com/?utm_campaign=mcp&utm_medium=referral&utm_source=github).
- `portfolio_arena_api_key` — a Portfolio Arena API key (generate one via the admin dashboard at <https://arena.kaufmann.dev>).
- `executive_arena_api_key` — an API key shown once when generated from Executive Arena's authenticated **API Keys** page.
- `cv_resume_api_key` — an API key created in the CV/Resume app's admin **Settings** tab.
- `purelymail_full_name` — optional sender display name; if omitted or empty, the server uses the email local part.
- `purelymail_email` — your full Purelymail mailbox address, used for IMAP and SMTP login.
- `purelymail_password` — your mailbox password; use a Purelymail app password when 2FA is enabled.

Without a required server credential, the corresponding MCP server is omitted.
Executive Arena uses the fixed `https://executives.kaufmann.dev/mcp` endpoint and is omitted unless
its API key is configured.

CV/Resume uses `https://resume.kaufmann.dev/api/mcp` with Bearer authentication. To enable
`cv_resume` across all harness configs, add the key under `[data]` in
`~/.config/chezmoi/chezmoi.toml`:

```toml
cv_resume_api_key = "your-api-key"
```

Run `chezmoi apply` and restart your agent tools. The server and its shared agent instruction
are omitted when the key is missing or empty. Keep the real key in this local config, not the
repository; the example leaves it empty. The key grants access to the shared document in both
CV and resume variants.

The Massive entry is generated only when `massive_api_key` is configured. Machines using it also
need [Astral UV](https://docs.astral.sh/uv/) and the `mcp_massive` binary on `PATH`:

```sh
uv tool install "mcp_massive @ git+https://github.com/massive-com/mcp_massive@v0.10.0"
```

The Purelymail entry runs `uvx mcp-email-server==1.9.0 stdio` and uses the server's
[environment configuration](https://mcp-email-server.wh1isper.top/configuration/#environment-variable-reference).
It connects using `purelymail_email` to `imap.purelymail.com:993` and
`smtp.purelymail.com:465` using SSL/TLS with certificate verification, following
[Purelymail's settings](https://support.purelymail.com/support/solutions/articles/159000430778-server-settings-imap-smtp-and-pop3).
Set `purelymail_full_name` to choose the sender display name for outgoing messages.
Sending to any recipient is enabled; the shared agent instructions still require explicit
authorization before sending messages.

To enable it, add your email address and password, plus an optional display name, under `[data]` in
`~/.config/chezmoi/chezmoi.toml`:

```toml
purelymail_full_name = "Your Name" # Optional
purelymail_email = "your-email@example.com"
purelymail_password = "your-mailbox-or-app-password"
```

Run `chezmoi apply` and restart your agent tools. The server is omitted unless the email address and password are
non-empty. Keep your address and password in that local file, not this repository. Like the
other secrets, they are rendered as plaintext into the private MCP configs. No separate email-server UI or credential
store setup is needed; use a fresh environment-based configuration rather than selecting the
server's managed mode, which ignores account environment variables.

Muse Code reads the same servers from `~/.config/muse/settings.json` (managed here as
`dot_config/muse/private_settings.json.tmpl`). Remote servers use `"type": "streamable-http"`
with `url`/`headers`, local servers use `"type": "stdio"` with `command`/`args`/`env`, every
entry carries `"mode": "optional"` so a failing server cannot block startup, and the file
carries `"schema_version": 1`. Never add a `mcp_servers` (snake_case) key next to `mcpServers`:
when both are present Muse drops the whole MCP configuration. Changes take effect on the next
Muse Code launch. Shared skills under `~/.agents/skills/` are already visible to Muse Code as a
skill source alongside its managed `$CONFIG_DIR/skills` store, so no extra skills wiring is needed.

## Browser Automation

The shared agent instructions use `agent-browser` for browser automation. Install the command and
a compatible Chromium browser in the environment, then run `agent-browser --help` before first use.
Agent-browser skills remain a per-project opt-in rather than a global dotfiles installation.
