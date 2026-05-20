---
name: improve-goal
description: Improve goals, persistent objectives, and long-running task contracts. Use when the user asks to revise, harden, or debug an objective with measurable success criteria, verification steps, constraints, or stop conditions.
---

# Improve Goal

Improve goal text in place. Write only what makes the objective clearer, more measurable, and easier to verify.

## Workflow

1. **Identify the target**: Use the goal text the user pastes, a named goal file, or multiple goal files if the project specifies more than one target objective.

2. **Check project context**: If a workspace is active, inspect the top-level structure only (package manager files, build configs, directory layout) to validate that commands and paths mentioned in the goal actually exist. Do not read source code or deep configs. If no workspace is active, rely entirely on what the user has provided in the chat.

3. **Handle vagueness**:
   - **Assumable** — If success criteria can be inferred from common best practices for the project type, rewrite the goal and flag those assumptions explicitly.
   - **Ambiguous** — If success criteria cannot be safely inferred, ask clarifying questions before rewriting.

4. **Rewrite**: Structure the goal as a concise persistent objective with clear success criteria, verification, constraints, and stop conditions. Apply the rules below.

5. **Validate**: Confirm every instruction is actionable, scoped, and durable across turns.

## Rewrite Rules

**Keep**: Exact commands, paths, tool names, budgets, thresholds, constraints, and completion criteria already in the goal.

**Rewrite**:
- Vague outcomes → measurable success criteria with an inspectable verification surface (tests, benchmarks, logs, artifacts, citations).
- Broad research or debugging requests → objective plus named evidence to collect.
- Long explanations → concise instructions with one small example only when necessary.

**Move**: Rarely needed background into referenced files. Long checklists into the success/verification structure.

**Cut**:
- General advice not specific to this goal.
- Tutorial sections and product framing.
- Implementation plans that will be stale after the first turn.
- Assumptions inferred from nearby project files rather than from the goal itself.
- Defensive handling, configurability, or alternate paths the user did not request.

A good goal fits long-running work where the next step depends on evidence gathered along the way. It states completion as an observable outcome, names the verification surface, preserves scope and safety constraints, and defines when to stop or ask before continuing.

## Output Pattern

Use this structure unless the user specifies another format.

```md
Goal:
<action-oriented objective>

Success means:
- <observable final state>

Verify by:
- <tests, benchmark, artifact review, logs, source citations, or other evidence>

Constraints:
- <scope, safety, quality, budget, or process constraints>

Stop or ask before:
- <conditions that require user input or should end the goal>
```

Custom sections (such as **Phases** or **Technical Details**) may follow the five core sections for complex tasks.

## Self-Check

Before finishing:

1. Confirm the frontmatter or instruction-file structure still matches the target format.
2. Confirm all original commands, constraints, thresholds, and priority rules are present.
3. Confirm no section is copied wholesale from reference material.
4. Summarize what changed and why.