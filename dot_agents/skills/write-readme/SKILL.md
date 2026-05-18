---
name: write-readme
description: Use only when creating README.md from scratch. Never for editing existing files.
---

# Write README

## Before Writing
Read config files first: `package.json`, `pyproject.toml`, `Makefile`, `Dockerfile`, `.env.example`.
Derive the project name, description, and commands from them — do not invent.

## Structure
```
# Project Name
> One-line description

## Contents
<anchor links to every H2 below>

## Installation
## Usage
## Configuration
## API / Reference
## Contributing
## License
```

## Rules
- `Contents` always appears after the title block, before any other section.
- `Installation` and `Usage` are required if anything must be installed or run.
  Use the actual package manager found in lockfiles.
- Combine macOS/Linux and Windows commands in a single code block, using comments to separate OSes.
- `Configuration` only if config options exist.
- `API / Reference` only for libraries.
- `Contributing` — one sentence; link `CONTRIBUTING.md` if it exists.
- `License` — one line; link `LICENSE` if it exists.
- Omit sections that do not apply. No placeholder sections.
- After writing, run `md-table-formatter` on any tables present.