---
name: audit
description: "Use this skill when the user asks for an audit, security review, release-readiness check, pre-deployment review, or read-only assessment of correctness, spec alignment, tests, architecture integrity, operability, and code quality."
---

# Audit

## Purpose

Review a project or change set before release. The audit should identify concrete risks and decide whether the work is safe to ship.

## Rules

- Stay read-only unless the user separately asks for fixes.
- Do not modify files, stage changes, create commits, deploy, or mutate external systems.
- Read the relevant brief, plan, docs, tests, and implementation before judging.
- Be specific: every finding needs a location, impact, and actionable recommendation.
- Do not assume dependency CVE scans or dynamic tests are clean unless results are provided.

## Review Areas

- Input validation and injection risks
- Authentication, authorization, and session handling
- Data protection, secrets, PII, logs, and backups
- CORS, security headers, OAuth, webhooks, and third-party scripts
- Correctness, edge cases, race conditions, and state consistency
- Architecture boundaries and dependency direction
- Tests, coverage quality, flaky or missing scenarios
- Operability, logging, pagination, bounded work, and rollback

## Severity

| Severity | Meaning | Verdict impact |
| --- | --- | --- |
| Critical | Remote exploit, data breach risk, broken core functionality, or direct spec violation | BLOCK |
| High | Significant exposure, exploitable with conditions, or material spec gap | HOLD |
| Medium | Limited impact, authenticated-only issue, or minor spec drift | HOLD or SHIP WITH TICKET |
| Low | Defense-in-depth or maintainability concern | SHIP WITH TICKET |
| Info | Observation or optional improvement | SHIP |

## Output

Use this structure:

```markdown
## Audit Report

**Verdict:** SHIP | SHIP WITH TICKET | HOLD | BLOCK

**Overview:** Brief summary of what was reviewed and the main risk theme.

### Findings

#### [SEVERITY] Title
- **Location:** file:line
- **Issue:** What is wrong.
- **Impact:** What can fail or be exploited.
- **Recommendation:** Specific fix.

### Spec Alignment

### What Is Done Well

### Verification
```

## Completion Rules

Finish with findings ordered by severity. If there are no issues, say so clearly and note any residual test or dependency-scan gaps.
