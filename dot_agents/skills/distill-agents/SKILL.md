---
name: distill-agents
description: Distills a bloated AGENTS.md or alternative instruction files into a lean, high-signal version. Use when the user asks you to distill AGENTS.md or alternative instruction files.
---

# distill-agents

Distill an agent config file (AGENTS.md, CLAUDE.md, or GEMINI.md) into a lean, high-compliance version.

## Step 1 — Locate the file

If the user specifies a file in `$ARGUMENTS`, use that.

Otherwise, check the project root in this order:
```
AGENTS.md    ← primary target
CLAUDE.md
GEMINI.md
```

Use the first one found. Read it and count total lines.

Also note which **sibling files** exist (any of AGENTS.md, CLAUDE.md, GEMINI.md not used as the target). These are synced in Step 4.

## Step 2 — Classify every section

Label each rule, section, or block as one of: **KEEP · REWRITE · CUT**

---

### KEEP

**Keep unconditionally:**
- Anti-pattern examples (Wrong/Right, Before/After, ❌/✅ blocks) — always verbatim
- MCP server configuration — which servers are active, optional, and their conditions
- Technology stack table — if one exists in the source file; keep it, do not generate one if absent
- Exact shell commands with non-obvious flags or project-specific arguments
- Import paths or CLI invocations that differ from what the package name suggests

**Keep fenced code blocks if** the code demonstrates something the agent wouldn't know from reading the codebase — a non-obvious pattern, a required invocation, or an anti-pattern trap. Cut code blocks that are large config dumps, outdated examples, or illustrative padding that adds no behavioral instruction.

**Keep prose if all three are true:**
1. The agent would not know this by reading the codebase
2. It applies regardless of what task is being worked on
3. It changes agent behavior in a verifiable way (clear pass/fail)

---

### REWRITE

Rewrite if any are true:
- Phrased as "don't X" without an alternative → convert to "always use Y instead of X". Positive framing scores higher in LLM attention weights — "never import from X" is weaker than "always import from Y".
- Buried in prose → extract as an imperative command
- Long explanation wrapping a code example → strip prose to one orienting sentence; keep the code

---

### CUT

Cut if any are true:
- The agent already does this correctly by default
- Style rule fully inferable from the existing codebase
- Vague directive with no verifiable outcome ("be careful", "be thorough", "think step by step")
- First-occurrence rule from a single bad session — one mistake is noise, not a pattern
- Prose explanation for a rule the agent already understands; the rule itself is enough
- Contradicts another rule without an explicit priority ordering

---

## Step 3 — Write the distilled file

Apply all classifications immediately. Output the distilled file and the report together in a single response — do not pause for confirmation mid-task, as this risks losing intermediate state. Mirror the source file's section structure where possible. Remove sections entirely if all their content was cut.

**Output rules:**
- Each section under 50 lines
- Target total: under 150 lines; hard ceiling 200 lines if code examples require it
- Commands as exact invocations, never descriptions
- Rules as imperatives: `Run pnpm vitest run before marking done` not `you should run tests`
- One orienting sentence max before any code block — cut everything else

**Report format** (shown after the file):
```
Distillation Report
Original: N lines → Distilled: M lines

KEPT     § Section — reason
REWROTE  § Section — what changed
CUT      § Section — reason
```

---

## Step 4 — Save and sync

Write the distilled content directly to the target file, overwriting it. No backup — the project uses git.

If sibling files were found in Step 1, copy the distilled content to those files verbatim as well. Report which files were written.

---

## Classification Quick Reference

**Always KEEP:**
```
# Non-obvious CLI
dotnet ef migrations add $NAME --project src/Data --startup-project src/Api

# Anti-pattern trap
# Wrong:
$effect(() => { count = count + 1; }); // infinite loop
# Right:
$effect(() => { untrack(() => { count = newValue; }); });

# External constraint
Deploy via Coolify only. Do not write Docker Compose for production.
```

**Cut code blocks like these:**
```json
// 80-line example config that was pasted in for reference
// Outdated schema snapshot
// "Here's what the response looks like" sample payloads
```

**Always CUT (prose):**
```
Write clean, readable code.          ← agent default
Be careful with database queries.    ← vague, unverifiable
Use TypeScript, not JavaScript.      ← inferable from codebase
This project was built to handle…   ← history, not instruction
```

**Rewrite (negative → positive):**
```
# Before
Do not import from 'shadcn-svelte'. Components live in $lib after CLI install.

# After
Import shadcn-svelte components from `$lib/components/ui/<name>`, never from the package name.
```

---

## Step 5 — Self-check

1. Can the agent reproduce every command verbatim if asked? If not — add specificity.
2. Does every rule apply regardless of current task? If not — cut it.
3. Are all constraints phrased as "always X"? Flip any remaining negations.
4. Is the file under 150 lines? If not — find the largest low-signal section and cut or condense it.
