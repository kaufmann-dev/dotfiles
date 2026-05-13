# Dotfiles

This repository manages system and application configurations across **macOS**, **Linux**, and **Windows** using [Chezmoi](https://www.chezmoi.io/).

## Structure

The repository is organized by tool, making it easy to expand in the future:

```text
dotfiles/
└── dot_config/         # Maps to ~/.config (or %USERPROFILE%\.config)
    └── opencode/       # OpenCode configuration
        ├── agents/
        ├── skills/
        └── rules/
```

**Note:** You can add new tool directories inside `dot_config/` (or create other top-level mappings) as needed. For example, `dot_config/git/` would map to `~/.config/git/`.

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

*   [Chezmoi](https://www.chezmoi.io/install/) must be installed on your system.

## Setup

### 1. Initialize Chezmoi with this repository

If you are cloning from a remote URL (replace `<username>` with your GitHub username):

```bash
# macOS / Linux / Windows
chezmoi init --apply [https://github.com/](https://github.com/)<username>/dotfiles.git
```

### 2. Apply the configurations

After initialization, apply the dotfiles to your system:

```bash
chezmoi apply
```

## Automating Updates

To ensure your configurations are always up to date across all machines, you can wrap your OpenCode launch command. This forces Chezmoi to pull any new GitHub changes right before the agent starts.

### macOS and Linux
Add this alias to your `~/.bashrc` or `~/.zshrc` file:

```bash
alias opencode="chezmoi update && command opencode"
```

### Windows
Add this function to your PowerShell profile (run `notepad $PROFILE` to edit it):

```powershell
function opencode {
    chezmoi update
    & "opencode.exe" @args
}
```

## Daily Usage

| Command | Description |
|---------|-------------|
| `chezmoi apply` | Apply any changes from the source directory to your system. |
| `chezmoi diff` | See what changes would be applied without making them. |
| `chezmoi edit <file>` | Edit a managed file in the source directory. |
| `chezmoi re-add` | Update the source directory with changes made to the target files. |
| `chezmoi update` | Pull the latest changes from the remote repository and apply them. |

## Cross-Platform Notes

Chezmoi supports templating and conditional logic. If you need platform-specific configurations in the future, you can use Chezmoi templates (e.g., `{{ if eq .chezmoi.os "darwin" }}...{{ end }}`) within your configuration files.

For more details, see the [Chezmoi documentation](https://www.chezmoi.io/docs/).