---
name: coolify
description: Inspect, configure, and diagnose Coolify deployments using minimal Nixpacks settings and a managed README deployment section. Use when a project needs Coolify configuration or a Coolify/Nixpacks build is failing.
---

# Coolify Deployment Config

Produce the configuration needed to deploy a project to **Coolify** using its **Nixpacks** build pack. Coolify reads configuration from two separate places, so this skill writes two artifacts and routes every setting to the one Coolify actually reads:

1. **`nixpacks.toml`** — build-time settings Nixpacks reads from the repo: install / build / start commands, system packages, build variables, static assets.
2. **A managed "Coolify Deployment" section in `README.md`** — the settings Coolify reads only from its own UI/API and *cannot* read from `nixpacks.toml`: Base Directory, Publish Directory, Pre/Post Deployment Commands, and the environment variables to set. This is a checklist the user transcribes into Coolify.

Putting a Coolify-UI-only setting into `nixpacks.toml` does nothing — Coolify silently ignores it. Routing each field to the correct destination is the core job of this skill.

## Scope Guardrails

- Generate only what the project's evidence supports. Never invent commands, packages, environment variables, or secret values.
- Stay minimal: `nixpacks.toml` should contain only what differs from the Nixpacks provider's automatic behavior, and the README section should be a short transcribe-into-Coolify checklist, not a tutorial.

## Field Routing

| Setting                                         | Destination                                                                                                           |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Install command                                 | `nixpacks.toml` → `[phases.install].cmds`                                                                             |
| Build command                                   | `nixpacks.toml` → `[phases.build].cmds`                                                                               |
| Start command                                   | `nixpacks.toml` → `[start].cmd`                                                                                       |
| Nix / apt packages                              | `nixpacks.toml` → `[phases.setup]` `nixPkgs` / `aptPkgs`                                                              |
| Runtime version (Node / Python / Go / Ruby / …) | Native manifest pin is Nixpacks' runtime source; every other active repository declaration must be compatible with it |
| Build-time variables / static assets            | `nixpacks.toml` → `[variables]` / `[staticAssets]`                                                                    |
| Base Directory                                  | README section (Coolify UI)                                                                                           |
| Publish Directory (static sites)                | README section (Coolify UI)                                                                                           |
| Pre / Post Deployment Commands                  | README section (Coolify UI; run via `sh -c`, not Nixpacks phases)                                                     |
| Environment variables (required / optional)     | README section (Coolify UI)                                                                                           |

## 1. Gather Evidence

Inspect the repo before generating anything. Prefer executable code and config over prose when sources disagree.

- **Stack and package manager** — read manifests and lockfiles: `package.json` + lockfile (npm / yarn / pnpm / bun), `requirements.txt` / `pyproject.toml` / `poetry.lock` / `Pipfile`, `go.mod`, `Cargo.toml`, `composer.json` / `artisan` (PHP / Laravel), `Gemfile`, `*.csproj`, etc.
- **Existing failure evidence** — read the generated Nixpacks plan, Dockerfile commands, selected package paths and versions, and the exact failing build step. Generic Coolify warnings are not authoritative.
- **Build and start commands** — `package.json` `scripts`, `Procfile`, framework config, server entrypoints.
- **Runtime versions** — inspect every active declaration in native manifests, container files (`Dockerfile`, `Containerfile`), Compose files, CI workflows, version-manager files (`.nvmrc`, `.node-version`, `.python-version`, `runtime.txt`, etc.), and deployment configuration. Also run the relevant runtime version command locally (for example, `node --version` or `python --version`) and record the currently running local version separately. The stack's native manifest pin remains Nixpacks' runtime source; never carry it into `nixpacks.toml`.
- **Static site signals** — a build output dir (`dist`, `build`, `out`, `public`), SSG/SPA frameworks (Vite, Astro, Hugo, CRA, Next static export), and the absence of a long-running server process.
- **Monorepo / subdirectory app** — workspaces, `apps/*`, `packages/*`, or a deployable manifest nested below the repo root. Informs **Base Directory**.
- **Deploy-time tooling** — database migrations or seeding that should run on deploy: `php artisan migrate`, Prisma / Drizzle / Knex migrate scripts, `manage.py migrate`, Rails `db:migrate`. Informs **Post-Deployment Command**.
- **Environment variables** — collect from `.env.example` / `.env.sample` and from code references (`process.env.X`, `import.meta.env.X`, `os.environ[...]` / `os.getenv`, `Deno.env.get`, framework config). Never invent variables or fill in secret values.

### Runtime Compatibility Gate

Complete this gate before editing any project file:

1. Compare the accepted versions or ranges from every active repository runtime declaration. Treat declarations as compatible when their accepted ranges overlap; for example, `engines.node >=22` and a container using Node 24 are compatible.
2. If repository declarations are incompatible, **stop before editing**. Report every conflicting file and value, ask which version is authoritative, then align all active repository declarations to the selected version before continuing.
3. If declarations are compatible, do not rewrite them merely to make their syntax or specificity identical. If the native manifest pin is missing, add a compatible pin there as part of generating the configuration.
4. Check the currently running local runtime against the selected project range, but never change it, suppress it, or treat it as a repository declaration. If it is incompatible, report the required local runtime switch as unresolved.

## 2. Generate `nixpacks.toml` (build-time only)

- **Emit only overrides.** Nixpacks already auto-detects standard stacks. A normal Node app that installs, builds with `npm run build`, and starts with `npm start` needs little or no `nixpacks.toml` — do not restate provider defaults. Override only for: non-standard install / build / start commands, alternate package managers, extra system packages, or static builds.
- Map detected values to:
  - `[phases.setup]` — `nixPkgs` / `aptPkgs` for extra system dependencies.
  - `[phases.install]` — `cmds` for a non-default install command.
  - `[phases.build]` — `cmds` for a non-default build command.
  - `[start]` — `cmd` for a non-default start command.
  - `[variables]` — build-time (non-secret) variables; `[staticAssets]` for files written into the image; `providers` only when genuinely required.
- **Do not pin the runtime version here.** Use the stack's native mechanism as Nixpacks' runtime source instead — `engines.node` in `package.json`, `.python-version` (or `requires-python`), the `go` directive in `go.mod`, `.ruby-version`, etc. Keep it compatible with every other active repository declaration. Nixpacks' providers are version-aware: they map the native field to the correct nixpkgs archive, whereas a raw `nixPkgs = ["nodejs_24"]` in `[phases.setup]` references an attribute in Nixpacks' default archive and can fail for newer versions.
  - **Never add `NIXPACKS_NODE_VERSION` (or a `nixPkgs` runtime pin) in addition to a native pin.** It is a duplicate source of truth and buys nothing — the native field resolves against the *same* nixpkgs archive, so if a version is unavailable the env var cannot reach it either. The fix for an unavailable version is to pin an available one in the native field, not to add the env var. Do not add it speculatively or "defensively."
  - The env var is an **escape hatch, not a default.** Reach for it only after a deploy has *actually* failed to resolve the runtime from the native field, and when used it **replaces** the native pin — the two are mutually exclusive.
- **For Node package managers, inspect the generated plan.** `packageManager` is the requested version, but an older Nixpacks release can still inject an outdated Corepack or package-manager binary earlier on `PATH`. Do not assume `npm install -g` wins command resolution.
  - When the generated plan cannot run the pinned pnpm version, override only the affected phases and invoke that exact version explicitly:

    ```toml
    [phases.install]
    cmds = ["npx --yes pnpm@<version> install --frozen-lockfile"]

    [phases.build]
    cmds = ["npx --yes pnpm@<version> run build"]
    ```

  - Do not use undocumented variables such as `NIXPACKS_COREPACK_VERSION`.
- **Do not pin `nixpkgsArchive` by default.** Let the provider select it. Pin only to resolve a confirmed archive mismatch and verify the revision contains every required package. In mixed-language builds, a `CXXABI_* not found` error usually means phases pulled incompatible Nix toolchains; align them deliberately or use a project Dockerfile instead of changing Node versions blindly.
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

- Re-read every active runtime declaration and confirm their accepted ranges overlap. Confirm the native manifest is Nixpacks' runtime source and `nixpacks.toml` does not duplicate it through `nixPkgs` or a runtime-version variable.
- Run `nixpacks plan -f json .` and inspect the selected runtime package, archive, package-manager commands, and every provider phase. Trust these resolved values over generic Coolify warnings.
- Re-read `nixpacks.toml`: valid TOML, no restated provider defaults, no Coolify-UI-only fields leaked in, start command binds to `$PORT`.
- Re-read the README section: every variable and command traces back to repo evidence, no invented capabilities, and re-running the skill would replace the section rather than duplicate it.
- Run the project's relevant package-manager, check, test, and build commands sequentially, one command at a time. Treat any runtime-version or engine warning as failed verification even when the command exits successfully; resolve repository declaration conflicts and repeat until no such warnings remain.
- Run any available formatter on the touched files. If a Markdown table formatter is available in the environment, run it on the README tables.
- Classify deployment failures before changing configuration:
  - setup/package lookup failure → archive mismatch;
  - runtime `CXXABI_*` failure → mixed Nix toolchains;
  - package-manager startup failure → verify the executable path and version;
  - application command failure → project issue;
  - failure after all build steps during image export → deployment-host issue, but do not call it OOM without host evidence.
- In the final response, report: the detected stack and runtime declarations, the local runtime and any unresolved required switch, what went into `nixpacks.toml` versus the README Coolify section, verification results, and the exact Coolify UI fields the user still needs to set by hand.
