---
name: commit
description: Create a git commit with a message based on the actual diff.
argument-hint: "Optional commit intent, scope, or files to include"
---

# Commit

## Purpose

Create a focused git commit from the current repository changes with a clear message based on the diff.

## Use When

- The user explicitly asks to commit.
- The user explicitly invokes this skill.
- The user provides a commit scope or intent and asks you to turn it into a commit.

## Do Not Use When

- The user only asks for implementation, review, or documentation.
- The working tree contains unrelated changes and the commit scope is unclear.
- Committing would include files outside the user's requested scope.

## Rules

- Never discard, revert, or overwrite user changes.
- If staged changes exist, commit only staged changes unless the user asks otherwise.
- If no staged changes exist, stage only the files that belong to the requested commit.
- Stop and ask if unrelated changes are mixed together.
- Do not mention AI, agents, or this skill in the commit message unless requested.

## Workflow

1. Inspect:
   - `git status --short`
   - `git diff --stat`
   - `git diff`
   - `git diff --cached --stat`
   - `git diff --cached`
2. Decide the commit scope from staged changes, user instructions, and the diff.
3. Stage only the relevant files if needed.
4. Generate a concise conventional commit message when a type fits:
   - `feat`
   - `fix`
   - `docs`
   - `test`
   - `refactor`
   - `chore`
5. Commit with a non-interactive command.
6. Report the commit hash, subject, scope, and verification.

## Message Shape

```text
<type>: <subject>

<short body explaining what changed and why>
```

Keep the subject under 72 characters. Keep the body to one to three short bullets or sentences.

## Completion Rules

Finish only after the commit succeeds or after explaining why no safe commit can be made.
