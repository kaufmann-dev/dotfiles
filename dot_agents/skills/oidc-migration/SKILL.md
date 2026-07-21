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
- Determine whether protected resources are global, shared, or user-owned.
- For a single-user or admin-only application, use the OIDC provider's access policy as the sole
  admission control. Do not add application-level identity or claim allowlists.
- Otherwise, if the migration could broaden access to shared or privileged resources, stop and ask
  whether provider admission must be restricted or the application must add per-user authorization
  and isolation.
- After OIDC login, create an application-local server-side session with an HttpOnly cookie. Do not
  request or store refresh tokens or use OIDC tokens as the application session. Retain the ID
  token server-side only as `id_token_hint` for logout and delete it with the local session.
- Use a 24-hour sliding idle timeout and seven-day absolute session lifetime. Reset idle only on
  authenticated user-driven requests, never passive background traffic. Require login after
  either timeout.
- Use OIDC RP-Initiated Logout, even when it ends provider-wide SSO. Do not implement back-channel
  logout.
- Preserve app-owned data, authorization, and security-sensitive behavior. Remove obsolete local
  authentication without adding a compatibility path unless explicitly requested.
- Run the smallest reliable checks and focused authentication tests appropriate to the solution.

## Authentication Setup Handoff

Create or update `## Authentication Setup` in the target project's `README.md`. If no README
exists, create a minimal one using the established project name. Keep the section extremely 
concise and include only:

- A project-specific one- or two-sentence explanation of the authentication flow.
- `Public Client: On|Off`, derived from whether the application can securely store client credentials.
- `Callback URL(s): ...`
- `Logout Callback URL(s): ...`
- Every authentication environment variable, including whether it is required. If the README
  already has a section for environment variables, update that
  section and reference it here instead of duplicating variables.

Update an existing Authentication Setup section in place; never create duplicate sections or
duplicate environment-variable documentation.

## Final Response

Report the chosen auth and session design, preserved and removed behavior, verification results,
manual steps, and where the Authentication Setup was recorded. Never print secret values.
