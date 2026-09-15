---
name: debloat
description: Remove over-engineered security, testing, and complexity from recent changes when explicitly invoked.
---

# Debloat

On-demand cleanup for model-generated bloat. Use only when the user explicitly
invokes this skill (e.g. "debloat", "trim this", "remove unnecessary stuff").

## Goal

Reduce the change under review to the smallest version that satisfies the
explicit requirements — nothing speculative, nothing "just in case".

## Process

1. Collect the explicit requirements from the user's request and any named
   governing evidence. Inference and "best practice" are not requirements.
2. Review the diff or files the user points at. If no scope is given, ask for
   it; do not sweep the whole repo.
3. For every added hunk, demand a trace: which explicit requirement needs it?
   No trace → remove. Weak trace → simplify until the trace is exact.
4. Prefer deletion over simplification, simplification over rewrite. Never
   replace one speculative layer with another.
5. Verify with the cheapest check that covers the touched area (type check,
   lint, or the existing targeted test).

## Remove

- Security hardening with no stated threat: extra auth layers, sanitizers for
  trusted input, encryption/validation speculative cases.
- Defensive code for impossible states: exhaustive error branches, null checks
  where the type excludes null, retries/fallbacks nobody asked for.
- Test bloat: tests for trivial getters/setters, duplicated coverage, snapshot
  tests for stable output, 100%-coverage chasing.
- Premature structure: abstractions with one caller, factories/builders for
  simple construction, interfaces with one implementation.
- Speculative flexibility: config flags with one real value, plugin hooks,
  feature toggles, compatibility shims, dual paths.
- Comment and doc bloat: comments restating the code, READMEs for internal
  helpers, changelogs nobody asked for.

## Keep

- Behavior the user explicitly requested, including security they named.
- Error handling for failure modes that really occur at that call site.
- Tests for non-trivial logic, regressions already observed, and contracts
  other code depends on.
- Structure that two or more existing callers already need.

## Report

List what was removed (one line each, with the missing requirement as the
reason) and what borderline complexity was kept and why. If a removal is
risky, say so instead of keeping it silently.
