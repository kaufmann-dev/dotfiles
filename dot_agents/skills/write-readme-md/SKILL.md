---
name: write-readme-md
description: Create a missing README.md from repository evidence, tailored to the project's primary audience and project type. Use only when the user explicitly invokes this skill or asks to create a README.
---

# Write README

Create a useful entry point for the people most likely to encounter the repository. Optimize
for their first successful task, not for compliance with a conventional README template.

## 1. Gather Evidence

- Stop if the target `README.md` already exists; use an editing workflow instead.
- Inspect package manifests, lockfiles, task runners, build files, `.env.example`, CI, and
  representative source files.
- Inspect nearby documentation, examples, screenshots, and contribution or license files.
- Prefer executable configuration and code over prose when sources disagree.
- Derive names, claims, prerequisites, commands, and examples from evidence. Never invent
  capabilities, commands, compatibility promises, or setup requirements.

## 2. Identify Audience and Purpose

Before choosing sections, determine:

1. **Primary audience**: the reader whose success matters most, such as prospective users,
   adopters, application operators, contributors, or repository maintainers.
2. **Project type**: for example CLI, library/SDK, end-user application, service/API,
   infrastructure/configuration repository, template, or internal tool.
3. **First successful task**: the smallest meaningful outcome the primary reader should reach,
   such as evaluating the project, running a command, importing a library, starting a service,
   deploying infrastructure, or making a verified change.

Infer these from repository evidence. If multiple audiences exist, prioritize one and include
secondary audiences only where their needs materially differ. Ask the user only when the primary
audience is materially ambiguous and cannot be inferred.

## 3. Design the Reading Path

- Lead with the project name, a concrete description, and the information needed to decide
  whether the project is relevant.
- Put the primary audience's first successful task immediately after the introduction, preceded
  only by prerequisites or safety boundaries needed to complete it correctly. Prefer a minimal
  working example over a long feature list or exhaustive setup guide.
- Order later sections by the reader's likely next questions. Use descriptive, project-specific
  headings where they improve navigation.
- Add a contents list only when the README is long enough that scanning headings is insufficient.
- Keep secondary-audience material later in the document or link to existing dedicated docs.
- Omit sections that do not help an identified reader complete a real task.

Use these project-type priorities as guidance, not as a fixed template:

- **CLI**: show a representative command and output early; then installation, common workflows,
  and command reference.
- **Library/SDK**: show installation plus a minimal import/example early; then core concepts,
  common recipes, and API documentation links.
- **Application**: explain what the application does and how to try or run it; use screenshots
  only when they materially aid evaluation.
- **Service/API**: show how to start or access it and make one successful request; then
  configuration, authentication, operations, and API documentation.
- **Infrastructure/configuration repository**: state scope, environment assumptions, and safety
  boundaries before apply/deploy commands; then verification and rollback.
- **Contributor- or maintainer-focused repository**: explain repository purpose briefly, then
  setup, architecture orientation, development loop, and verification.
- **Template/starter**: explain intended users, included decisions, how to instantiate it, and
  what must be customized.

## 4. Write Precisely

- Use the actual package manager and commands found in the repository.
- Make code examples minimal, runnable, and consistent with the current interfaces.
- Separate platform-specific instructions only when the commands genuinely differ.
- Explain configuration only when options exist; distinguish required settings from optional ones.
- Link existing detailed documentation instead of duplicating it.
- Include contributing, support, security, or license information only when evidence exists and
  the information helps the intended reader.
- Use tables only when they improve comparison or lookup. If a Markdown table formatter is
  available in the agent environment, run it on any tables.
- Do not add placeholder sections, generic badges, marketing claims, or exhaustive file trees.

## 5. Verify

- Re-read the README from the primary audience's perspective and confirm the first successful task
  is obvious and achievable.
- Verify every command, path, link, prerequisite, and factual claim against repository evidence.
- Run cheap, non-destructive commands or examples when practical.
- Remove conventional sections that do not serve the chosen audience or project type.
