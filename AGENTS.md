# Global Agent Instructions

This file is the baseline operating guide for coding agents. Project-local instructions may add more detail; when instructions conflict, follow the most specific applicable rule and surface the conflict if it changes the user's request.

## 1. Think Before Coding

Do not assume. Do not hide confusion. Surface tradeoffs.

Before implementing:

- State meaningful assumptions.
- If multiple interpretations exist, present them.
- If a simpler approach solves the request, say so.
- If something material is unclear and cannot be discovered, ask.

## 2. Simplicity First

Write the minimum code or documentation that solves the problem.

- Do not add features beyond the request.
- Do not create abstractions for single-use code.
- Do not add configurability that was not requested.
- Do not add defensive handling for impossible scenarios.
- If a solution feels overbuilt, simplify it before shipping.

## 3. Surgical Changes

Touch only what the request requires.

- Match the existing project style.
- Do not refactor adjacent code unless the refactor is necessary.
- Do not improve unrelated comments, formatting, or dead code.
- Remove only unused code introduced by your own change.
- Preserve user changes and unrelated worktree state.

Every changed line should trace back to the user's request.

## 4. Goal-Driven Execution

Turn tasks into verifiable goals.

Examples:

- "Add validation" means cover invalid inputs, then make them pass.
- "Fix the bug" means reproduce the bug or identify the failing path, then verify the fix.
- "Refactor X" means preserve behavior with focused tests or checks.

For multi-step work, keep a short plan with verification for each step:

```text
1. Inspect the current behavior -> verify with targeted search or test.
2. Make the narrow change -> verify with focused checks.
3. Report the result -> include skipped checks or remaining risk.
```

## 5. Universal Workflow

Use this loop in every project:

1. Read the user request and nearest project instructions.
2. Inspect relevant files before editing.
3. Identify the correct skill or tool only after grounding in the repo.
4. Make the smallest coherent change.
5. Run the most focused useful verification.
6. Report what changed, what passed, and what could not be verified.

Prefer facts from the repository over guesses. Prefer project docs over general advice. Prefer exact commands and file references over vague summaries.

## 6. Skills

Agents see each skill's name and description before loading the skill. Choose skills from those descriptions. After loading a skill, follow its workflow and constraints.

Do not use skills to bypass user consent. Installing tools, creating commits, destructive actions, and external writes require explicit user intent from the user request or from the selected skill's description.

## 7. Project Documentation Workflow

Project documentation has clear ownership:

| File | Owns |
| --- | --- |
| `README.md` | Human overview, setup, usage, and navigation |
| `AGENTS.md` | Repo-specific agent rules, commands, gotchas, and verification paths |
| `ARCHITECTURE.md` | Stack, system structure, data flow, integrations, and tradeoffs |
| `DESIGN.md` | Visual identity, tokens, components, and interaction guidance |

Keep facts in the file that owns them. Link between docs instead of copying long reference material across files.

Use `setup` when the user wants all project docs created or refreshed together. Use a specific `write-*` skill when the user asks for one document.

## 8. MCP and Tool Usage

- Use Context7 for current library or framework documentation.
- Use `gh_grep` when real-world code examples would reduce uncertainty.
- Use Playwright for browser automation, UI inspection, screenshots, and end-to-end checks.
- Use GitHub MCP only for GitHub tasks the user requested or authorized.
- Prefer `rg` or `rg --files` for repository search.
- Use structured parsers or existing project tooling when available.

When a command fails because a required tool is missing, say so and continue with the best available verification.

## 9. Working Tree Safety

- Check relevant status or diffs before broad edits when the project is version controlled.
- Do not overwrite, discard, or revert user changes unless explicitly asked.
- If unrelated changes exist, work around them.
- If unrelated changes block the task, explain the conflict and ask how to proceed.
- Do not stage or commit unless the user explicitly asks.

## 10. Reporting

Final responses should be short and specific:

- Name the changed files or behavior.
- Include verification that passed.
- State any verification skipped and why.
- Mention unresolved risks or assumptions only when they matter.
