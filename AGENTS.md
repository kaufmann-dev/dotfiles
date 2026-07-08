# Global Instructions

## Critical Evaluation
Assess every request silently before acting, then:
- **No materially better option exists** → proceed without comment.
- **Materially better option exists** → stop. State the better option, why it is better, and ask: proceed with the original, or switch to the alternative?

"Materially better" means measurably less complexity, fewer side effects, or higher correctness — not stylistic preference. Do not block on minor tradeoffs.

## Uncertainty
If something material is unclear and cannot be discovered, ask before proceeding.

## Backwards Compatibility
- Never preserve backwards compatibility when building a new feature. Implement it as the first and only version.
- Delete or replace conflicting legacy patterns.
- Do not add compatibility shims, dual paths, flags, or aliases unless explicitly requested.

## Tooling Preferences
- Use `podman` instead of `docker` for all container operations.
- Use the `playwright` MCP server for browser interaction and UI testing when such testing is explicitly requested or genuinely necessary. Never use the Playwright CLI or another headless browser as a substitute.
- Use the `gh_grep` MCP server to search public GitHub code for concrete patterns; use local `rg` for a single cloned repository.
- Use the `context7` MCP server for version-specific library or framework documentation.
- {{- if (index . "github_pat") }} Use the `github` MCP server for GitHub interactions such as issues, PRs, and remote file contents; use local git for local repository operations. {{- end }}
- {{- if (index . "massive_api_key") }} Use the `massive` MCP server for stock market data. {{- end }}
- {{- if (index . "portfolio_arena_api_key") }} Use the `portfolio_arena` MCP server for Portfolio Arena data and admin operations. {{- end }}

## Development Servers and Containers

Only start a development server or container if the user explicitly asks for it, or if it is genuinely important for testing and verification.

Before starting a development server or container, enumerate instances already running for *this project*. Then, **act on the count:**
- **None running** → start exactly one.
- **Exactly one running** → use it. Do not start another.
- **More than one running** → keep exactly one and terminate the rest, then use the kept one. Keep a healthy, responding instance; if several are equally healthy, keep the oldest and stop the newer duplicates.

If the instance you keep is unresponsive, restart that one rather than leaving a broken server in place.

## Testing and Verification

After any change, confirm it with the smallest reliable check, preferring in this order: type check → lint → targeted unit test → build → targeted manual or browser check. (Reproducing a bug to diagnose it is a separate activity; see Debugging.)

If a chosen check reports unrelated or pre-existing issues, fix them too instead of ignoring them or limiting fixes to touched files, then rerun the check.

Do not run end-to-end tests by default. Run them only when:
- the user explicitly asks for them, or
- the change is high-risk and cannot be verified by any cheaper check above, or
- the check cannot be done more cheaply by asking the user to verify it themselves.

## Commits

After completing requested file changes, automatically create one commit on the current branch unless the user explicitly says not to:

```sh
git add -A
git commit -m "<subject>"
```

Do not run git status, git fetch, git pull, repository discovery, or extra pre-commit inspection as part of committing.

Choose `<subject>` from the work just completed. It must be a Conventional Commit subject, lowercase, present tense, no trailing period, no newline, and at most 120 characters:
- feat(scope): add thing
- fix(scope): handle thing
- docs(scope): update thing
- chore(scope): adjust thing

Allowed types are feat, fix, docs, style, refactor, test, chore, perf, ci, build, and revert. Use an optional scope when it makes the commit clearer.

## Missing Tools and Permissions

Do not substitute tools, reduce the task's scope, or improvise a workaround when a required tool or permission is unavailable. Stop and fail the task.

- **Missing tool** → stop. Tell the user which required tool is unavailable and exactly what must be installed or enabled before the task can continue.
- **Insufficient permissions** → stop. Tell the user the task cannot complete with the current access, and name the exact permissions or access required to continue.

## Planning Rules

Every plan is self-contained and implementation-ready. Assume it will be executed in a fresh context by someone who cannot see this conversation. Restate any needed detail inside the plan; never rely on "as discussed", "the previous version", "the current implementation", or "the earlier request".

- When a prompt contains both a question and a request for a plan, answer the question first, then write the plan separately. The plan contains only implementation-relevant information — none of the preceding discussion.
- When revising a plan from feedback: (1) evaluate the feedback; (2) tell the user which items you accepted, rejected, or modified, and why; (3) then give a clean updated plan. The updated plan reads as the final version, not a changelog — it must not mention the revision process.

## Project Documentation

Do not create documentation unless explicitly asked.

After changing project files:

- Check existing Markdown documentation with `git ls-files -- '*.md' ':!docs/bugs/**' ':!.*/**' ':!**/.*/**'`.
- Use the listed filenames to judge whether the changes just made could affect any existing documentation.
- Do not read every Markdown file automatically. First judge from the filenames and the nature of the change.
- If a Markdown file may describe the changed setup, behavior, architecture, tooling, workflow, conventions, constraints, or visual design, read that file and update it in the same task.
- If no existing Markdown file appears relevant, do nothing.

Do not finish with documentation that is outdated or contradicted by the changes just made.