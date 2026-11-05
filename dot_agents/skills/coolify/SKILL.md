---
name: coolify
description: Inspect, configure, and diagnose Coolify deployments using minimal Railpack settings and a managed README deployment section. Use when a project needs Coolify configuration or a Coolify/Railpack build is failing.
---

# Coolify Deployment Config

Produce the configuration needed to deploy a project to **Coolify** using its **Railpack** build pack. Coolify reads configuration from two separate places, so this skill writes two artifacts and routes every setting to the one Coolify actually reads:

1. **`railpack.json`** — build settings Railpack reads from the Base Directory: install / build / start commands, extra Mise and Apt packages.
2. **A managed "Coolify Deployment" section in `README.md`** — the settings Coolify reads only from its own UI/API and *cannot* read from `railpack.json`: Base Directory, Site type, Publish Directory, Ports Exposes, Pre/Post Deployment Commands, and the environment variables to set. This is a checklist the user transcribes into Coolify.

Putting a Coolify-UI-only setting into `railpack.json` does nothing. Routing each field to the correct destination is the core job of this skill.

## Scope Guardrails

- Generate only what the project's evidence supports. Never invent commands, packages, environment variables, or secret values.
- Stay minimal: `railpack.json` should contain only what differs from Railpack's automatic detection, and the README section should be a short transcribe-into-Coolify checklist, not a tutorial.
- Do not create `nixpacks.toml`. If one exists from an earlier Nixpacks setup, migrate its intentional overrides into `railpack.json` and delete it.
- Never put database migrations or seeds in Railpack build steps: the BuildKit builder is not on the `coolify` network and cannot reach its databases.

## Field Routing

| Setting                                         | Destination                                                                                                            |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Install command                                 | `railpack.json` → `steps.install.commands`                                                                             |
| Build command                                   | `railpack.json` → `steps.build.commands`                                                                               |
| Start command                                   | `railpack.json` → `deploy.startCommand`                                                                                |
| Extra Mise packages                             | `railpack.json` → `packages`                                                                                           |
| Apt packages (build / runtime)                  | `railpack.json` → `buildAptPackages` / `deploy.aptPackages`                                                            |
| Runtime version (Node / Python / Go / Ruby / …) | Native manifest pin is Railpack's runtime source; every other active repository declaration must be compatible with it |
| Base Directory                                  | README section (Coolify UI)                                                                                            |
| Site type / Publish Directory (static sites)    | README section (Coolify UI)                                                                                            |
| Ports Exposes                                   | README section (Coolify UI)                                                                                            |
| Pre / Post Deployment Commands                  | README section (Coolify UI; run via `sh -c`, not Railpack steps)                                                       |
| Environment variables (required / optional)     | README section (Coolify UI)                                                                                            |

## 1. Gather Evidence

Inspect the repo before generating anything. Prefer executable code and config over prose when sources disagree.

- **Stack and package manager** — read manifests and lockfiles: `package.json` + lockfile (npm / yarn / pnpm / bun), `requirements.txt` / `pyproject.toml` / `poetry.lock` / `Pipfile`, `go.mod`, `Cargo.toml`, `composer.json` / `artisan` (PHP / Laravel), `Gemfile`, `*.csproj`, etc.
- **Existing configuration** — read any existing `railpack.json` and any legacy `nixpacks.toml`.
- **Existing failure evidence** — read the Railpack build plan in the deployment log, the selected Mise package versions, and the exact failing build step. Generic Coolify warnings are not authoritative.
- **Build and start commands** — `package.json` `scripts`, `Procfile`, framework config, server entrypoints.
- **Runtime versions** — inspect every active declaration in native manifests, container files (`Dockerfile`, `Containerfile`), Compose files, CI workflows, version-manager files (`.nvmrc`, `.node-version`, `.python-version`, `mise.toml`, `.tool-versions`, `runtime.txt`, etc.), and deployment configuration. Also run the relevant runtime version command locally (for example, `node --version` or `python --version`) and record the currently running local version separately. The stack's native manifest pin remains Railpack's runtime source; never carry it into `railpack.json`.
- **Static site signals** — a build output dir (`dist`, `build`, `out`, `public`), SSG/SPA frameworks (Vite, Astro, Hugo, CRA, Next static export), and the absence of a long-running server process.
- **Listen port** — the port the server binds to, and whether it reads `PORT`. Informs **Ports Exposes**.
- **Monorepo / subdirectory app** — workspaces, `apps/*`, `packages/*`, or a deployable manifest nested below the repo root. Informs **Base Directory**, which is also where `railpack.json` must live.
- **Deploy-time tooling** — database migrations or seeding that should run on deploy: `php artisan migrate`, Prisma / Drizzle / Knex migrate scripts, `manage.py migrate`, Rails `db:migrate`. Informs **Post-Deployment Command**.
- **Environment variables** — collect from `.env.example` / `.env.sample` and from code references (`process.env.X`, `import.meta.env.X`, `os.environ[...]` / `os.getenv`, `Deno.env.get`, framework config). Never invent variables or fill in secret values.

### Runtime Compatibility Gate

Complete this gate before editing any project file:

1. Compare the accepted versions or ranges from every active repository runtime declaration. Treat declarations as compatible when their accepted ranges overlap; for example, `engines.node >=22` and a container using Node 24 are compatible.
2. If repository declarations are incompatible, **stop before editing**. Report every conflicting file and value, ask which version is authoritative, then align all active repository declarations to the selected version before continuing.
3. If declarations are compatible, do not rewrite them merely to make their syntax or specificity identical. If the native manifest pin is missing, add a compatible pin there as part of generating the configuration.
4. Check the currently running local runtime against the selected project range, but never change it, suppress it, or treat it as a repository declaration. If it is incompatible, report the required local runtime switch as unresolved.

## 2. Generate `railpack.json` (build only)

- **Emit only overrides.** Railpack already auto-detects standard stacks. A normal Node app that installs, builds with its `build` script, and starts with `npm start` needs no `railpack.json` — do not restate detected values, and do not create the file when there is nothing to override. Override only for: non-standard install / build / start commands, extra system packages, or extra tools.
- Start the file with `"$schema": "https://schema.railpack.com"`, then map detected values to:
  - `steps.install.commands` — a non-default install command.
  - `steps.build.commands` — a non-default build command.
  - `deploy.startCommand` — a non-default start command.
  - `packages` — extra Mise tools only (for example a CLI the build needs), not the primary runtime.
  - `buildAptPackages` / `deploy.aptPackages` — extra Apt packages needed during build / at runtime.
- **Extend, do not replace.** In `commands` and package arrays, include `"..."` to keep Railpack's generated entries and add to them (for example `["...", "ffmpeg"]`). Omit `"..."` only when deliberately replacing the generated list.
- **Do not pin the runtime version here.** Use the stack's native mechanism as Railpack's runtime source instead — `engines.node` in `package.json`, `.python-version` (or `requires-python`), the `go` directive in `go.mod`, `.ruby-version`, etc. Keep it compatible with every other active repository declaration.
  - **Never add `packages.<runtime>` or `RAILPACK_<RUNTIME>_VERSION` in addition to a native pin.** It is a duplicate source of truth that silently takes precedence over the native pin. Fix an unresolvable version by pinning a resolvable one in the native field.
  - **Polyglot builds are the exception.** Railpack detects one primary language. When the build plan lacks a second required runtime (for example Node in a Python app), add it to `packages` with a version compatible with its repository declarations, and add its install and build commands to `steps`.
- **Custom build phases** (for example a Playwright browser install) become `commands` on an existing step, or a custom step with `inputs` referencing the step it depends on.
- **Package managers come from the project.** Railpack selects the Node package manager from `packageManager`, then lockfiles, and installs that version itself. Pin the version through `packageManager`; do not add install-time workarounds such as `npm install -g` or `npx pnpm@<version>` unless the build plan proves the wrong version runs.
- **Prefer `railpack.json` over `RAILPACK_*` command and package variables.** Keep repository-owned build configuration in the file; do not duplicate it in Coolify environment variables or the Coolify Install/Build/Start Command fields.
- **Do not invent a `PORT`.** Ensure the start command binds to `$PORT` or a fixed port that matches the README's Ports Exposes value.
- **Never** put Base Directory, Site type, Publish Directory, Ports Exposes, Pre/Post Deployment Commands, or runtime secrets in this file — they belong in the README section.
- **Update in place.** If `railpack.json` already exists, read it, preserve intentional custom keys, and change or add only what is needed. Confirm with the user before overwriting any non-trivial existing value.

## 3. Manage the README "Coolify Deployment" Section

- Use the heading `## Coolify Deployment`. The section spans from that heading to the next heading of the same or higher level.
- **Idempotent.** If a Coolify deployment section already exists (case-insensitive match on a "Coolify" heading), replace exactly that section. Otherwise append a new one. Never duplicate.
- If no `README.md` exists, create a minimal one containing this section.
- Include only the rows that apply — not every project is static or has deploy commands:
  - **Build Pack** — Railpack.
  - **Base Directory** — detected value; default `/`, or the subfolder for a monorepo app (e.g. `/apps/web`).
  - **Site type** — Dynamic for a server; Static or SPA only when a static build is detected, with **Publish Directory** set to the detected output dir (e.g. `/dist`). Coolify serves static output through Nginx on port `80`.
  - **Ports Exposes** — the port the server listens on (dynamic sites only).
  - **Pre-Deployment Command / Post-Deployment Command** — only when detected (e.g. `php artisan migrate --force` as post-deploy). Note they run via `sh -c`. Omit if none apply.
  - **Environment Variables** — two lists:
    - **Required** — referenced with no code default, plus expected secrets (`DATABASE_URL`, `APP_KEY`, `SECRET_KEY`, API keys). One line each with a short purpose. Never supply a value for a secret. Mark variables the build reads as needing **Available during build**.
    - **Optional** — has a code default or fallback. One line each with its default.
- Keep it short and scannable — it is a transcribe-into-Coolify checklist, not documentation.

## 4. Verify

- Re-read every active runtime declaration and confirm their accepted ranges overlap. Confirm the native manifest is Railpack's runtime source and `railpack.json` does not duplicate it through `packages` or a runtime-version variable.
- If the `railpack` CLI is available, run `railpack plan --out <scratch>/railpack-plan.json <base-dir>` and `railpack info --format json --out <scratch>/railpack-info.json <base-dir>` with output outside the repo. Inspect the resolved runtime and package-manager versions, commands, and packages for accidental replacement. Trust these resolved values over generic Coolify warnings.
- Re-read `railpack.json`: valid JSON, `$schema` present, no restated detected values, `"..."` kept wherever generated entries should remain, no Coolify-UI-only fields leaked in.
- Re-read the README section: every variable and command traces back to repo evidence, no invented capabilities, and re-running the skill would replace the section rather than duplicate it.
- Run the project's relevant package-manager, check, test, and build commands sequentially, one command at a time. Treat any runtime-version or engine warning as failed verification even when the command exits successfully; resolve repository declaration conflicts and repeat until no such warnings remain.
- Run any available formatter on the touched files. If a Markdown table formatter is available in the environment, run it on the README tables.
- Classify deployment failures before changing configuration:
  - Mise package or version resolution failure → fix the native pin or the `packages` entry;
  - missing system library or binary → add the Apt package to the correct build or deploy list;
  - package-manager startup failure → verify the `packageManager` value and the version in the plan;
  - build step that connects to a database fails, often silently → builder network isolation; move it to deploy time;
  - application command failure → project issue;
  - failure after all build steps during image export → deployment-host issue, but do not call it OOM without host evidence.
- In the final response, report: the detected stack and runtime declarations, the local runtime and any unresolved required switch, what went into `railpack.json` versus the README Coolify section, verification results, and the exact Coolify UI fields the user still needs to set by hand.
