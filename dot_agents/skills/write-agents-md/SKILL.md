---
name: write-agents-md
description: Create a missing repository- or subtree-scoped AGENTS.md from evidence in the codebase. Use only when the user explicitly invokes this skill or asks to create agent instructions.
---

# Write AGENTS

Create a concise operating guide for agents working in the target directory. Optimize
for correct execution, not for onboarding humans or describing the project.

## 1. Determine Scope

- Use the path requested by the user. Otherwise create `AGENTS.md` at the repository root.
- Stop if the target file already exists; use an editing or distillation workflow instead.
- Read every applicable parent `AGENTS.md` up to the repository root. Add only instructions
  that are more specific than inherited instructions.
- For a subtree file, inspect that subtree rather than documenting unrelated repository areas.

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

## 3. Select Content

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

## 4. Write the File

- Use `# Repository Instructions` unless a more specific scope title is useful.
- Choose descriptive sections based on the evidence; do not force a fixed template.
- Put the most operationally important instructions first.
- Write short imperative bullets. Use positive phrasing when it remains precise; use explicit
  prohibitions when the forbidden action itself is the important constraint.
- Show commands in fenced code blocks and paths, filenames, and identifiers in backticks.
- Keep the file concise, usually 200-500 words, but let necessary commands and constraints
  determine length. Omit empty or speculative sections.

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
