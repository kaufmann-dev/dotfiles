# Simplicity First
Write the minimum code that solves the problem.
- Do not add features beyond the request.
- Do not create abstractions for single-use code.
- Do not add configurability that was not requested.
- Do not add defensive handling for impossible scenarios.

# Surgical Changes
Touch only what the request requires.
- Do not refactor adjacent code unless necessary for the task.
- Do not improve unrelated comments, formatting, or dead code.
- Remove only unused code introduced by your own change.
- Preserve unrelated worktree state.
- Every changed line should trace back to the request.

# Critical Evaluation
Before executing any request, assess it silently. Then:
- **Makes sense, no better option exists** → proceed without comment.
- **Makes sense, but a better option exists** → proceed, then note the better option and why.
- **Does not make sense or causes harm** → stop. Explain why, propose an alternative,
  and ask: proceed with original, or implement the alternative?

"Better" means measurably less complexity, fewer side effects, or higher correctness —
not stylistic preference. Do not block on minor tradeoffs.

# Uncertainty
If something material is unclear and cannot be discovered, ask before proceeding.

# Project Documentation Convention
Projects that follow this convention maintain three root-level files with distinct audiences:
- `README.md` — for humans: setup, usage, context
- `AGENTS.md` — for AI agents: instructions, constraints, workflow
- `DESIGN.md` — for visual decisions: design tokens and style rationale per Google Material spec

These files may not exist in every project. Do not create them unless explicitly asked.
Treat their presence as opt-in. If they exist, respect their structure and purpose.

# Post-Change Documentation Sync
After completing any change, check whether each documentation file exists in the project root.
For each one that exists, silently assess whether the change affects its content:
- `README.md` — update if setup steps, public API, or usage behavior changed
- `DESIGN.md` — update if tokens, component styles, or visual decisions changed
- `AGENTS.md` — update if build commands, tooling, conventions, or constraints changed

If an update is needed and the file exists, make it as part of the same task.
Do not ask for permission. Do not mention it unless something is ambiguous.
If a file does not exist, do nothing — do not create it, do not suggest creating it.

# Package Manager
Use `pnpm` instead of `npm` for new projects.

# MCP Servers
{{- if (index . "github_pat") }}
- `github` — GitHub interactions (issues, PRs, remote file contents). Not for local git.
{{- end }}
- `playwright` — browser interaction and UI testing. Not for static HTML.
- `gh_grep` — pattern search across remote or multi-repo scope. Use local `rg` for single cloned repos.
- `context7` — version-specific library/framework docs. Not for general reasoning.

# Skills
- `add-mcp-servers` — add or update project-scoped MCP server configuration entries for multiple agent tools.
- `write-readme` / `write-design` / `write-agents` — only when creating that file from scratch.
  For edits to existing files, apply changes directly (see Post-Change Documentation Sync).
- `md-table-formatter` — every time a Markdown table is created or modified, no exceptions.
- `commit` — only when explicitly requested. Never volunteer it.
