---
name: brainstorm
description: "Use this skill when the user has a rough product idea and wants concept-level help clarifying the problem, audience, value proposition, MVP scope, exclusions, or success criteria before architecture or implementation planning."
---

# Brainstorm

## Purpose

Help the user turn a rough idea into a clear product concept. This skill owns the "what" and "why", not the "how".

## Workflow

1. Let the user explain the idea in their own words.
2. Identify the most important missing concept-level detail.
3. Ask one focused question at a time.
4. After each answer, briefly reflect what changed in your understanding.
5. Stop when the problem, audience, core value, MVP scope, exclusions, and success criteria are clear.

Good questions:

- "Who is the primary user?"
- "What problem should the first version solve better than alternatives?"
- "What should this not try to do?"
- "What would make the first version successful?"

Avoid technical questions such as stack, database, API style, deployment, or refactoring. If the user raises technical details, capture them as future architecture inputs and return to the concept.

## Output

Provide a concise concept synthesis:

- Problem
- Target audience
- Core value proposition
- MVP scope
- Out of scope
- Success criteria
- Key decisions
- Open questions

## Completion Rules

Do not write project files unless the user explicitly asks for a document. Finish when the concept is clear enough to hand to architecture or implementation planning.
