# Unrestricted agent launchers.
#
# POSIX-compatible (bash and zsh). On Linux and macOS, chezmoi adds this
# source line to ~/.bashrc and ~/.zshrc:
#
#   source ~/.config/shell/agent-aliases.sh
#
# Codex needs no wrapper: dot_codex/private_config.toml.tmpl already sets
# approval_policy = "never" with full-access default permissions.
#
# These wrappers disable real protections. Do not use them on untrusted
# checkouts (forks, PR branches): agent instructions and skills there are
# attacker-controlled content.

muse() {
  command muse --yolo "$@"
}

agy() {
  command agy --dangerously-skip-permissions "$@"
}

claude() {
  command claude --dangerously-skip-permissions "$@"
}
