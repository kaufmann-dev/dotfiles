---
name: handoff
description: "Use this skill only when the user explicitly asks for a handoff, context summary, continuation note, or document for another agent or future session to continue the work."
argument-hint: "What the next session should focus on"
---

# Handoff

## Purpose

Summarize the current work so a fresh agent can continue without rereading the entire conversation.

## Workflow

1. Identify the next session's likely goal from the user request.
2. Summarize only information needed to resume work:
   - Goal
   - Current state
   - Important files
   - Decisions made
   - Commands run
   - Verification status
   - Remaining tasks
3. Reference existing artifacts by path or URL instead of copying them.
4. Suggest relevant skills for the next session when useful.
5. Save the handoff as a temporary Markdown file unless the user requested a specific path.

## Output

Report the handoff file path and a one-sentence summary of what it covers.

## Completion Rules

Use this skill only by explicit opt-in. Do not write a handoff into the repository unless the user asks for that location.
