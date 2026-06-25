---
name: debugging
description: Use when reviewing, fixing, reproducing, or hunting bugs.
---

# Debugging

Before touching code, read `docs/bugs/*.md` to learn from previously resolved issues and avoid repeating past mistakes.

## Rules

* Find the root cause before changing code. Do not ship a fix you cannot explain.
* For runtime, behavioral, async, reactivity, event-ordering, or data-loss bugs, reproduce and observe the running system before writing a fix.
* For data-loss bugs, inspect the datastore directly to distinguish a save failure from a display failure.
* For code that maps external APIs or external data shapes, verify field names and types against a real response. Use curl, logs, or the raw payload. Do not trust existing code assumptions.
* Do not trust passing tests if their mocks or fixtures encode the same assumption as the broken code.
* When tests pass but behavior is broken, suspect the fixtures or mocks.
* If two or more fixes fail, stop patching. Restart from reproduction and confirm the actual cause before touching code again.
* Before proposing a fix, state the confirmed cause and the evidence proving it.

## After fixing

After a confirmed fix, create:

`docs/bugs/<descriptive-symptom>.md`

Document:

1. The symptom.
2. The confirmed root cause.
3. The exact changes made.