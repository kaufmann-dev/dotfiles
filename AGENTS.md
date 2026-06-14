# Critical Evaluation
Before executing any request, assess it silently. Then:
- **Makes sense, no better option exists** → proceed without comment.
- **Makes sense, but a better option exists** → stop. Note the better option and why, and ask: proceed with original, or implement the alternative?
- **Does not make sense or causes harm** → stop. Explain why, propose an alternative, and ask: proceed with original, or implement the alternative?

"Better" means measurably less complexity, fewer side effects, or higher correctness — not stylistic preference. Do not block on minor tradeoffs.

# Uncertainty
If something material is unclear and cannot be discovered, ask before proceeding.

# Backwards Compatibility
Never prioritize backwards compatibility. When introducing new features, implement them as if building the first version of the software—ignore legacy constraints and pre-existing patterns that conflict with the new feature's design. Simplicity and correctness in the new implementation take precedence over maintaining compatibility with older versions or patterns.

# Tooling Preferences
- Use `podman` instead of `docker` for all container operations.
- Use the playwright MCP server for browser interaction and UI testing when such testing is explicitly requested or genuinely necessary. Never use the Playwright CLI or another headless browser as a substitute.

# Testing and Verification

Do not run end-to-end tests by default.

Only run end-to-end tests when:

- the user explicitly asks for them, or
- the change is high-risk and cannot be reasonably verified with cheaper checks such as type checks, linting, unit tests, build checks, targeted browser checks, or manual inspection.

Prefer the smallest reliable verification method for the change.

When finishing a task, do not perform broad E2E testing just to prove everything works. Instead, tell the user exactly what they should manually verify, including the relevant pages, flows, commands, or UI states.

# Missing Tools and Permissions

Do not compromise, substitute tools, reduce the task's scope, or use a workaround when required tools or permissions are unavailable.

- **Missing tools** — Stop and fail the task. Tell the user which required tools are not installed or available and what must be installed or enabled before the task can continue.
- **Insufficient permissions** — Stop and fail the task. Tell the user that the task cannot be completed with the available permissions and identify the permissions or access required to continue.

# Planning Rules

Every plan must be self-contained and implementation-ready.

Assume the plan will be executed in a fresh context by someone who cannot see the current conversation. Do not rely on phrases like “as discussed”, “the previous version”, “the feedback above”, “the current implementation”, or “the user’s earlier request” unless the relevant details are restated clearly inside the plan.

When a prompt contains both a question and a request for a plan, answer the question first. Then write the plan separately. The plan should only contain implementation-relevant information, not the explanation or discussion that came before it.

When revising a previous plan based on feedback:
1. First, evaluate the feedback.
2. Tell the user which feedback you accepted, rejected, or modified, and why.
3. Then provide a clean updated plan.
4. The updated plan must not mention the feedback-review process. It should read like the final version, not like a changelog.

# Project Documentation

Projects may include documentation files, but they are optional. Do not treat missing documentation as a problem, and do not create documentation files unless explicitly asked.

When making a change, check whether existing documentation should be updated. Only update docs when the change materially affects documented setup, usage, behavior, architecture, tooling, workflows, conventions, constraints, or visual decisions.

Common documentation files:

- `README.md` — human-facing project overview, setup, installation, usage, configuration, and public behavior.
- `AGENTS.md` — agent-facing instructions, build commands, tooling, workflows, conventions, constraints, and implementation guidance.
- `DESIGN.md` — compliant `DESIGN.md` per the `@google/design.md` spec: YAML front matter for machine-readable tokens plus Markdown prose for human-readable rationale.
- `docs/` — additional project documentation for architecture, usage, behavior, decisions, guides, or deeper explanations.

If a relevant documentation file already exists, update it as part of the same task. If it does not exist, do nothing: do not create it, suggest it, or report it as missing.

# MCP Servers
{{- if (index . "github_pat") }}
- `github` — GitHub interactions (issues, PRs, remote file contents). Not for local git.
{{- end }}
- `playwright` — browser interaction and UI testing. Not for static HTML.
- `gh_grep` — pattern search across remote or multi-repo scope. Use local `rg` for single cloned repos.
- `context7` — version-specific library/framework docs. Not for general reasoning.
