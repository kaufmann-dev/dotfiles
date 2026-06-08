---
name: audit-defect
description: Audit a codebase for concrete, actionable defects. Use only when the user explicitly invokes this skill or asks for a defect audit.
---

# Actionable Defect Audit

Find and report real defects with concrete evidence and realistic user impact. Do not fix code while using this skill.

## Establish the Audit Boundary

Derive the boundary from the user's request. If the user names files, features, commits, or risks, inspect those and directly affected behavior. Otherwise, perform a repository-wide audit focused on the highest-risk paths.

Before looking for defects:

1. Read the applicable agent instructions.
2. Inspect the repository structure, working-tree status, and relevant documentation.
3. Identify the public contract from user-facing docs, interfaces, tests, schemas, and configuration.
4. Identify the primary execution paths, trust boundaries, state mutations, external integrations, and recovery paths.
5. Record any material area that cannot be inspected or verified.

Do not treat uncommitted changes as defects merely because they are uncommitted. Do not modify or revert tracked changes.

## Qualifying Defects

Report only concrete problems in one or more of these categories:

- incorrect behavior or results
- security or privacy violations
- data loss, corruption, or unsafe recovery
- broken public or documented behavior
- race conditions and invalid state transitions
- failures hidden behind success output or exit status
- user-visible regressions
- unsafe automation or non-interactive behavior
- missing validation at a meaningful trust boundary
- test failures that expose a product defect

Do not report:

- style preferences or naming opinions
- speculative refactors or feature requests
- maintainability concerns without a present failure mode
- theoretical edge cases without a realistic trigger
- behavior already prevented or handled by the code
- missing tests unless they conceal a concrete defect or leave safety-critical behavior unverifiable
- dependency age or known vulnerabilities without evidence that the repository is affected

## Audit Workflow

### 1. Prioritize Risk

Inspect likely high-impact paths first:

- destructive or irreversible operations
- authentication, authorization, secrets, and untrusted input
- persistence, migrations, synchronization, and concurrency
- target selection, path handling, and command construction
- error propagation, retries, rollback, and cleanup
- defaults and configuration that alter safety or correctness
- release, installation, and automation paths that can report false success

Spend less time on low-impact leaf code unless evidence points there.

### 2. Trace Candidate Defects

For each candidate:

1. Trace the complete relevant path, including callers, validation, error handling, and cleanup.
2. Check whether another layer prevents or handles the suspected failure.
3. Compare behavior with the applicable public contract.
4. Construct a realistic trigger and identify the observable impact.
5. Run the smallest useful existing test or focused non-destructive check when practical.
6. Reject the candidate if evidence is incomplete, impact is merely hypothetical, or the claim depends on an unstated preference.

Never run destructive, production-facing, credential-using, or externally mutating checks without explicit user approval.

### 3. Consolidate and Rank

- Merge multiple symptoms caused by the same root defect.
- Prefer the smallest accurate claim supported by evidence.
- Rank findings by user impact, likelihood, and reversibility.
- Stop when the defined boundary is covered and no high-confidence candidate remains unverified.
- Do not continue searching merely to produce more findings.

## Severity

- **Critical**: likely credential disclosure, remote compromise, irreversible corruption, major data loss, or destructive action against the wrong target.
- **High**: serious user-visible breakage, broken safety boundary, common-path data corruption, or false success after a consequential failure.
- **Medium**: meaningful public-contract violation, realistic race, incorrect state transition, or missing validation with material impact.
- **Low**: limited but concrete user-visible defect with a realistic trigger and straightforward fix.

Do not inflate severity based on hypothetical downstream consequences. Omit low-severity findings unless they are unambiguous and actionable.

## Required Evidence

A finding is valid only when all of the following are known:

- the affected code location
- the triggering conditions
- the actual or inevitable behavior
- the realistic user or system impact
- why existing handling does not prevent the defect
- a minimal direction for fixing the root cause

Use confidence to describe evidence quality, not severity:

- **High**: demonstrated by a test/check or inevitable from the traced code path.
- **Medium**: strongly supported by the traced path but not practically demonstrated.
- **Low**: materially uncertain; normally omit.

## Output

Do not pad the report. Report zero, one, or many findings depending only on what qualifies.

Lead with findings ordered by severity. For each finding, use:

```text
## [severity] Concise defect title

- Evidence: exact file and line or symbol, plus the relevant behavior
- Trigger: realistic reproduction path or failing scenario
- Impact: concrete user or system consequence
- Existing handling: why the defect is not already prevented or recovered
- Minimal fix: smallest change that addresses the root cause
- Confidence: high / medium / low
```

After the findings, include:

```text
## Audit Coverage

- Inspected: relevant areas and checks performed
- Not verified: material limitations, or "None"
```

If no finding qualifies, say exactly:

```text
No actionable defects found under the inspected scope.
```

Still include the audit coverage so the result does not imply uninspected areas were verified.

## Guardrails

- Do not intentionally edit tracked files or perform repository mutations. Disposable artifacts produced by non-destructive verification are acceptable.
- Do not turn the audit into a feature wishlist or broad refactor proposal.
- Do not report a concern before checking nearby validation and error handling.
- Do not present assumptions as verified facts.
- Do not duplicate findings or split one root cause into several reports.
- Treat a no-finding result as a valid outcome.
