# Dotfiles

My personal dotfiles, managed with [Chezmoi](https://www.chezmoi.io/) for cross-platform compatibility.


## Structure

```text
dotfiles/
└── dot_config/         # Maps to ~/.config (or %USERPROFILE%\.config)
    └── opencode/       # OpenCode configuration
        ├── agents/
        ├── skills/
        └── rules/
```

New tool directories can be added inside `dot_config/` (or with other top-level mappings) as needed. For example, `dot_config/git/` would map to `~/.config/git/`.

## How Chezmoi Maps Files

Chezmoi translates special prefixes in the source directory to paths in your home directory:

| Source prefix | Destination |
|---------------|-------------|
| `dot_` | `.` (hidden file/directory) |
| `private_` | Sets file permissions to `600` |
| `executable_` | Sets file as executable (`755`) |
| `literal_` | Removes the prefix literally (useful for files literally named `dot_...`) |
| `symlink_` | Creates a symlink instead of a regular file |

Because the source path is `dot_config/opencode/`, Chezmoi will create and manage `%USERPROFILE%\.config\opencode\` on Windows and `~/.config/opencode/` on macOS and Linux.

## Prerequisites

*   [Chezmoi](https://www.chezmoi.io/install/)

## Setup

### 1. Initialize Chezmoi with this repository

```bash
# macOS / Linux / Windows
chezmoi init --apply https://github.com/kaufmann-dev/dotfiles.git
```

Or, if working with a local copy:

```bash
# macOS / Linux
chezmoi init --source-path /absolute/path/to/this/repo

# Windows (PowerShell)
chezmoi init --source-path C:\absolute\path\to\this\repo
```

### 2. Apply the configurations

```bash
chezmoi apply
```

## Automating Updates

To keep OpenCode configurations continuously in sync across machines without slowing down your workflow, you can wrap the launch command to update your dotfiles **asynchronously** in the background.

### macOS and Linux (Bash / Zsh)

Copy and paste the appropriate command for your shell to automatically set up the function and reload your profile:

**For Bash:**
```bash
echo 'opencode() { chezmoi update > /dev/null 2>&1 & command opencode "$@"; }' >> ~/.bashrc && source ~/.bashrc
```

**For Zsh:**
```sh
echo 'opencode() { chezmoi update > /dev/null 2>&1 & command opencode "$@"; }' >> ~/.zshrc && source ~/.zshrc
```

### Windows (PowerShell)

Copy and paste this command into PowerShell to automatically create/update your profile and reload it:

```powershell
if (!(Test-Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }; Add-Content -Path $PROFILE -Value "`nfunction opencode { Start-Process -WindowStyle Hidden -FilePath 'chezmoi' -ArgumentList 'update'; & 'opencode.exe' @args }"; . $PROFILE
```

## Daily Usage

| Command | Description |
|---------|-------------|
| `chezmoi apply` | Apply changes from the source directory to the system. |
| `chezmoi diff` | Preview changes without applying them. |
| `chezmoi edit <file>` | Edit a managed file in the source directory. |
| `chezmoi re-add` | Update the source directory with changes made to target files. |
| `chezmoi update` | Pull the latest changes from the remote repository and apply them. |

## Cross-Platform Notes

Chezmoi supports templating and conditional logic. Platform-specific configurations can be handled with templates (e.g., `{{ if eq .chezmoi.os "darwin" }}...{{ end }}`).

For more details, see the [Chezmoi documentation](https://www.chezmoi.io/docs/).
