---
name: agents-md
description: Create, fix, update, or distill repository- or subtree-scoped agent instructions from codebase evidence. Use for AGENTS.md and alternative instruction files such as CLAUDE.md or GEMINI.md.
---

# AGENTS.md

Create or repair a concise operating guide for agents working in the target directory. Distill
bloated instructions without losing meaningful constraints. Optimize for correct execution, not
for onboarding humans or describing the project.

## 1. Determine Scope

- Use the path requested by the user. Otherwise check the repository root for `AGENTS.md`,
  `CLAUDE.md`, then `GEMINI.md`, and use the first found. If none exists, create `AGENTS.md` there.
- Read the selected file when it exists. Determine whether the request calls for a focused fix,
  an update, or a full distillation; do not rewrite unrelated sections for a narrow repair.
- Read every applicable parent `AGENTS.md` up to the repository root. Add only instructions
  that are more specific than inherited instructions.
- For a subtree file, inspect that subtree rather than documenting unrelated repository areas.
- Treat the selected file as the only target. Inspect sibling instruction files only to identify
  conflicts or tool-specific rules; do not synchronize them unless explicitly requested.

## 2. Gather Evidence

Inspect before writing:

- `README.md`, `CONTRIBUTING.md`, existing instruction files, and relevant docs
- package manifests, lockfiles, task runners, build files, and tool configuration
- CI workflows and hooks for commands that are expected to pass
- representative source and test files for naming, layout, and local patterns
- recent Git history only when commit or pull-request conventions are not documented

Prefer executable configuration and CI over prose when sources disagree. Derive commands
and rules from evidence; never invent missing commands, coverage targets, directory roles,
or contribution requirements.

## 3. Select and Distill Content

Include a fact only when it changes how an agent should work and is not obvious from the
files involved in a normal task. Prioritize:

- exact setup, build, lint, test, formatting, generation, and targeted-test commands
- required tool choices and non-default invocation details
- architecture boundaries, generated-file ownership, and source-of-truth relationships
- test locations, naming rules, fixtures, and verification expectations
- repository-specific safety, security, configuration, and workflow constraints
- commit or pull-request rules only when agents are expected to perform those actions

Omit project history, product descriptions, generic engineering advice, exhaustive directory
trees, and style rules already enforced automatically. Do not duplicate inherited instructions.

For an existing file, classify the relevant rules and sections as **KEEP**, **REWRITE**, or **CUT**:

- **KEEP** accurate, non-obvious commands and flags, unusual import paths or CLI invocations,
  architecture boundaries, external constraints, and MCP configuration with its activation
  conditions. Preserve useful existing stack tables; do not add one merely to summarize the repo.
- **KEEP** correct anti-pattern examples and Wrong/Right blocks verbatim when they teach a
  non-obvious trap. Retain code blocks that demonstrate a required invocation or local pattern.
- **REWRITE** outdated commands or factual claims against current evidence. Extract buried rules
  as short imperatives. Prefer the correct alternative over a bare prohibition, while retaining
  explicit prohibitions when the forbidden action itself is the constraint.
- **CUT** redundant rules, vague directives without an observable outcome, generic advice,
  illustrative padding, large configuration dumps, and obsolete examples. Do not remove an
  explicit user constraint merely because it originated in one incident.
- Resolve contradictions using instruction precedence and repository evidence. If the intended
  policy remains materially unclear, ask instead of silently deleting one side.

Keep rules that apply to a particular kind of task when they prevent mistakes; make their scope
clear rather than requiring every instruction to apply to every task.

## 4. Create or Fix the File

- Use `# Repository Instructions` unless a more specific scope title is useful.
- Choose descriptive sections based on the evidence; do not force a fixed template.
- Put the most operationally important instructions first.
- Write short imperative bullets. Use positive phrasing when it remains precise; use explicit
  prohibitions when the forbidden action itself is the important constraint.
- Show commands in fenced code blocks and paths, filenames, and identifiers in backticks.
- Preserve useful existing section structure when fixing or distilling; remove sections whose
  content is entirely obsolete or redundant.
- Keep the file concise, usually 200-500 words and under 150 lines. Allow more space for necessary
  commands and examples rather than dropping meaningful constraints to meet a line count.
  Omit empty or speculative sections.

Common sections, only when relevant:

```markdown
# Repository Instructions

## Build and Verification
## Project Structure
## Implementation Conventions
## Testing
## Generated Files and Configuration
## Git and Pull Requests
```

Do not default to `# Repository Guidelines`: that framing tends to produce a human contributor
guide. `AGENTS.md` should contain durable instructions that help an agent make correct changes.

## 5. Verify

- Re-read the file against all applicable parent instructions and remove duplication or conflict.
- Confirm every command and factual claim against its source.
- Run cheap, non-destructive commands when practical, such as task-list or help commands.
- Check that every line has a behavioral consequence. Remove anything that merely summarizes
  the repository.
- Save directly to the selected target. Report the path and meaningful changes; for a full
  distillation, include the original and final line counts plus a concise kept/rewritten/cut
  summary. Do not print the entire file unless requested.
