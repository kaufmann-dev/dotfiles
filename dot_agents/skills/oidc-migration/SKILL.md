---
name: oidc-migration
description: Design and implement a project-appropriate migration from local authentication to an OpenID Connect provider while preserving intended access and app-owned data. Use only when the user explicitly invokes this skill.
---

# OIDC Migration

Replace the application's local authentication with OIDC. Inspect the repository and use a mature
OIDC or framework integration to design the solution that best fits the application. Do not mutate
the identity provider or deployment platform; report the settings an administrator must apply.

## Requirements

- Derive the design from the application's code, data ownership, authorization, runtime,
  deployment configuration, tests, and existing documentation.
- Configure the authentication parameters with environment variables using repository conventions.
  Never hardcode or expose secret values.
- For confidential clients, use Pocket ID's `client_secret_post`. Do not force
  `client_secret_basic`. For example, with `openid-client`, use `ClientSecretPost`.
- For every interactive Authorization Code flow, use PKCE with S256, including for confidential clients.
- Show an application-owned login screen before starting an interactive OIDC flow. Visiting the
  application or a protected document must route to that screen, not redirect immediately to the
  identity provider. Start OIDC only from the screen's explicit sign-in action, and preserve a
  validated same-origin return destination so authentication resumes the intended workflow.
- Determine whether protected resources are global, shared, or user-owned.
- For a single-user or admin-only application, use the OIDC provider's access policy as the sole
  admission control. Do not add application-level identity or claim allowlists.
- Otherwise, if the migration could broaden access to shared or privileged resources, stop and ask
  whether provider admission must be restricted or the application must add per-user authorization
  and isolation.
- After OIDC login, use the chosen library's server-side session with an HttpOnly cookie. Sessions
  expire seven days after login and are never extended; require login afterwards. Keep the
  library's default token storage unless the application has a concrete need to change it.
- Logout must end the local session. Add provider (RP-initiated) logout only when the library
  supports it natively. Do not hand-roll OIDC protocol handling or implement back-channel logout.
- Preserve app-owned data, authorization, and security-sensitive behavior. Remove obsolete local
  authentication without adding a compatibility path unless explicitly requested.
- Run the smallest reliable checks and focused authentication tests appropriate to the solution.

## Better Auth

When the application uses or adopts Better Auth (1.7 or later), use the `genericOAuth` plugin with
the provider's `discoveryUrl`. PKCE is on by default and the default token authentication is
`client_secret_post`; do not override either. Disable email/password sign-in. Start sign-in from
the login screen with `authClient.signIn.social({ provider: providerId, callbackURL })`, passing
the validated return destination as `callbackURL`; no generic OAuth client plugin is needed. Set
`session: { expiresIn: 60 * 60 * 24 * 7, disableSessionRefresh: true }`. The callback path is `/api/auth/callback/<providerId>`. `authClient.signOut({ callbackURL })` performs
provider logout through the discovered `end_session_endpoint`.

## Authentication Setup Handoff

Create or update `## Authentication Setup` in the target project's `README.md`. If no README
exists, create a minimal one using the established project name. Keep the section extremely 
concise and include only:

- A project-specific one- or two-sentence explanation of the authentication flow.
- `Public Client: On|Off`, derived from whether the application can securely store client credentials.
- `Callback URL: ...`, meaning the OIDC redirect URI for handling login authentication responses
- `Logout Callback URL: ...`, meaning the RP logout callback (do not mention the RP-initiated logout request URL)
- Every authentication environment variable, including whether it is required. If the README
  already has a section for environment variables, update that
  section and reference it here instead of duplicating variables.

For both callback URLs, include only the path after the domain.

Update an existing Authentication Setup section in place; never create duplicate sections or
duplicate environment-variable documentation.

## Final Response

Report the chosen auth and session design, preserved and removed behavior, verification results,
manual steps, and where the Authentication Setup was recorded. Never print secret values.
