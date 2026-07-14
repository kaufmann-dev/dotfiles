---
name: authentik-oidc-migration
description: Migrate a Kaufmann application from app-local authentication to Kaufmann Authentik OIDC while preserving app-owned data and authorization when needed. Use only when the user explicitly invokes this skill.
---

# Authentik OIDC Migration

Replace an application's local authentication with Kaufmann ID. Authentik authenticates
users and controls admission to the application; the application keeps only its own session,
domain data, and app-specific authorization.

Do not mutate Authentik or Coolify. Implement the application migration and report the exact
administrator settings from [references/provider-checklist.md](references/provider-checklist.md).

## Non-Negotiable Design

- Use `https://auth.kaufmann.dev` as the OpenID Provider.
- Use Authorization Code Flow with PKCE and a mature OIDC or framework auth library. Do not
  implement OIDC protocol handling manually.
- Use a confidential client for applications with a trusted server. Keep its client secret
  server-only.
- For a browser-only SPA, stop before implementation and propose a backend-for-frontend unless
  the user explicitly accepts a public-client design. A public client must use PKCE, no client
  secret, and library-managed browser token/session handling; record this exception in the final
  report.
- For applications with a trusted server, create an app-local session after login. Do not share
  session databases or cookies between apps, expose tokens to browser code, or store access or
  refresh tokens unless an identified application requirement needs them.
- Treat successful Authentik authentication and Authentik application policies as the admission
  gate. Keep app-specific roles, permissions, ownership, subscriptions, and feature access local.
- Remove app-local password authentication, recovery, and duplicate MFA at cutover. Add a
  temporary local fallback only when the user explicitly requests it; keep it disabled by
  default and separate from the normal login UI.

## 1. Inspect Before Editing

Establish the existing contract from code, configuration, tests, and deployment files:

- Login, registration, logout, password reset/change, magic-link, and MFA routes and UI
- Auth library, session implementation, protected-route middleware, and authorization checks
- User model plus every table, relation, role, setting, subscription, audit record, and domain
  object associated with a user
- The intended audience and any existing local admission rules that must become Authentik
  application policies or group bindings
- Environment-variable conventions, public-variable prefixes, callback/base URL handling, and
  Coolify deployment documentation
- Existing auth tests and documented setup

Identify the framework's supported OIDC libraries and callback convention. Prefer its established
auth/session integration over introducing parallel infrastructure. Never guess the callback path.

## 2. Classify Local Users

Choose the migration path from repository evidence before designing a database migration.

### Authentication-Only Users

Use fresh Authentik-only access when local user records merely enable login or global
administrator settings and no meaningful state belongs to individual users.

- Remove local users from the authentication path.
- Do not add identity-linking tables or migrate empty authentication-only records.
- Keep global application settings independent from the authenticated identity.
- Store the minimum Authentik identity or session fields required by the chosen library.

### Domain Users

Preserve and link local users when they own or receive any app-specific data, relationships,
roles, preferences, subscriptions, audit attribution, or permissions.

- Identify an external identity by the exact validated OIDC `issuer` and `sub` pair.
- Add a linked-identity table unless the application can support only one identity provider and
  direct fields on the user model are materially simpler.
- Enforce uniqueness for `(issuer, subject)`.
- On login, use an existing issuer/subject link first.
- For first-login linking, require `email_verified = true`, normalize email with the
  application's established rules, and link only when exactly one local user matches.
- Reject ambiguous or unverified email matches. Never merge accounts automatically.
- When no link or eligible existing user matches, create a new local domain user from validated
  claims because Authentik has already admitted the user.
- Preserve all local data and authorization during linking.

Do not use email as the durable external identity key. Authentik's default `email_verified` claim
can be false, so do not assume the claim is true merely because an email exists.

## 3. Implement OIDC Login

Configure the selected library through OpenID Connect discovery. Use:

```text
https://auth.kaufmann.dev/application/o/<app-slug>/.well-known/openid-configuration
```

Read and validate the issuer from discovery; do not hard-code the per-provider issuer because
Authentik can be configured with a global issuer. Request only the scopes the application needs,
starting with `openid email profile`. Request `offline_access` only when a demonstrated
requirement needs refresh tokens.

Implement the library's equivalent of:

```text
login
  -> generate state, nonce, and PKCE values
  -> redirect to Authentik

callback
  -> validate state, nonce, PKCE, signature, issuer, audience, and expiration
  -> resolve or link the local domain user when the app has domain users
  -> create or rotate the app-local session for a server-backed application
  -> redirect only to a validated local return destination
```

Use the chosen library's configuration names rather than imposing generic aliases. Ensure the
client secret cannot enter public-prefixed variables, client bundles, logs, errors, or committed
environment files.

For server-backed applications, set app-local session cookies to `HttpOnly`, `Secure`, an
appropriate `SameSite` value, and host-only scope where possible. Regenerate the session
identifier after login.

## 4. Complete the Cutover

- Make the normal login action redirect to Authentik and label it `Continue with Kaufmann ID` or
  `Sign in with Kaufmann ID`.
- Remove local email/password forms, registration, password reset/change, password hashing and
  verification, and duplicate MFA or magic-link flows.
- Replace app-local account-security controls with a link to Kaufmann ID when useful.
- Implement local logout as a state-changing request that destroys the app session and clears its
  cookie. Provider logout is optional and must not be required for local logout to work.
- Remove obsolete dependencies, environment variables, routes, tests, and unreachable code.
- Update existing `.env.example`, README, or deployment documentation when the changed setup or
  behavior is already documented. Do not create optional documentation files.

## 5. Verify

Run the repository's relevant formatting, static checks, tests, build, and non-destructive
end-to-end checks. Add focused tests that prove the applicable behavior:

- Unauthenticated requests remain protected and login redirects to Authentik.
- Callback rejects invalid state, nonce, issuer, audience, signature, and expired tokens through
  the selected library's test surface.
- Server-backed applications prevent session fixation and destroy the local session on logout.
- Authentication-only apps do not retain a redundant local-user admission gate.
- Domain-user apps resolve issuer/subject links first, link only one verified-email match,
  create a new domain user when no eligible match exists, preserve app-owned data and roles, and
  reject ambiguous or unverified matches.
- Local password login, reset, registration, and change routes no longer work.
- The client secret is absent from browser output and public configuration.

Where browser interaction is necessary, use the available Playwright MCP server. Do not use the
Playwright CLI or another headless-browser substitute. Do not claim a live Authentik login was
verified unless the required access and provider configuration were available.

## Final Report

Report:

1. The previous auth/session design and whether local users were authentication-only or domain
   users.
2. The selected OIDC library, callback route, scopes, session design, and user migration path.
3. Removed local-auth surfaces and preserved app-owned authorization/data.
4. Required application environment variables using their actual implemented names.
5. The exact Authentik and Coolify administrator checklist, including redirect and logout URIs.
6. Verification performed, results, and any manual or unverified steps.
