---
name: audit-complete
description: Perform a comprehensive, evidence-based codebase audit. Use only when the user explicitly invokes this skill or asks for a complete audit.
---

# Complete Codebase Audit

Perform a thorough, repository-wide audit intended for major-release confidence. Find every concrete defect that can be supported by evidence, including lower-severity defects, while rejecting style opinions, speculative concerns, and feature wishes.

Completeness changes the breadth and depth of inspection, not the evidence threshold for findings.

## Operating Constraints

- Do not fix code or intentionally modify tracked files.
- Do not create or use an audit rubric.
- Do not create audit documents, ledgers, checkpoints, or other persistent audit state.
- Keep working notes transient and report the full result in the response.
- Do not install or update dependencies, use credentials, mutate external systems, or run destructive checks without explicit user approval.
- Treat existing uncommitted changes as part of the code under audit, not as defects merely because they are uncommitted.
- If the user defines a narrower boundary, audit that boundary completely and trace every directly affected integration.

## Completion Standard

Do not stop after finding several important defects or after high-risk paths look sound. Continue until every material repository area and every applicable audit lens has been inspected or explicitly recorded as not verified.

For a repository-wide audit:

- Inventory the entire repository before prioritizing.
- Read every relevant first-party source, test, configuration, workflow, migration, script, and user-facing documentation file.
- Exclude generated, vendored, binary, cache, fixture-data, and lock files from line-by-line review only when their role and provenance are understood. Inspect their metadata or relevant sections when they affect release behavior.
- Trace cross-file and cross-component behavior rather than evaluating files only in isolation.
- Run the broadest practical non-destructive verification available in the repository.
- Revisit low-risk and leaf areas after high-risk paths are covered.
- Account explicitly for anything that could not be inspected or verified.

For a repository too large to inspect fully within practical limits, do not silently sample and call it complete. Maximize coverage, explain the limitation, and identify exactly what remains unverified.

## Workflow

### 1. Establish Context and Inventory

1. Read all applicable agent instructions.
2. Inspect repository status, structure, submodules, ignored-file rules, and relevant recent or release-target changes when available.
3. Read user-facing documentation, architecture or design documents, manifests, schemas, and public interfaces to establish the intended contract.
4. Identify languages, frameworks, build systems, package managers, test commands, CI workflows, release paths, deployment targets, and supported environments.
5. Build a transient inventory of every material area and classify files that do not require line-by-line review.
6. Identify entry points, trust boundaries, state stores, mutation paths, external integrations, privileged operations, and irreversible actions.

Do not infer the public contract from implementation alone when documentation, schemas, tests, CLI help, API definitions, or configuration define it more directly.

### 2. Run Baseline Verification

Run the repository's existing non-destructive checks when practical:

- full test suites, including integration and end-to-end tests that do not require unsafe external mutation
- build, typecheck, lint, static analysis, and validation commands
- packaging, artifact-generation, installation, or dry-run release checks
- project-provided security, dependency, migration, or configuration checks

Inspect failures to determine whether they expose a product defect, test defect, environment limitation, or unrelated pre-existing condition. Do not report raw tool output as a finding without tracing the cause and impact.

Do not run formatters, autofix modes, snapshot updates, dependency updates, or commands likely to modify tracked files. Check repository status after verification and distinguish disposable test artifacts from user changes.

### 3. Perform Systematic Audit Passes

Apply every relevant lens below. These are investigation prompts, not rubric items. Do not mark them pass or fail mechanically.

#### Contract and Functional Correctness

- Trace each public entry point and primary user workflow through success, invalid-input, empty-state, boundary, and failure paths.
- Compare implementation with documented behavior, schemas, types, examples, CLI help, API contracts, and tests.
- Check calculations, parsing, serialization, ordering, filtering, defaults, time handling, encoding, path handling, and platform assumptions.
- Check that all supported modes, options, variants, and feature combinations behave consistently.
- For user interfaces, verify realistic interaction paths, accessibility semantics, keyboard operation, responsive behavior, localization boundaries, and error or empty states where applicable.

#### Security and Privacy

- Trace untrusted input through validation, authorization, command execution, file access, queries, templates, logging, and output.
- Check authentication, authorization, tenant or target isolation, secret handling, sensitive-data exposure, injection risks, unsafe deserialization, traversal, and privilege boundaries.
- Confirm secure behavior is enforced server-side or at the authoritative layer rather than only by callers or UI.

#### State, Data, and Concurrency

- Trace creates, reads, updates, deletes, migrations, synchronization, caching, retries, and recovery.
- Check invariants, transaction boundaries, partial failures, idempotency, race conditions, stale state, duplicate execution, rollback, cleanup, and crash recovery.
- Check destructive actions, target selection, backups, and data-retention behavior.

#### Failure Handling and Operability

- Follow errors across boundaries and confirm consequential failures cannot appear successful.
- Check timeouts, cancellation, retries, fallback behavior, cleanup, resource release, exit status, diagnostics, and recovery instructions.
- Check logs and telemetry for misleading output, secret leakage, missing actionable context, and failures hidden from operators.

#### Integrations, Configuration, and Environments

- Verify external API assumptions, protocol boundaries, version constraints, environment variables, configuration precedence, and invalid or missing configuration behavior.
- Check development, test, CI, production, container, and supported platform differences where applicable.
- Check optional integrations and disabled-feature behavior, not only the default configuration.

#### Performance and Resource Safety

- Inspect realistic paths for unbounded work, memory or disk growth, repeated network calls, blocking operations, leaks, pathological algorithms, and denial-of-service triggers.
- Report only issues with a realistic workload or attacker-controlled trigger and meaningful impact.

#### Release, Distribution, and Upgrade Safety

- Trace build, packaging, installation, startup, shutdown, deployment, migration, upgrade, rollback, and uninstall paths.
- Check artifact contents, runtime dependencies, version metadata, permissions, defaults, CI gates, release automation, and false-success paths.
- Verify examples and documented setup against the release artifact or actual supported workflow when practical.

#### Tests and Documentation as Evidence

- Inspect whether tests assert the intended behavior rather than reproducing an implementation mistake.
- Look for skipped, disabled, flaky, overly mocked, or non-executed tests that leave consequential behavior falsely appearing covered.
- Treat a missing test as a finding only when it creates a concrete release risk for safety-critical or repeatedly regressing behavior that cannot otherwise be verified.
- Report documentation defects only when they can realistically cause incorrect use, failed setup, unsafe action, or a broken public contract.

### 4. Trace and Verify Every Candidate

For each suspected defect:

1. Trace callers, callees, validation, state changes, error handling, and cleanup.
2. Check whether another layer prevents, contains, or recovers from the issue.
3. Construct a realistic trigger and determine the observable behavior.
4. Compare the behavior with the authoritative contract.
5. Run the smallest useful focused, non-destructive reproduction or existing test when practical.
6. Search for the same root cause and equivalent pattern elsewhere.
7. Reject the candidate if the trigger, behavior, or impact remains speculative.

When subagents are permitted and available, use independent passes for materially different areas or lenses to improve coverage. Give them raw repository scope rather than suspected findings. Independently verify every candidate before reporting it.

### 5. Reconcile the Whole System

After area-by-area inspection:

1. Re-check interactions between components, configuration, environments, and lifecycle stages.
2. Review the complete diff or release delta when one is available for regressions and incomplete migrations.
3. Revisit repository areas that received less attention during risk-first inspection.
4. Resolve contradictions between code, tests, documentation, schemas, and automation.
5. Merge duplicate symptoms under the smallest accurate root cause.
6. Confirm every material inventory area is either inspected or named under `Not verified`.

## Finding Standard

Report a finding only when all of these are known:

- affected location
- realistic triggering conditions
- actual or inevitable behavior
- concrete user, system, security, operational, or release impact
- why existing handling does not prevent or recover from it
- smallest reasonable direction for fixing the root cause

Report all qualifying severities. Low severity is allowed because this is a complete audit, but it must still be a concrete defect rather than polish, preference, or maintainability commentary.

Do not report:

- style, naming, formatting, or taste
- speculative refactors or feature requests
- maintainability concerns without a present failure mode
- theoretical edge cases without a realistic trigger
- dependency age or scanner output without evidence the repository is affected
- duplicate symptoms of one root cause
- behavior already prevented or correctly handled

## Severity and Confidence

- **Critical**: likely remote compromise, credential disclosure, irreversible corruption, major data loss, or destructive action against the wrong target.
- **High**: serious user-visible breakage, broken security or safety boundary, common-path corruption, or false success after a consequential failure.
- **Medium**: meaningful contract violation, realistic race, incorrect state transition, release failure, or missing validation with material impact.
- **Low**: limited but concrete defect with a realistic trigger and user-visible or operational impact.

Use confidence for evidence quality:

- **High**: demonstrated by a check or inevitable from the traced path.
- **Medium**: strongly supported by the complete traced path but not practically demonstrated.
- **Low**: materially uncertain; do not report as a finding.

## Output

Lead with findings ordered by severity, then confidence. Do not dilute findings with a long preamble.

For each finding, use:

```text
## [severity] Concise defect title

- Evidence: exact file and line or symbol, plus the relevant behavior
- Trigger: realistic reproduction path or failing scenario
- Impact: concrete user or system consequence
- Existing handling: why the defect is not already prevented or recovered
- Minimal fix: smallest change that addresses the root cause
- Confidence: high / medium
```

After findings, include:

```text
## Audit Coverage

- Inspected: material repository areas and cross-cutting paths
- Verification: commands and focused checks run, with outcomes
- Not verified: exact limitations and affected areas, or "None"
```

If no finding qualifies, say exactly:

```text
No actionable defects found under the inspected scope.
```

Still include complete audit coverage and limitations. Never claim the repository is defect-free; report only what the performed audit supports.
