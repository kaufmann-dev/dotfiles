---
name: find-skills
description: Discover, compare, vet, and optionally help install external agent skills.
---

# Find Skills

## Purpose

Help the user discover external skills that extend agent capabilities, then verify whether they are trustworthy enough to recommend or install.

## Use When

- The user asks whether a skill exists.
- The user asks to find or install a skill.
- The user describes a recurring capability gap that a reusable skill might solve.
- The user asks how to extend the agent workflow.

## Do Not Use When

- A local skill already fits the request.
- The user wants the current task solved directly rather than adding capabilities.
- The requested installation would be unsafe or unrelated to the user's goal.

## Rules

- Do not recommend a skill based only on a name.
- Prefer official, popular, maintained, and source-visible skills.
- Be cautious with unknown authors, low install counts, stale repos, or broad permissions.
- Do not install anything without explicit user consent.
- Do not overwrite local skills without confirming scope.

## Workflow

1. Identify the domain, task, and whether a reusable skill is appropriate.
2. Check current skill sources such as skills.sh, the Skills CLI, and the source repository.
3. Vet candidates:
   - Source reputation
   - Install count or adoption
   - Repository activity
   - Documentation quality
   - Permission or tool implications
4. Present the best option or a short comparison.
5. If the user approves installation, run the appropriate install command and verify the skill appears locally.

## Output

Include:

- Skill name
- What it does
- Why it fits
- Trust notes
- Install command or next step
- Any risks or unknowns

## Completion Rules

Finish after recommending, declining to recommend, or completing an approved install. If no suitable skill exists, offer to handle the task directly or help design a purpose-specific skill.
