---
name: improve-prompt
description: Use when the user asks to make a prompt clearer, more effective, more concise, or better aligned with its intended behavior.
---

# Improve Prompt

Improve prompt text in place. Write only what makes the prompt clearer, more specific, and better aligned with the intended output.

## Workflow

1. **Identify the target**: Use the prompt the user pastes or a single named prompt file.
2. **Understand intent**: Use only what the user provides. If the intended behavior is unclear, ask before rewriting.
3. **Rewrite**: Apply the rules below.
4. **Validate**: Confirm every remaining line changes the expected output. If it doesn't, cut it.

## Rewrite Rules

**Keep**: Exact terms, required phrases, constraints, examples, and output format requirements already in the prompt.

**Rewrite**:
- Vague quality words ("clear", "good", "thorough") → specific, observable instructions.
- Long explanations → short commands plus one small example only when the example removes ambiguity.
- Negative rules → preferred behavior when the alternative is unambiguous.

**Consolidate**: Repeated or overlapping rules into one authoritative instruction.

**Move**: Rarely needed details into a separate section when the prompt format supports progressive disclosure.

**Cut**:
- General advice that doesn't change the expected output.
- Background, marketing claims, release notes, and benchmark data.
- Implementation details unless the prompt is specifically about implementation.
- Options, abstractions, fallback behavior, or scope the user did not request.

A good prompt states the task and desired outcome plainly, includes only the context needed to do the task well, makes constraints and output format explicit, and contains no contradictions or duplicates.

## Self-Check

Before finishing:

1. Confirm the rewrite preserves the user's intent.
2. Confirm all required constraints, examples, and output requirements are present.
3. Confirm no instruction is redundant with another.
4. Summarize what changed and why.