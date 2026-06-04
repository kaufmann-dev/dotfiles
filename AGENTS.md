# Critical Evaluation
Before executing any request, assess it silently. Then:
- **Makes sense, no better option exists** → proceed without comment.
- **Makes sense, but a better option exists** → stop. Note the better option and why, and ask: proceed with original, or implement the alternative?
- **Does not make sense or causes harm** → stop. Explain why, propose an alternative, and ask: proceed with original, or implement the alternative?

"Better" means measurably less complexity, fewer side effects, or higher correctness — not stylistic preference. Do not block on minor tradeoffs.

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

# MCP Servers
{{- if (index . "github_pat") }}
- `github` — GitHub interactions (issues, PRs, remote file contents). Not for local git.
{{- end }}
- `playwright` — browser interaction and UI testing. Not for static HTML.
- `gh_grep` — pattern search across remote or multi-repo scope. Use local `rg` for single cloned repos.
- `context7` — version-specific library/framework docs. Not for general reasoning.

# Skills
- `add-mcp-servers` — add or update project-scoped MCP server configuration entries. Use when the user asks to install, add, change, or synchronize MCP configs for multiple agent tools.
- `add-subagents` — add or update project-scoped subagent definitions. Use when the user asks to install, add, change, or synchronize subagents for multiple agent tools.
- `commit` — makes a git commit. Use only when explicitly requested. Never volunteer it.
- `distill-agents` — distills a bloated AGENTS.md or alternative instruction files into a lean, high-signal version. Use when the user asks to distill instruction files.
- `improve-goal` — improves goals, persistent objectives, and long-running task contracts with measurable criteria and verification steps. Use when the user asks to revise, harden, or debug an objective.
- `improve-prompt` — makes a prompt clearer, more effective, more concise, or better aligned with its intended behavior. Use when the user asks to improve a prompt.
- `md-table-formatter` — formats Markdown tables for consistency. Run every time a markdown table is created or modified, no exceptions.
- `write-readme` / `write-design` / `write-agents` — creates a new README.md, DESIGN.md, or AGENTS.md file from scratch. Use only when creating that file from scratch, never for editing existing files.