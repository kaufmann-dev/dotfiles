# Chezmoi Hook Exec Format Error

- Fixed: 2026-07-29 12:50:00 UTC (+0000)
- Commit before fix: `6d5ea7f04b18a4772e6d577dd6380313eecf95f9`

## Symptom

`chezmoi update` pulled the repository but failed while applying with:

```text
chezmoi: 10_secure_chezmoi_config.sh: fork/exec ...: exec format error
```

## Root Cause

The opening Go-template action in
`run_before_10_secure_chezmoi_config.sh.tmpl` did not trim its following
newline. The rendered executable therefore started with a blank line instead
of `#!/bin/sh`, so the operating system could not identify its interpreter.

## Fix

Added right-side whitespace trimming to the opening template action. The
rendered hook now starts with the shell shebang as its first bytes.
