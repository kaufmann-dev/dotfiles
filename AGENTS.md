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

## Debugging

This section applies only when you are reviewing, fixing or hunting bugs. Skip it otherwise.

**Before touching code,** read `docs/bugs/*.md` to learn from previously resolved issues and avoid repeating past mistakes

- Find the root cause before changing code; do not ship a fix you cannot explain.
- For runtime, behavioral, or "data is wrong/lost" bugs, reasoning from source alone about reactivity, event ordering, async timing, or framework internals is frequently plausible and wrong. Reproduce and observe the running system before writing a fix — for these bugs that is the cheapest reliable way to find the cause, not the most expensive.
- For "data lost" bugs, inspect the datastore directly to separate a save failure from a display failure: the value on screen and the row in storage can disagree, and which one is wrong tells you where the bug lives.
- For code that maps an external API or data shape, verify field names and types against a real response (curl the endpoint, log the raw payload). Do not trust the names already in the code.
- A passing test is not proof when its fixtures or mocks encode the same assumption as the code under test. A mock that reuses the code's own (wrong) field name makes a broken mapping look correct. When tests are green but behavior is broken, suspect the fixtures.
- If two or more fixes have failed, stop patching. The diagnosis is wrong, not the fix. Restart from reproduction and confirm the actual cause before touching code again.
- State the confirmed cause and the evidence that proves it before proposing the fix.

**After a confirmed fix:** create `docs/bugs/<descriptive-symptom>.md` documenting (a) the symptom, (b) the root cause you confirmed, (c) the exact changes made.

## Development Servers and Containers

Before starting a development server or container, reuse an existing one for this project instead of spawning a duplicate.

1. **Check first.** Enumerate instances already running for *this project* — match containers by project name / label / compose project (`podman ps`); match dev servers by the project's expected port or process command.

2. **Act on the count:**
- **None running** → start exactly one.
- **Exactly one running** → use it. Do not start another.
- **More than one running** → keep exactly one and terminate the rest, then use the kept one. Keep a healthy, responding instance; if several are equally healthy, keep the oldest and stop the newer duplicates.

If the instance you keep is unresponsive, restart that one rather than leaving a broken server in place.

## Testing and Verification

After any change, confirm it with the smallest reliable check, preferring in this order: type check → lint → targeted unit test → build → targeted manual or browser check. (Reproducing a bug to diagnose it is a separate activity; see Debugging.)

Do not run end-to-end tests by default. Run them only when:

- the user explicitly asks for them, or
- the change is high-risk and cannot be verified by any cheaper check above.

## Missing Tools and Permissions

Do not substitute tools, reduce the task's scope, or improvise a workaround when a required tool or permission is unavailable. Stop and fail the task.

- **Missing tool** → stop. Tell the user which required tool is unavailable and exactly what must be installed or enabled before the task can continue.
- **Insufficient permissions** → stop. Tell the user the task cannot complete with the current access, and name the exact permissions or access required to continue.

## Planning Rules

Every plan is self-contained and implementation-ready. Assume it will be executed in a fresh context by someone who cannot see this conversation. Restate any needed detail inside the plan; never rely on "as discussed", "the previous version", "the current implementation", or "the earlier request".

- When a prompt contains both a question and a request for a plan, answer the question first, then write the plan separately. The plan contains only implementation-relevant information — none of the preceding discussion.
- When revising a plan from feedback: (1) evaluate the feedback; (2) tell the user which items you accepted, rejected, or modified, and why; (3) then give a clean updated plan. The updated plan reads as the final version, not a changelog — it must not mention the revision process.

## Project Documentation

Projects may include documentation files (e.g. `AGENTS.md`, `README.md`, `DESIGN.md`, `docs/*.md`). Do not treat missing documentation as a problem, and do not create documentation unless explicitly asked.

- When a change materially affects documented setup, usage, behavior, architecture, tooling, workflows, conventions, constraints, or visual decisions, update the existing documentation in the same task.
- If the relevant documentation does not already exist, do nothing.
