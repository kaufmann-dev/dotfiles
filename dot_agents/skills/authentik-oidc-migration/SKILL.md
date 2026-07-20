---
name: authentik-oidc-migration
description: Migrate an application from local authentication to Authentik OIDC while preserving app-owned data and authorization when needed. Use only when the user explicitly invokes this skill.
---

# Authentik OIDC Migration

Replace local authentication with Authentik OIDC. Do not mutate Authentik or the deployment
platform; implement the application changes and report the administrator settings to apply.

## Design

- Inspect the existing auth, session, user data, authorization, environment conventions, public
  URL handling, tests, and documentation before editing.
- Use Authorization Code Flow with PKCE through a mature OIDC or framework auth library. Use its
  callback route and configuration conventions; do not implement OIDC manually.
- Configure the target application, not the agent process, with `OIDC_DISCOVERY_URL` containing
  the complete discovery URL and `OIDC_PROVIDER_NAME` containing the user-facing provider name.
- Reuse suitable existing variable names for the client ID, client secret, session secret, and
  application base URL; otherwise use names appropriate to the implementation. Require a base URL
  only when the framework cannot determine the external origin.
- Use a confidential client and app-local session when a trusted server exists. Keep client and
  session secrets server-only. For a browser-only app, propose a backend-for-frontend and stop
  unless the user explicitly accepts a public client with PKCE, no client secret, and any required
  public-prefixed provider variables.
- Let Authentik policies control admission. Keep app-specific roles, permissions, ownership, and
  subscriptions local. Remove local passwords, registration, recovery, magic links, and duplicate
  MFA at cutover; add no fallback unless explicitly requested.

## Users and Login

- Remove authentication-only local users when no meaningful data belongs to them.
- Preserve domain users and link identities by the validated `(issuer, sub)` pair with a uniqueness
  constraint. On first login, link by normalized email only when `email_verified` is true and
  exactly one user matches; reject ambiguous or unverified matches, otherwise create a domain user.
- Read and validate the issuer through discovery. Start with `openid email profile`; request
  `offline_access` and retain tokens only for a demonstrated requirement.
- Build login and account UI from `OIDC_PROVIDER_NAME`. Keep callback, route, scope, cookie, and
  local redirect behavior in code. Implement local logout independently of optional provider
  logout.
- Never hardcode provider branding, discovery URLs, credentials, deployment origins, application
  slugs, or tenant-specific identifiers, groups, or policies.

## Documentation and Handoff

- Update `.env.example` or equivalent without real secrets. Update `README.md` with every required
  variable, its purpose, placeholder format, and secret status; create `README.md` when absent.
- Report the actual variable names, marking each as secret or non-secret and new or reused. Never
  print secret values.
- Report these administrator values after implementation:

```text
Provider name: <configured provider name>
Application name and slug: <values to configure>
Client type: Confidential | Public
Client ID variable: <implemented name>
Client secret variable: <implemented name or "none">
Redirect URI: <exact external callback URL>
Discovery URL: <configured OIDC_DISCOVERY_URL value>
Scopes: <implemented scopes>
Admission policy/group: <required Authentik policy or group>
Logout URI and method: <implemented value or "local logout only">
```

- Tell the administrator to create one Authentik application and provider, configure the exact
  callback as a Strict redirect URI, keep the issuer published by discovery, bind the intended
  admission policy or group, and enable only the implemented scope mappings. Ask the user when the
  intended audience is not discoverable.
- Tell the administrator to set the reported deployment variables, keep secrets out of public
  prefixes and browser code, match the external HTTPS callback exactly, and redeploy.

## Verify and Report

- Run the repository's smallest reliable static checks and focused auth tests.
- Verify protected-route login, callback validation through the library, user linking when
  applicable, session rotation and local logout, removed local-auth routes, and absence of secrets
  or tokens from browser output, configuration, errors, and logs.
- Report the previous and new auth/session designs, preserved data and authorization, removed
  surfaces, exact administrator settings, verification results, and manual steps.
