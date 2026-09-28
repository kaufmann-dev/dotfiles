# Graph Contract

This contract defines the graph context that `autofixer-graphify` may pass to auditors, fixers, adjudication, and verification. Graph data is advisory context, not proof that a finding is real.

## Slice Schema

Every graph slice must be JSON with exactly these top-level fields:

- `schema_version`: must be `autofixer-graphify.slice.v1`
- `purpose`: one of `audit`, `fix`, `adjudication`, or `verification`
- `source`: object describing the graph source
- `coverage`: object describing graph extraction coverage
- `focus`: object describing requested paths, symbols, and queries
- `nodes`: array of node objects
- `edges`: array of edge objects
- `neighborhoods`: array of graph neighborhoods

`source` fields:

- `graph_path`
- `workspace_fingerprint`
- `generated_at`

`coverage` fields:

- `mode`
- `limitations`
- `excluded_paths`

`focus` fields:

- `paths`
- `symbols`
- `queries`

Node fields:

- `id`
- `kind`
- `label`
- `path`
- `summary`
- `confidence`
- `reasons`

Edge fields:

- `id`
- `source`
- `target`
- `kind`
- `confidence`
- `evidence`

Neighborhood fields:

- `focus`
- `node_ids`
- `edge_ids`
- `likely_affected_files`
- `callers`
- `dependents`
- `shared_tests`
- `entrypoints`

Unknown fields are invalid. Slices must pass `scripts/validate_slice.py` before use.

## Forbidden State

Never include autofixer coordinator ledger state in graph slices or fresh subagent prompts. Forbidden state includes:

- prior findings
- accepted findings, except the accepted findings intentionally given to a fixer for the current repair batch
- rejected findings
- unresolved findings
- findings marked `needs evidence`
- repair attempts
- failed repair count
- clean-confirmation count
- coordinator conclusions
- convergence status
- previous auditor wording
- previous fixer implementation proposals

Fresh auditor prompts may receive only the repository scope, instructions, allowed verification operations, graph slices, and the requirement to report concrete defects.

Fresh fixer prompts may receive only the current accepted finding or approved repair batch, required behavior, relevant graph neighborhoods, repository instructions, verification expectations, and unrelated-change preservation requirements.

## Confidence

Graph node and edge confidence is advisory. Low-confidence graph context may guide investigation, but it cannot support accepting a finding by itself.

Findings still require a realistic trigger, concrete impact, and support from at least one authoritative contract, established invariant, test expectation, or directly observed incorrect behavior.

If graph evidence contradicts source code, authoritative contracts, tests, or observed behavior, trust the latter and record the graph limitation.

## Batching Guidance

Default maximum repair batch size is three accepted root causes.

Batch when findings are independent or coherently coupled:

- Independent findings have separate causes, separable expected changes, and separately verifiable behavior.
- Coherently coupled findings are best fixed by one focused change because separate fixes would duplicate work or create unnecessary churn.

Graph context may inform batching through likely affected files, callers, dependents, shared tests, entrypoint reachability, and module neighborhoods. Formal graph proof is not required.

Do not batch when any finding needs more evidence, any fix needs approval, changes are broad or risky, findings may fight over the same behavior, or the coordinator cannot explain why the batch is safe in one sentence.

If batch verification fails, count a failed repair attempt for every surviving root cause. Split the next repair round unless the failure shows tighter coupling. Block when the same root cause survives two repair attempts.
