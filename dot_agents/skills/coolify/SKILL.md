---
name: coolify
description: Inspect a project and generate its Coolify deployment configuration — a minimal nixpacks.toml for build-time settings plus a managed "Coolify Deployment" section in the README for the settings Coolify reads from its own UI (Base Directory, Publish Directory, Pre/Post Deployment Commands, environment variables). Use only when the user explicitly invokes this skill or asks to generate Coolify / Nixpacks deployment config.
---

# Coolify Deployment Config

Produce the configuration needed to deploy a project to **Coolify** using its **Nixpacks** build pack. Coolify reads configuration from two separate places, so this skill writes two artifacts and routes every setting to the one Coolify actually reads:

1. **`nixpacks.toml`** — build-time settings Nixpacks reads from the repo: install / build / start commands, system packages, build variables, static assets.
2. **A managed "Coolify Deployment" section in `README.md`** — the settings Coolify reads only from its own UI/API and *cannot* read from `nixpacks.toml`: Base Directory, Publish Directory, Pre/Post Deployment Commands, and the environment variables to set. This is a checklist the user transcribes into Coolify.

Putting a Coolify-UI-only setting into `nixpacks.toml` does nothing — Coolify silently ignores it. Routing each field to the correct destination is the core job of this skill.

## Scope Guardrails

- Use this skill only after explicit user invocation. If it was loaded without that, stop applying it and follow the ordinary task instructions.
- Generate only what the project's evidence supports. Never invent commands, packages, environment variables, or secret values.
- Stay minimal: `nixpacks.toml` should contain only what differs from the Nixpacks provider's automatic behavior, and the README section should be a short transcribe-into-Coolify checklist, not a tutorial.

## Field Routing

| Setting | Destination |
| --- | --- |
| Install command | `nixpacks.toml` → `[phases.install].cmds` |
| Build command | `nixpacks.toml` → `[phases.build].cmds` |
| Start command | `nixpacks.toml` → `[start].cmd` |
| Nix / apt packages | `nixpacks.toml` → `[phases.setup]` `nixPkgs` / `aptPkgs` |
| Build-time variables / static assets | `nixpacks.toml` → `[variables]` / `[staticAssets]` |
| Base Directory | README section (Coolify UI) |
| Publish Directory (static sites) | README section (Coolify UI) |
| Pre / Post Deployment Commands | README section (Coolify UI; run via `sh -c`, not Nixpacks phases) |
| Environment variables (required / optional) | README section (Coolify UI) |

## 1. Gather Evidence

Inspect the repo before generating anything. Prefer executable code and config over prose when sources disagree.

- **Stack and package manager** — read manifests and lockfiles: `package.json` + lockfile (npm / yarn / pnpm / bun), `requirements.txt` / `pyproject.toml` / `poetry.lock` / `Pipfile`, `go.mod`, `Cargo.toml`, `composer.json` / `artisan` (PHP / Laravel), `Gemfile`, `*.csproj`, etc.
- **Build and start commands** — `package.json` `scripts`, `Procfile`, framework config, server entrypoints.
- **Runtime version pins** — `engines`, `.nvmrc`, `.python-version`, `runtime.txt`, the `go` directive in `go.mod`.
- **Static site signals** — a build output dir (`dist`, `build`, `out`, `public`), SSG/SPA frameworks (Vite, Astro, Hugo, CRA, Next static export), and the absence of a long-running server process.
- **Monorepo / subdirectory app** — workspaces, `apps/*`, `packages/*`, or a deployable manifest nested below the repo root. Informs **Base Directory**.
- **Deploy-time tooling** — database migrations or seeding that should run on deploy: `php artisan migrate`, Prisma / Drizzle / Knex migrate scripts, `manage.py migrate`, Rails `db:migrate`. Informs **Post-Deployment Command**.
- **Environment variables** — collect from `.env.example` / `.env.sample` and from code references (`process.env.X`, `import.meta.env.X`, `os.environ[...]` / `os.getenv`, `Deno.env.get`, framework config). Never invent variables or fill in secret values.

## 2. Generate `nixpacks.toml` (build-time only)

- **Emit only overrides.** Nixpacks already auto-detects standard stacks. A normal Node app that installs, builds with `npm run build`, and starts with `npm start` needs little or no `nixpacks.toml` — do not restate provider defaults. Override only for: non-standard install / build / start commands, alternate package managers, extra system packages, or static builds.
- Map detected values to:
  - `[phases.setup]` — `nixPkgs` / `aptPkgs` for extra system dependencies.
  - `[phases.install]` — `cmds` for a non-default install command.
  - `[phases.build]` — `cmds` for a non-default build command.
  - `[start]` — `cmd` for a non-default start command.
  - `[variables]` — build-time (non-secret) variables; `[staticAssets]` for files written into the image; `providers` only when genuinely required.
- **Do not invent a `PORT`.** Coolify/Nixpacks injects `PORT`; ensure the start command binds the app to `$PORT` rather than a hardcoded port.
- **Never** put Base Directory, Publish Directory, Pre/Post Deployment Commands, or runtime secrets in this file — they belong in the README section.
- **Update in place.** If `nixpacks.toml` already exists, read it, preserve intentional custom phases and keys, and change or add only what is needed. Confirm with the user before overwriting any non-trivial existing value.

## 3. Manage the README "Coolify Deployment" Section

- Use the heading `## Coolify Deployment`. The section spans from that heading to the next heading of the same or higher level.
- **Idempotent.** If a Coolify deployment section already exists (case-insensitive match on a "Coolify" heading), replace exactly that section. Otherwise append a new one. Never duplicate.
- If no `README.md` exists, create a minimal one containing this section.
- Include only the rows that apply — not every project is static or has deploy commands:
  - **Build Pack** — Nixpacks.
  - **Base Directory** — detected value; default `/`, or the subfolder for a monorepo app (e.g. `/apps/web`).
  - **Static site / Publish Directory** — only when a static build is detected. Note to enable "Is it a static site" and give the detected output dir (e.g. `/dist`).
  - **Pre-Deployment Command / Post-Deployment Command** — only when detected (e.g. `php artisan migrate --force` as post-deploy). Note they run via `sh -c`. Omit if none apply.
  - **Environment Variables** — two lists:
    - **Required** — referenced with no code default, plus expected secrets (`DATABASE_URL`, `APP_KEY`, `SECRET_KEY`, API keys). One line each with a short purpose. Never supply a value for a secret.
    - **Optional** — has a code default or fallback. One line each with its default.
- Keep it short and scannable — it is a transcribe-into-Coolify checklist, not documentation.

## 4. Verify

- Re-read `nixpacks.toml`: valid TOML, no restated provider defaults, no Coolify-UI-only fields leaked in, start command binds to `$PORT`.
- Re-read the README section: every variable and command traces back to repo evidence, no invented capabilities, and re-running the skill would replace the section rather than duplicate it.
- Run any available formatter on the touched files. If a Markdown table formatter is available in the environment, run it on the README tables.
- In the final response, report: the detected stack, what went into `nixpacks.toml` versus the README Coolify section, and the exact Coolify UI fields the user still needs to set by hand.
