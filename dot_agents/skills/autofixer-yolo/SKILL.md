---
name: autofixer-yolo
description: Coordinate a bounded audit-fix-verify loop that automatically mutates code through fresh-context subagents, proceeding without approval for dangerous fixes. Use only when the user explicitly invokes this skill.
---

# Autofixer YOLO

Act as the persistent coordinator. Own scope, finding adjudication, transient state, safety decisions, progress, and termination. Delegate every audit and fix to a newly spawned fresh-context subagent.

Run auditors and fixers serially. Never run them concurrently because the workspace must remain stable for mutation attribution and regression analysis.

This skill proceeds without explicit approval for dangerous fixes. It still identifies risky actions, records them in the ledger, and includes them in checkpoint or final reporting.

## Initialize

1. Read all applicable instructions and establish the requested audit boundary. If none is supplied, use a repository-wide, risk-prioritized audit for concrete defects.
2. Record the initial working-tree state so pre-existing user changes can be distinguished and preserved.
3. Identify available verification commands and operations that are prohibited or require approval.
4. Stop as blocked immediately if fresh subagents are unavailable.
5. Maintain a transient ledger only in coordinator context. Do not create a persistent ledger, audit document, script, or harness-specific subagent definition.

Track in the ledger:

- accepted, rejected, and unresolved finding fingerprints
- repair attempts per root cause
- verification outcomes
- consecutive qualified clean-confirmation count
- completed repair rounds
- audit coverage and material limitations
- risky actions performed
- workspace state needed to identify changes between audits

Fingerprint findings by affected behavior, root cause, and relevant location. Do not rely only on wording or line numbers.

## Dangerous Fixes

This skill does not pause for explicit approval before dangerous fixes, including destructive actions, credential use, external mutation, dependency updates, major migrations, or broad rewrites.

When a dangerous fix is required:

- Proceed without approval and record the risky action in the ledger.
- Include the risky action in checkpoint or final reporting.
- Still respect all stop conditions that are not approval gates, including workspace-conflict blocking, failed-attempt blocking, verification requirements, and stricter user-provided or harness-provided budgets.
- Still stop after every five completed repair rounds and ask for confirmation before beginning another five-round block.
- Never treat the absence of approval gates as permission to bypass missing required tools, missing permissions, verification, fresh-context subagents, or user-specified scope.

## Run The Serial Loop

### 1. Audit

Spawn a new fresh-context audit subagent. Give it only:

- raw repository scope and audit boundary
- applicable repository instructions
- allowed verification operations
- the requirement to report concrete defects only

Do not disclose prior findings, rejections, attempted fixes, or coordinator conclusions.

Require each finding to include evidence and relevant location, realistic trigger, concrete impact, existing handling and why it is insufficient, minimal fix direction, confidence, verification performed, audit coverage, and limitations. Reject preferences, speculative refactors, unsupported concerns, and low-confidence claims.

If an audit is malformed or materially incomplete, retry once with a new fresh auditor. Stop as blocked if the retry is also malformed or materially incomplete.

### 2. Adjudicate

Independently trace every reported finding before accepting it. Classify it as `accepted`, `rejected`, or `needs evidence`.

- Reject a finding without a realistic trigger, concrete impact, and support from at least one of: an authoritative contract, established invariant, test expectation, or directly observed incorrect behavior.
- Treat `needs evidence` as unresolved, never accepted or clean.
- Merge duplicate symptoms into one root cause.
- Reuse a prior rejection only when its fingerprint matches and neither the relevant implementation nor authoritative contract changed.
- Reset the clean-confirmation count whenever an accepted or `needs evidence` finding appears, or the repository changes between confirmation audits.

An audit counts as a qualified clean confirmation only when adjudication yields no accepted or `needs evidence` findings, no material unverified area remains that could reasonably invalidate the clean result under the requested scope, and required verification passes. The first qualified clean audit sets the count to one. The second consecutive qualified clean audit establishes convergence only if no repository changes occurred between the two.

### 3. Fix

Select one repair batch per repair round. The default batch is one accepted root cause. The coordinator may batch up to three accepted root causes when they are independent or coherently coupled:

- Independent: separate causes, separable expected changes, and separately verifiable behavior.
- Coherently coupled: one focused change is the simplest correct fix because separate fixes would duplicate work or create unnecessary churn.

Do not batch when any finding is `needs evidence`, expected changes are broad or risky, findings may fight over the same behavior, or the coordinator cannot explain why the batch is safe in one sentence.

Before delegation, identify whether the fix requires a destructive action, credentials, external mutation, dependency update, major migration, or broad rewrite. Proceed without approval and record the risky action in the ledger. If the fix cannot proceed safely for any reason other than missing approval, preserve the finding as unresolved and continue only with independent safe findings; ultimately report `Blocked`, never `Converged`.

Spawn one new fresh-context fixer subagent per repair batch. Give it only:

- the accepted finding or accepted findings in the batch, with required behavior for each
- relevant scope and repository instructions
- per-finding verification expectations
- the requirement to preserve unrelated and pre-existing changes

Do not require or disclose the auditor's proposed implementation. Require the smallest correct fix or smallest correct combined patch, focused tests where appropriate, and updates to existing documentation only when directly affected. For batched repairs, require the final report to map changed files and tests back to each finding.

### 4. Verify

Review the resulting diff and confirm it addresses only the accepted repair batch and necessary directly affected behavior. Preserve unrelated and pre-existing changes.

Run focused verification and relevant broader checks for each finding in the repair batch. Count the round as a failed repair attempt for each surviving root cause if there is no relevant diff, verification fails, or the same defect survives. If batch verification fails, split the batch on the next round unless the failure shows the findings are more tightly coupled. After every repair attempt, return to step 1 with a completely fresh auditor.

Pause as blocked if concurrent or unattributable workspace changes make fixer changes unsafe to distinguish from user changes.

## Stop Conditions

### Converged

Report `Converged` only after all conditions hold:

- two consecutive qualified clean confirmation audits completed
- no repository changes occurred between those audits
- required verification passed
- no material unverified area remains that could reasonably invalidate the clean result under the requested scope
- no accepted, `needs evidence`, or blocked finding remains

Rejected findings do not prevent convergence. State that convergence was reached under the inspected scope; never claim the repository is universally defect-free.

### Checkpoint Reached

After every five completed repair rounds, stop before beginning another repair round. Report `Checkpoint reached`, summarize progress, and ask permission to continue with exactly five additional repair rounds. Never continue automatically beyond a five-round block. Respect stricter user-provided or harness-provided budgets.

### Blocked

Report `Blocked` when:

- the same root cause survives two repair attempts
- fixes oscillate, repeatedly reintroduce an earlier accepted defect, or make no measurable progress
- two consecutive audits are malformed or materially incomplete
- a dangerous fix cannot proceed safely for reasons other than missing approval
- workspace conflicts prevent safe mutation attribution
- unresolved findings or material verification gaps prevent convergence

## Report

Every final or checkpoint report must include:

- outcome: `Converged`, `Checkpoint reached`, or `Blocked`
- accepted findings fixed
- rejected findings with concise reasons
- unresolved or blocked findings
- verification performed and outcomes
- audit coverage and limitations
- completed repair rounds
- risky actions performed
- remaining working-tree changes, distinguishing pre-existing changes when possible

For `Checkpoint reached`, ask permission for exactly five additional repair rounds.
