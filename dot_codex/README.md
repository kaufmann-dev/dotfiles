# Codex Configuration

This directory is managed by Chezmoi and maps to `~/.codex`.

## Contents

- `config.toml` - Codex user configuration, including MCP servers copied from OpenCode where Codex supports them.
- `AGENTS.md` - Global Codex guidance copied from the OpenCode instructions.

## Notes

Codex reads skills from `~/.agents/skills`, so shared Codex/OpenCode skills live in `dot_agents/skills` in this repository.

The OpenCode model names were not copied into active Codex settings because the OpenCode config does not include the provider details Codex would need for those custom model IDs.
