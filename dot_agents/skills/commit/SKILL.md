---
name: commit
description: Use only when the user explicitly asks to commit.
---

# Commit

Never discard, revert, or overwrite user changes.

## Inspect
```bash
git status --short && git diff --stat && git diff && git diff --cached --stat && git diff --cached
```

## Scope
- Staged changes exist -> commit only staged.
- Nothing staged -> stage only files relevant to the request.
- Unrelated changes are mixed -> ask before proceeding.

## Message
```text
<type>(<scope>): <subject, max 72 chars>

<1-3 sentences: what changed and why>
```
Types: `feat` `fix` `docs` `refactor` `test` `chore`

Do not mention AI, agents, or tooling in the message.
Commit non-interactively. Finish only after the commit succeeds or after explaining why no safe commit can be made.
