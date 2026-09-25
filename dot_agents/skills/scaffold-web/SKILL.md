---
name: scaffold-web
description: Create a new web application and set it up with the standard project conventions by coordinating the ui-design-principles, oidc-auth, add-compliance-links, coolify, write-readme-md, and write-agents-md skills. Use only when the user explicitly invokes this skill.
---

# Scaffold Web

Create a new web application and bring it to a deployable, documented state by running other
skills in a fixed order. Invoking this skill counts as explicitly invoking each skill it runs. Load
and follow each skill completely; this skill only decides order, conditions, and handoffs.

## 1. Gather Inputs

Before changing files, collect the following from the request, asking once for anything missing:

- What the application does and who uses it.
- Whether it needs login: protected pages, user-owned data, or admin features. Only a fully
  public site skips authentication.
- The canonical production domain, which `add-compliance-links` requires. Do not infer it.

## 2. Choose the Foundation

- If the working directory already contains a template or starter project, build on it. Keep its
  stack, structure, and tooling, and follow its instruction files. Do not regenerate it or switch
  stacks.
- Otherwise, use the stack the user names. If none is named, choose a mature, maintained stack
  that fits the application's rendering, data, authentication, and Coolify/Nixpacks deployment
  needs, and state the choice. Scaffold with the stack's official generator, non-interactively,
  using current stable versions.
- Initialize a Git repository if the directory is not already one.

## 3. Build the Application

- Implement the requested functionality following `ui-design-principles`.
- Remove generator demo pages, sample assets, and boilerplate styles. Generator starter styling
  is not an established visual system; apply the personal visual defaults unless the template
  defines its own visual system.

## 4. Write the README

Delete `README.md` if it only describes the generator or template, then run `write-readme-md`.
Complete this before the following steps, which add managed sections to the README.

## 5. Add Authentication

Only when the application needs login, run `oidc-auth`. It creates the login screen and adds the
`Authentication Setup` README section.

## 6. Add Compliance Links

Run `add-compliance-links` with the domain from step 1. Run it after authentication so link
placement accounts for the login screen.

## 7. Configure Deployment

Run `coolify` to add any required `nixpacks.toml` and the `Coolify Deployment` README section.

## 8. Write AGENTS.md

Run `write-agents-md` last so its commands reflect the finished project. If the template or
generator already created `AGENTS.md`, update it in place under the same content rules instead,
keeping instructions that remain accurate.

## 9. Verify and Report

- Run the project's type check, lint, and build, and fix any failures.
- Confirm the README has no duplicate sections and every documented command works.
- Report the stack and why it was chosen, whether authentication was added, the compliance
  domain, the verification results, and every manual step an administrator must apply, such as
  OIDC client and Coolify settings. Never print secret values.
