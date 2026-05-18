---
name: brainstorm
description: Refine rough product ideas through concept-level questioning before implementation planning.
---

# Brainstorm

## Purpose

Help the user turn a rough idea into a clear product concept. This skill owns the "what" and "why", not the "how".

## Use When

- The user has an early idea and wants to shape it.
- The request is about audience, value proposition, MVP scope, or success criteria.
- The user is not ready for architecture, implementation, or code changes.

## Do Not Use When

- The user is asking for code, architecture, stack selection, or refactoring.
- The user already supplied a clear concept and wants execution.
- The task is a documentation rewrite that can be handled directly or with a `write-*` skill.

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
