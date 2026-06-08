---
name: autofixer-graphify
description: Coordinate the autofixer audit-fix-verify loop with Graphify repository graph context. Use only when the user explicitly asks for `autofixer-graphify`, graph-assisted autofixing, or combining `autofixer` with Graphify.
---

# Autofixer Graphify

Use this skill only on explicit request for `autofixer-graphify`, graph-assisted autofixing, or combining `autofixer` with Graphify.

Read the existing `autofixer` skill first and inherit its safety model, stop conditions, reporting requirements, fresh-context subagent requirement, and serial audit/fix/verify loop. This skill adds Graphify-backed repository graph context and one explicit batching override.

Graphify is a hard prerequisite. Before starting the loop, run:

```bash
python dot_agents/skills/autofixer-graphify/scripts/check_graphify.py
```

If it fails, stop as `Blocked` and tell the user to install the `graphifyy` package so the `graphify` command is available on `PATH`.

## Required References

Read `references/graph-contract.md` before creating graph slices, auditor prompts, fixer prompts, adjudication context, or verification context.

## Initialize

1. Run the `autofixer` initialization exactly: read applicable instructions, establish audit scope, record initial working-tree state, identify verification commands and approval-required operations, and confirm fresh subagents are available.
2. Run `scripts/check_graphify.py`.
3. Compute the first workspace epoch:

   ```bash
   python dot_agents/skills/autofixer-graphify/scripts/graph_epoch.py --workspace .
   ```

4. Build the first transient Graphify snapshot:

   ```bash
   python dot_agents/skills/autofixer-graphify/scripts/graph_snapshot.py --workspace . --epoch-json <epoch.json>
   ```

5. Default to code-oriented extraction only. Treat PDFs, office documents, images, videos, audio, and broad documentation extraction as deep semantic extraction.
6. If deep semantic files are in scope, stop for explicit approval before including them. Without approval, exclude them and record the exclusion as a graph coverage limitation.

Runtime graph output must be transient and untracked. Do not commit Graphify output, persistent ledgers, or harness-specific subagent definitions.

## Graph Slices

Use `scripts/graph_slice.py` to create schema-limited slices for audit, fix, adjudication, and verification. Validate every slice before using it:

```bash
python dot_agents/skills/autofixer-graphify/scripts/graph_slice.py --graph-json <graph.json> --purpose audit --output <slice.json>
python dot_agents/skills/autofixer-graphify/scripts/validate_slice.py <slice.json>
```

Slices may include repository graph context only: likely affected files, callers, dependents, shared tests, entrypoint reachability, and nearby modules. They must not contain prior findings, rejected findings, repair attempts, clean-confirmation count, coordinator conclusions, or any other autofixer ledger state.

## Audit

Run auditors serially through fresh-context subagents. Give each auditor only:

- raw repository scope and audit boundary
- applicable repository instructions
- allowed verification operations
- validated graph slices for the requested scope
- the requirement to report concrete defects only

Do not disclose prior findings, rejections, attempted fixes, clean-confirmation count, or coordinator conclusions. Graph context is advisory; auditors must still provide concrete evidence, realistic triggers, impact, confidence, verification performed, coverage, and limitations.

## Adjudication

Adjudicate every finding independently as `accepted`, `rejected`, or `needs evidence`, using the inherited `autofixer` rules. Graph evidence may help trace reachability, callers, dependents, entrypoints, and shared tests, but it is not a substitute for a realistic trigger and concrete impact.

## Repair Batching Override

Override only the `autofixer` rule that selects exactly one accepted root cause per repair round.

After adjudication, the coordinator may select one repair batch of up to three accepted root causes when the findings are independent or coherently coupled:

- Independent: separate causes, separable expected changes, and separately verifiable behavior.
- Coherently coupled: one focused change is the simplest correct fix because separate fixes would duplicate work or create unnecessary churn.

Use graph context as advisory input for likely affected files, callers, dependents, shared tests, entrypoint reachability, and module neighborhoods. Do not require formal graph proof before batching.

Do not batch when any finding is `needs evidence`, any fix needs approval, expected changes are broad or risky, findings may fight over the same behavior, or the coordinator cannot explain why the batch is safe in one sentence.

Use one fresh fixer subagent per batch. Give it the accepted findings, required behavior for each finding, relevant graph neighborhoods, per-finding verification expectations, and the requirement to produce the smallest correct combined patch. Require the final report to map changed files and tests back to each finding.

Do not run concurrent fixers.

## After Each Repair Batch

1. Review the diff and verify each finding in the batch.
2. If verification fails, count a failed repair attempt for each surviving root cause.
3. Split the batch on the next round unless the failure shows the findings are more tightly coupled.
4. Stop as `Blocked` if the same root cause survives two attempts.
5. Mark the graph epoch stale, recompute the workspace fingerprint, and refresh the graph before the next audit.

Run Graphify incremental update only when the prior transient cache matches the previous epoch. Otherwise perform a full transient rebuild. Do not start the next audit until the graph snapshot matches the current workspace fingerprint.

## Clean Confirmation

After the first qualified clean audit, freeze the graph epoch. Reuse it for the second clean audit only if the workspace fingerprint is unchanged. If the workspace changes, reset the clean-confirmation count and rebuild or update the graph first.

Report final outcomes with the inherited `autofixer` format plus graph coverage limitations and whether any repair rounds used batching.
