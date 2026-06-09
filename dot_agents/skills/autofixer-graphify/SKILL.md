---
name: autofixer-graphify
description: Coordinate the autofixer audit-fix-verify loop with Graphify repository graph context. Use only when the user explicitly asks for `autofixer-graphify`, graph-assisted autofixing, or combining `autofixer` with Graphify.
---

# Autofixer Graphify

Use this skill only on explicit request for `autofixer-graphify`, graph-assisted autofixing, or combining `autofixer` with Graphify.

Act as the persistent coordinator. Own scope, finding adjudication, transient state, safety decisions, progress, and termination. Delegate every audit and fix to a newly spawned fresh-context subagent.

Run auditors and fixers serially. Never run them concurrently because the workspace must remain stable for mutation attribution and regression analysis. This skill utilizes Graphify-backed repository graph context.

Graphify is a hard prerequisite. Before starting the loop, run:

```bash
python dot_agents/skills/autofixer-graphify/scripts/check_graphify.py
```

If it fails, stop as `Blocked` and tell the user to install the `graphifyy` package so the `graphify` command is available on `PATH`.

## Required References

Read `references/graph-contract.md` before creating graph slices, auditor prompts, fixer prompts, adjudication context, or verification context.

## Initialize

1. Read all applicable instructions and establish the requested audit boundary. If none is supplied, use a repository-wide, risk-prioritized audit for concrete defects.
2. Record the initial working-tree state so pre-existing user changes can be distinguished and preserved.
3. Identify available verification commands and operations that are prohibited or require approval.
4. Stop as blocked immediately if fresh subagents are unavailable.
5. Detect whether the user requested YOLO mode by explicitly pairing this skill request with terms such as `YOLO mode`, `yolo`, or `no approval for dangerous fixes`.
6. Run `scripts/check_graphify.py`.
7. Compute the first workspace epoch:

   ```bash
   python dot_agents/skills/autofixer-graphify/scripts/graph_epoch.py --workspace .
   ```

8. Build the first transient Graphify snapshot:

   ```bash
   python dot_agents/skills/autofixer-graphify/scripts/graph_snapshot.py --workspace . --epoch-json <epoch.json>
   ```

9. Default to code-oriented extraction only. Treat PDFs, office documents, images, videos, audio, and broad documentation extraction as deep semantic extraction.
10. If deep semantic files are in scope, stop for explicit approval before including them. Without approval, exclude them and record the exclusion as a graph coverage limitation.
11. Maintain a transient ledger only in coordinator context. Do not create a persistent ledger, audit document, script, or harness-specific subagent definition.

Track in the ledger:
- accepted, rejected, and unresolved finding fingerprints
- repair attempts per root cause
- verification outcomes
- consecutive qualified clean-confirmation count
- completed repair rounds
- YOLO mode status
- audit coverage and material limitations (including graph coverage limitations)
- workspace state needed to identify changes between audits
- whether any repair rounds used batching

Fingerprint findings by affected behavior, root cause, and relevant location. Do not rely only on wording or line numbers.

Runtime graph output must be transient and untracked. Do not commit Graphify output, persistent ledgers, or harness-specific subagent definitions.

## YOLO Mode

YOLO mode is active only when the user explicitly requests it for this skill invocation.

When YOLO mode is active:
- Do not pause for approval before dangerous fixes, including destructive actions, credential use, external mutation, dependency updates, major migrations, or broad rewrites.
- Still identify dangerous fixes, record that YOLO mode authorized proceeding without approval, and include the risky action in checkpoint or final reporting.
- Still respect all stop conditions that are not approval gates, including workspace-conflict blocking, failed-attempt blocking, verification requirements, and stricter user-provided or harness-provided budgets.
- Still stop after every five completed repair rounds and ask for confirmation before beginning another five-round block.
- Never interpret YOLO mode as permission to bypass missing required tools, missing permissions, verification, fresh-context subagents, or user-specified scope.

## Graph Slices

Use `scripts/graph_slice.py` to create schema-limited slices for audit, fix, adjudication, and verification. Validate every slice before using it:

```bash
python dot_agents/skills/autofixer-graphify/scripts/graph_slice.py --graph-json <graph.json> --purpose audit --output <slice.json>
python dot_agents/skills/autofixer-graphify/scripts/validate_slice.py <slice.json>
```

Slices may include repository graph context only: likely affected files, callers, dependents, shared tests, entrypoint reachability, and nearby modules. They must not contain prior findings, rejected findings, repair attempts, clean-confirmation count, coordinator conclusions, or any other autofixer ledger state.

## Run The Serial Loop

### 1. Audit

Spawn a new fresh-context audit subagent. Give it only:
- raw repository scope and audit boundary
- applicable repository instructions
- allowed verification operations
- validated graph slices for the requested scope
- the requirement to report concrete defects only

Do not disclose prior findings, rejections, attempted fixes, clean-confirmation count, or coordinator conclusions. Graph context is advisory; auditors must still provide concrete evidence, realistic triggers, impact, confidence, verification performed, coverage, and limitations.

If an audit is malformed or materially incomplete, retry once with a new fresh auditor. Stop as blocked if the retry is also malformed or materially incomplete.

### 2. Adjudicate

Independently trace every reported finding before accepting it. Classify it as `accepted`, `rejected`, or `needs evidence`.

- Reject a finding without a realistic trigger, concrete impact, and support from at least one of: an authoritative contract, established invariant, test expectation, or directly observed incorrect behavior. Graph evidence may help trace reachability, callers, dependents, entrypoints, and shared tests, but it is not a substitute for a realistic trigger and concrete impact.
- Treat `needs evidence` as unresolved, never accepted or clean.
- Merge duplicate symptoms into one root cause.
- Reuse a prior rejection only when its fingerprint matches and neither the relevant implementation nor authoritative contract changed.
- Reset the clean-confirmation count whenever an accepted or `needs evidence` finding appears, or the repository changes between confirmation audits.

### 3. Repair (Batching and Fixing)

After adjudication, the coordinator selects repair batches. The coordinator may select one repair batch of up to three accepted root causes when the findings are independent or coherently coupled:
- Independent: separate causes, separable expected changes, and separately verifiable behavior.
- Coherently coupled: one focused change is the simplest correct fix because separate fixes would duplicate work or create unnecessary churn.

Use graph context as advisory input for likely affected files, callers, dependents, shared tests, entrypoint reachability, and module neighborhoods. Do not require formal graph proof before batching.

Do not batch when any finding is `needs evidence`, expected changes are broad or risky, findings may fight over the same behavior, or the coordinator cannot explain why the batch is safe in one sentence. When YOLO mode is inactive, also do not batch when any fix needs approval.

Before delegation, pause for explicit approval if YOLO mode is inactive and the fix requires a destructive action, credentials, external mutation, dependency update, major migration, or broad rewrite. If approval is denied, preserve the finding as unresolved, continue only with independent safe findings, and ultimately report `Blocked`, never `Converged`. If YOLO mode is active, proceed without approval and record the risky action in the ledger.

Spawn one new fresh-context fixer subagent per repair batch. Give it only:
- the accepted finding or accepted findings in the batch, with required behavior for each
- relevant scope and repository instructions
- relevant graph neighborhoods
- per-finding verification expectations
- the requirement to preserve unrelated and pre-existing changes

Do not require or disclose the auditor's proposed implementation. Require the smallest correct fix or smallest correct combined patch, focused tests where appropriate, and updates to existing documentation only when directly affected. Require the final report to map changed files and tests back to each finding.

Do not run concurrent fixers.

### 4. Verify

Review the resulting diff and confirm it addresses only the accepted repair batch and necessary directly affected behavior. Preserve unrelated and pre-existing changes.

Run focused verification and relevant broader checks for each finding in the repair batch. Count the round as a failed repair attempt for each surviving root cause if there is no relevant diff, verification fails, or the same defect survives. If batch verification fails, split the batch on the next round unless the failure shows the findings are more tightly coupled. After every repair attempt, return to step 1 with a completely fresh auditor.

Stop as `Blocked` if the same root cause survives two attempts.

Pause as blocked if concurrent or unattributable workspace changes make fixer changes unsafe to distinguish from user changes.

After each repair batch:
1. Mark the graph epoch stale, recompute the workspace fingerprint, and refresh the graph before the next audit.
2. Run Graphify incremental update only when the prior transient cache matches the previous epoch. Otherwise perform a full transient rebuild. Do not start the next audit until the graph snapshot matches the current workspace fingerprint.

## Clean Confirmation

After the first qualified clean audit, freeze the graph epoch. Reuse it for the second clean audit only if the workspace fingerprint is unchanged. If the workspace changes, reset the clean-confirmation count and rebuild or update the graph first.

An audit counts as a qualified clean confirmation only when adjudication yields no accepted or `needs evidence` findings, no material unverified area remains that could reasonably invalidate the clean result under the requested scope, and required verification passes. The first qualified clean audit sets the count to one. The second consecutive qualified clean audit establishes convergence only if no repository changes occurred between the two.

## Stop Conditions

### Converged

Report `Converged` only after all conditions hold:
- two consecutive qualified clean confirmation audits completed
- no repository changes occurred between those audits
- required verification passed
- no material unverified area remains that could reasonably invalidate the clean result under the requested scope
- no accepted, `needs evidence`, approval-pending, or blocked finding remains

Rejected findings do not prevent convergence. State that convergence was reached under the inspected scope; never claim the repository is universally defect-free.

### Checkpoint Reached

After every five completed repair rounds, stop before beginning another repair round. Report `Checkpoint reached`, summarize progress, and ask permission to continue with exactly five additional repair rounds. Never continue automatically beyond a five-round block. Respect stricter user-provided or harness-provided budgets.

### Approval Required

When YOLO mode is inactive, report `Approval required` before any destructive action, credential use, external mutation, dependency update, major migration, or broad rewrite. Describe the accepted finding, proposed risky action, and why approval is required. Resume the serial loop only after explicit approval.

When YOLO mode is active, do not use `Approval required` for dangerous fixes. Proceed with the fix, record the risky action as YOLO-authorized, and include it in the next checkpoint or final report.

### Blocked

Report `Blocked` when:
- the same root cause survives two repair attempts
- fixes oscillate, repeatedly reintroduce an earlier accepted defect, or make no measurable progress
- two consecutive audits are malformed or materially incomplete
- approval denial leaves an unresolved finding
- workspace conflicts prevent safe mutation attribution
- unresolved findings or material verification gaps prevent convergence
- check_graphify.py fails during initialization

## Report

Every final, checkpoint, or approval report must include:
- outcome: `Converged`, `Checkpoint reached`, `Approval required`, or `Blocked`
- accepted findings fixed
- rejected findings with concise reasons
- unresolved or blocked findings
- verification performed and outcomes
- audit coverage and limitations (including graph coverage limitations)
- completed repair rounds
- YOLO mode status and any risky actions performed without approval
- remaining working-tree changes, distinguishing pre-existing changes when possible
- whether any repair rounds used batching

For `Checkpoint reached`, ask permission for exactly five additional repair rounds. For `Approval required`, ask for explicit approval of the described action.
