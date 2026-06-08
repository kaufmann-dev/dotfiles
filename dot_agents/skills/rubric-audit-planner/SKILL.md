---
name: rubric-audit-planner
description: Use in plan mode to inspect a project and create a project-specific audit rubric plus a bounded audit prompt. Use when the user wants a rubric-based audit, wants to avoid endless AI nitpicking, or explicitly invokes this skill.
---

# Rubric Audit Planner

Create a project-specific rubric and a ready-to-run audit prompt that makes an AI evaluate fixed criteria instead of hunting for problems.

Do not fix code. Do not create an implementation plan unless the user asks.

## Workflow

1. Inspect the project enough to understand its public contract and real risk surfaces.
   - Read docs, entry points, config/state handling, mutation paths, external integrations, tests, CI/release files, and any safety-sensitive code that exists.
   - Do not include generic categories unless the project actually needs them.

2. Summarize:
   - what the project does
   - what users are promised
   - where failure would matter

3. Build a rubric from those risks.
   - Each item must be project-specific, pass/fail, evidence-based, user-impacting, and realistically verifiable.
   - Use this form:

```text
A1. Concrete requirement
- Pass if ...
- Fail only if ...
- Do not fail merely because ...
```

4. Generate a standalone audit prompt that tells the next agent:
   - evaluate only this rubric
   - do not invent new categories
   - do not report style preferences, speculative refactors, or theoretical edge cases
   - report a failure only with concrete evidence and realistic user impact
   - mark uncertainty as "Not enough evidence"
   - accept "No actionable defects found under this rubric" as success

5. Add re-audit rules:
   - use the same rubric
   - inspect only changed files and directly affected behavior
   - report only unresolved original failures or regressions from the fix
   - do not lower the threshold or add new categories

## Required Finding Format

Every failed rubric item in the generated audit prompt must require:

1. Rubric item ID
2. Severity: critical / high / medium / low
3. Evidence: file, function, and relevant logic
4. Reproduction path or realistic user scenario
5. Why this is a real defect, not a preference
6. Minimal fix
7. Confidence: high / medium / low
8. False-positive risk: low / medium / high

Only recommend implementation for findings with concrete user impact, high or medium confidence, and low or medium false-positive risk.

## Severity Rules

- Critical: likely data loss, credential leak, destructive action without consent, remote compromise, or irreversible corruption.
- High: serious user-visible breakage, broken safety boundary, wrong-target mutation, or false success after failure.
- Medium: meaningful public-contract mismatch, important compatibility issue, or missing validation around risky behavior.
- Low: minor concrete user-visible defect with limited impact.

Do not report low-severity issues unless they are concrete, user-visible, and cheap to fix.

## Output Format

```text
# Rubric-Based Audit Plan

## Project Understanding
...

## Risk Surfaces
...

## Audit Rubric
...

## Ready-To-Run Audit Prompt
...

## Re-Audit Rules
...
```

## Guardrails

- The rubric is not a wishlist.
- Missing tests are defects only when the untested behavior is safety-critical and cannot otherwise be verified.
- Prefer minimal fixes over rewrites.
- If docs and code disagree, identify the public contract before deciding what is wrong.
- Stop at the rubric. Do not keep auditing indefinitely.