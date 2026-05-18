---
name: commit
description: Use only when the user explicitly asks to commit.
---

# Commit

## Inspect
```bash
git status --short && git diff --stat && git diff && git diff --cached
```

## Scope
- Staged changes exist → commit only staged.
- Nothing staged → stage only files relevant to the request.
- Unrelated changes are mixed → ask before proceeding.

## Message
```
<type>(<scope>): <subject, max 72 chars>

<1–3 sentences: what changed and why>
```
Types: `feat` `fix` `docs` `refactor` `test` `chore`

Do not mention AI, agents, or tooling in the message.