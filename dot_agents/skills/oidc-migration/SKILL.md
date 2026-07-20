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
- Keep deployment-specific provider configuration, credentials, and secrets in environment
  variables using repository conventions. Never hardcode or expose secret values.
- Determine whether protected resources are global, shared, or user-owned. If the migration could
  broaden access to shared or privileged resources, stop and ask whether provider admission must
  be restricted or the application must add per-user authorization and isolation.
- For an admin-only or single-user application, require an environment variable containing the
  allowed OIDC `sub` and admit only that identity.
- Use short-lived OIDC access tokens with refresh tokens. Store refresh tokens server-side and use
  an HttpOnly application session cookie that expires after 24 hours of inactivity.
- Use OIDC RP-Initiated Logout, even when it ends provider-wide SSO. Do not implement back-channel
  logout.
- Preserve app-owned data, authorization, and security-sensitive behavior. Remove obsolete local
  authentication without adding a compatibility path unless explicitly requested.
- Update existing operator-facing configuration documentation. If none exists, put the complete
  configuration handoff in the final response instead of creating documentation.
- Run the smallest reliable checks and focused authentication tests appropriate to the solution.

## Final Response

Report the chosen auth and session design, preserved and removed behavior, actual environment
variable names with secret status, exact provider registration and callback settings, scopes,
admission and logout behavior, verification results, and manual steps. Never print secret values.
