---
name: audit-rubric
description: Create a project-specific audit rubric or audit against an existing rubric. Use only when the user explicitly invokes this skill.
---

# Rubric-Based Audit

Operate in exactly one of two modes. Keep every rubric and audit result under `docs/audits/`. Store reusable rubrics separately from dated audit results.

Do not fix code while using this skill.

## Select a Mode

First inspect `docs/audits/` for suitable rubric files and previous audit results. Create `docs/audits/` before writing artifacts if it does not exist, but do not treat an empty directory as an existing rubric.

- Use **Rubric creation mode** when the user explicitly asks for a new rubric, even if a rubric exists. Also use it when no suitable rubric exists.
- Otherwise, use **Audit against existing rubric mode** when a suitable rubric exists or the user asks to audit, re-audit, recheck, verify fixes, or evaluate against a rubric.
- If multiple rubrics exist, choose the most relevant one from its name and content. Ask the user only when ambiguity would make the audit invalid.
- Never reconstruct an existing rubric from memory. Read and reuse the exact rubric file.

## Mode 1: Rubric Creation

1. Inspect the project enough to understand:
   - its public contract and user promises
   - mutation paths
   - configuration and state handling
   - external integrations
   - tests
   - CI and release files
   - real risk surfaces

2. Create a project-specific rubric.
   - Include only pass/fail, evidence-based, user-impacting, realistically verifiable requirements.
   - Do not create generic wishlist categories.
   - Use stable item IDs and this exact item structure:

```text
A1. Concrete requirement
- Pass if ...
- Fail only if ...
- Do not fail merely because ...
```

3. Save the reusable rubric under `docs/audits/`, normally as:

```text
docs/audits/audit-rubric.md
```

4. Immediately perform a full audit against the saved rubric unless the user explicitly asked only to create the rubric.

5. Save the audit as a separate dated document, normally:

```text
docs/audits/YYYY-MM-DD-audit.md
```

If that dated result file already exists, add a short numeric suffix so the new result does not overwrite it.

## Mode 2: Audit Against Existing Rubric

1. Read the exact existing rubric from `docs/audits/`.
2. Read previous audit result documents from `docs/audits/` when present.
3. Determine whether the request is a full audit or a re-audit after fixes.

### Full Audit

- Evaluate every rubric item.
- Do not add, remove, rewrite, or reinterpret rubric items.
- Mark uncertain items as `Not enough evidence`.
- Save the result as a new dated audit document under `docs/audits/`.

### Re-Audit After Fixes

- Use the existing rubric and previous audit findings as the fixed evaluation boundary.
- Determine changed files from version control when available, usually with `git status` and recent diffs. If changed files cannot be determined, inspect the smallest relevant code paths tied to previous failures.
- Inspect only changed files and directly affected behavior where practical.
- Report only unresolved previous failures or regressions caused by the fix.
- If previous audit results contain no failed items, say there were no previous failures to verify and perform only a regression check of directly changed behavior against the existing rubric.
- Do not perform a fresh bug hunt.
- Do not add new rubric categories or lower the failure threshold.
- Save the result as a new dated recheck document, normally:

```text
docs/audits/YYYY-MM-DD-recheck.md
```

If a dated audit or recheck file already exists, add a short numeric suffix so the new result does not overwrite it.

## Evaluate and Verify

- Verify relevant code paths and run focused checks when practical.
- Report a failure only with concrete evidence and realistic user impact.
- If docs and code disagree, identify the public contract before deciding what is wrong.
- Missing tests are defects only when the untested behavior is safety-critical and cannot otherwise be verified.
- Stop when every relevant rubric item has been evaluated.
- Accept this as a successful result:

```text
No actionable defects found under this rubric.
```

## Audit Result Format

State the rubric file used and whether the result is a full audit or recheck. Record the disposition of every relevant rubric item as `Pass`, `Fail`, or `Not enough evidence`.

For every failed rubric item, include exactly:

1. Rubric item ID
2. Severity: critical / high / medium / low
3. Evidence: file, function, and relevant logic
4. Reproduction path or realistic user scenario
5. Why this is a real defect, not a preference
6. Minimal fix
7. Confidence: high / medium / low
8. False-positive risk: low / medium / high

## Severity Rules

- Critical: likely data loss, credential leak, destructive action without consent, remote compromise, or irreversible corruption.
- High: serious user-visible breakage, broken safety boundary, wrong-target mutation, or false success after failure.
- Medium: meaningful public-contract mismatch, important compatibility issue, or missing validation around risky behavior.
- Low: minor concrete user-visible defect with limited impact.

Do not report low-severity issues unless they are concrete, user-visible, and cheap to fix.

## Guardrails

- Do not fix code while using this skill.
- Do not turn the rubric into a wishlist.
- Do not invent rubric items during an audit against an existing rubric.
- Do not treat a re-audit as a fresh bug hunt.
- Prefer minimal fixes over rewrites.
- Treat `No actionable defects found under this rubric.` as a successful result.
