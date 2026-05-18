---
name: commit
description: Create a git commit with an AI-generated name and description based on the actual changes.
argument-hint: "Optional commit intent, scope, or files to include"
---

# AI Commit Writer

Create a git commit whose subject and body are generated from the repository changes. The commit message must describe what changed and why, without inventing intent that is not visible in the diff or provided by the user.

## Workflow

### 1. Inspect the Repository

Run:

```bash
git status --short
git diff --stat
git diff
git diff --cached --stat
git diff --cached
```

If the user passed arguments, treat them as guidance for the intended commit scope or message emphasis.

### 2. Decide What to Commit

- If staged changes exist, commit only the staged changes unless the user explicitly asks to include unstaged files.
- If no staged changes exist but unstaged changes do, stage the relevant changed files before committing.
- If the user named specific files, stage and commit only those files.
- If there are no changes, stop and say there is nothing to commit.
- If unrelated changes are mixed together, stop and ask which changes belong in this commit.

Never discard, revert, or rewrite user changes.

### 3. Generate the Commit Message

Write a concise commit message from the diff:

```text
<type>: <subject>

<description>
```

Use a conventional commit type when it fits:

- `feat` for user-visible functionality
- `fix` for bug fixes
- `docs` for documentation-only changes
- `test` for tests
- `refactor` for behavior-preserving code changes
- `chore` for maintenance or tooling

Rules:

- Keep the subject under 72 characters.
- Use imperative mood when natural.
- Make the description 1-3 short bullet points or sentences.
- Mention important verification if it was run.
- Do not mention AI, Codex, or the skill unless the user asked for that.
- Do not add vague filler such as "update files" or "misc changes."

### 4. Create the Commit

Run the commit with the generated message. Prefer a non-interactive command such as:

```bash
git commit -m "<subject>" -m "<description>"
```

If the commit fails, explain the failure and do not retry with unrelated changes.

### 5. Report the Result

Reply with:

- the commit hash
- the generated subject
- a brief summary of what was committed
- any verification that was run or skipped

Keep the final response short.
