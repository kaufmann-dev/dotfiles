---
name: audit-defect
description: Directly audit a codebase for concrete, actionable defects. Use when the user asks for an immediate audit, defect review, bug hunt, safety review, or explicitly invokes this skill.
---

# Actionable Defect Audit

Audit the codebase directly for concrete, actionable defects.

This is the problem-finder counterpart to a rubric-based audit. It is less constrained than a rubric audit, so keep the scope strict and avoid inventing issues.

Do not fix code while using this skill.

## Scope

Look only for:

- correctness bugs
- security issues
- data loss risks
- broken documented behavior
- race conditions
- test failures
- user-visible regressions
- unsafe mutation or recovery behavior
- serious automation/scriptability breakage

Do not report:

- style preferences
- speculative refactors
- theoretical edge cases without a plausible user path
- issues already handled by existing behavior
- “could be cleaner” maintainability comments
- missing tests unless the untested behavior is safety-critical and cannot otherwise be verified

## Workflow

1. Inspect enough of the project to understand its public contract and risky code paths.
   - Read relevant docs, entry points, config/state handling, mutation paths, external integrations, tests, and CI/release files.
   - Focus on code that can break users, lose data, leak secrets, corrupt state, or produce false success.

2. Verify before reporting.
   - Prefer running existing tests or focused checks when practical.
   - Trace the actual code path.
   - Do not report a finding unless there is concrete evidence and realistic user impact.

3. Minimize findings.
   - Report only actionable defects.
   - Merge duplicate symptoms under one root cause.
   - Omit low-confidence concerns.
   - If nothing qualifies, say exactly:

```text
No actionable defects found under this audit scope.
```

## Required Finding Format

For each finding, include:

1. Severity: critical / high / medium / low
2. Evidence: exact file, function, and relevant logic
3. Reproduction path or plausible failing scenario
4. Why this is a real defect, not a preference
5. Minimal fix
6. Confidence: high / medium / low
7. False-positive risk: low / medium / high

## Severity Rules

- Critical: likely data loss, credential leak, destructive action without consent, remote compromise, or irreversible corruption.
- High: serious user-visible breakage, broken safety boundary, wrong-target mutation, or false success after failure.
- Medium: meaningful documented behavior mismatch, important compatibility issue, race condition, or missing validation around risky behavior.
- Low: minor concrete user-visible defect with limited impact.

Do not include low-severity findings unless they are concrete, user-visible, and cheap to fix.

## Output Format

```text
# Actionable Defect Audit

## Audit Scope
[Briefly state what was inspected.]

## Findings
[Findings in the required format, or the exact no-finding sentence.]

## Re-Audit Rule
After fixes, re-audit only changed code and directly affected behavior. Report only regressions introduced by the fix or unresolved original findings.
```

## Guardrails

- Do not create a feature wishlist.
- Do not expand the audit into broad refactoring.
- Do not propose large rewrites when a minimal fix is enough.
- Do not keep searching for weaker issues after no high-confidence actionable defects remain.
- Treat “no actionable defects found” as a successful audit outcome.
