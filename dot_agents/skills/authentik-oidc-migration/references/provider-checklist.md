# Kaufmann Authentik Provider Checklist

Use this reference after the application implementation determines its exact callback route,
configuration names, scopes, and logout behavior. Report the completed values for an administrator
to apply manually. Do not mutate Authentik or Coolify.

Official references:

- [Authentik OAuth2/OIDC provider](https://docs.goauthentik.io/add-secure-apps/providers/oauth2/)
- [Authentik provider property mappings](https://docs.goauthentik.io/add-secure-apps/providers/property-mappings/)
- [Authentik single logout](https://docs.goauthentik.io/add-secure-apps/providers/single-logout/)

## Authentik Application and Provider

- Create one Authentik application and OAuth2/OpenID Connect provider for the app.
- Use an app-specific slug and report it.
- Use a confidential client when the application has a trusted server. Use a public client only
  for an explicitly accepted browser-only design; public clients have no client secret.
- Configure the exact implemented callback URL as a **Strict** redirect URI. Do not leave redirect
  URIs empty or use a regular expression without an explicit requirement.
- Keep Authentik's default per-provider issuer mode unless the installation intentionally uses
  global issuer mode. The application must accept the issuer published by discovery.
- Bind the Authentik policies or groups that should admit users to the application. Do not
  duplicate this admission gate with a local allowlist. If the intended audience cannot be
  established from repository evidence, ask the user before implementation; do not deploy an
  application with undefined admission.
- Enable the standard `openid`, `email`, and `profile` scope mappings when the application uses
  those claims. Add custom group or attribute mappings only when the application has an explicit
  requirement.
- Add `offline_access` only when the application needs refresh tokens.

Report these exact values:

```text
Application name: <name>
Application/provider slug: <app-slug>
Client type: Confidential | Public
Redirect URI: https://<app-domain>/<implemented-callback-path>
Discovery URL: https://auth.kaufmann.dev/application/o/<app-slug>/.well-known/openid-configuration
Scopes: <implemented scopes>
Admission policy/group: <required Authentik policy or group>
Logout URI and method: <implemented value or "local logout only">
```

Authentik exposes the end-session endpoint at:

```text
https://auth.kaufmann.dev/application/o/<app-slug>/end-session/
```

Configure front-channel or back-channel logout only when both the application/library and the
deployed Authentik version support the selected behavior. Local application logout must remain
independent.

## Coolify

- Add every application configuration variable required by the selected OIDC library.
- Store the confidential-client secret only as a server-side secret.
- Never place the client secret in variables exposed to frontend code, including `PUBLIC_*`,
  `VITE_*`, `NEXT_PUBLIC_*`, or `NUXT_PUBLIC_*`.
- Confirm the application's externally visible base URL and callback URL use HTTPS and match the
  Authentik Strict redirect URI exactly.
- Redeploy after Authentik and Coolify settings are applied.

## Manual Verification

After configuration and deployment, verify:

1. An unauthenticated private route redirects through the application's login flow to Authentik.
2. An admitted Authentik user returns through the exact callback URL and receives an app-local
   session.
3. A user denied by Authentik policy cannot enter the application.
4. Domain-user linking preserves owned data and app-specific authorization when applicable.
5. Local logout clears the app session even when Authentik logout is not configured.
6. Removed password login, registration, reset, and change routes remain unavailable.
7. Browser-delivered code, configuration, responses, and logs do not expose the client secret or
   tokens.
