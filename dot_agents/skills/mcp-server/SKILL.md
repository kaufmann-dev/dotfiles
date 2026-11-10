---
name: mcp-server
description: Design and implement an application's remote MCP server with OAuth, browser-based consent, client connection instructions, and connected-app management. Use when adding or changing an app's MCP server or its connection UI, not when configuring an agent to consume an existing server.
---

# MCP Server

Build an application-owned remote MCP server using the patterns in `webmail-client` and
`ai-portfolios`: one Streamable HTTP endpoint at `/mcp`, browser sign-in through Pocket ID,
explicit consent, and a settings UI for connecting clients and managing their access. Users
connect with the URL alone; no API key, manually copied bearer token, or local stdio bridge is
needed.

## Gather Evidence

Inspect the target application's authentication, authorization, data ownership, service layer,
database, server lifecycle, canonical origin, settings UI, and tests before implementing.
Preserve its intended admission policy and resource isolation. Do not make user-owned data global
because a reference project has shared data.

Use the project's stack and conventions. In a TypeScript application, prefer the official MCP
server SDK and Better Auth's MCP/OAuth integration over a custom transport or authorization
server. Check version-specific documentation through Context7 before using library APIs; keep
related Better Auth packages on matching versions. Do not copy a reference project's version
pins or framework imports blindly.

When the reference projects are available, the useful source files are:

- Both: `src/lib/server/auth.ts`, `src/routes/mcp/+server.ts`, `src/routes/consent/`,
  `src/lib/server/oauth-registration.ts`, and `src/lib/server/mcp/tools.ts`.
- `ai-portfolios`: `src/lib/server/mcp/scopes.ts`, `src/lib/server/services/connected-apps.ts`,
  and `src/routes/settings/` for tool scopes and a compact connected-apps table.
- `webmail-client`: `src/lib/server/mcp/access.ts`, `src/lib/server/mcp/connected-apps.ts`,
  `src/lib/components/access-grant-fields.svelte`, and
  `src/routes/(app)/settings/connected-apps/` for editable per-account grants.

These are examples, not runtime dependencies. Implement the behavior in the target application.

## Transport and OAuth

- Serve `/mcp` through the SDK's stateless Streamable HTTP handler. Build the tool server for
  each request with that request's verified identity, client, scopes, and applicable grants;
  never share mutable user or client context across requests.
- Use a single canonical resource URL derived from the configured public origin. The advertised
  URL, OAuth resource, token audience, and verifier must agree, including behind a reverse proxy.
- The application is the OAuth 2.1 authorization server for MCP clients; Pocket ID authenticates
  the human through OIDC. Do not accept upstream identity-provider tokens or browser session
  cookies as MCP access tokens.
- Use Authorization Code with PKCE S256, audience-bound signed access tokens lasting 15 minutes,
  and rotating refresh tokens. Support `offline_access` for MCP clients independently of the
  browser session and the application's upstream OIDC scopes.
- Publish protected-resource metadata (RFC 9728), authorization-server metadata (RFC 8414), and
  the signing keys through the library. Route origin-root `/.well-known/*` requests correctly
  even when the auth handler lives under `/api/auth`.
- Support Client ID Metadata Documents and Dynamic Client Registration so users do not have to
  pre-register each assistant or enter a client secret. Use the library's metadata fetcher and
  redirect validation rather than custom URL fetching or relaxed redirect checks.
- For CLI registrations that omit `application_type`, infer `native` only when the non-empty
  redirect list consists entirely of HTTP loopback URLs (`localhost`, `127.0.0.1`, or `[::1]`).
  Preserve explicit types and leave mixed, non-loopback, or malformed lists to normal validation.
- Verify token signature, issuer, audience, expiry, and required scopes before dispatching tools.
  Missing or invalid tokens receive HTTP 401 with a `WWW-Authenticate` challenge pointing to
  protected-resource metadata. Insufficient tool scopes receive HTTP 403 with an
  `insufficient_scope` challenge. Advertise the app's tool scopes and `offline_access` so clients
  can request useful access and refresh tokens together.
- Let unauthenticated requests reach the MCP verifier and OAuth discovery instead of redirecting
  them to HTML login. Consent and connected-app management still require the browser session.
- For the stateless POST-only endpoint used here, return 405 with `Allow: POST` for GET and
  DELETE. Leave protocol negotiation and JSON-RPC handling to the SDK.
- Persist the library's OAuth clients, consents, tokens, and signing keys using project database
  conventions. Run migrations before initializing auth when initialization seeds tables or
  discovers Pocket ID; keep builds independent of live services and runtime secrets.
- Allow legitimate cross-origin OAuth token form posts through the framework boundary while
  retaining the auth library's protections and CSRF checks on application forms. Scope any
  exemption to the auth routes; never disable CSRF protection for the whole application.

For Better Auth, the reference composition is `genericOAuth` for Pocket ID, `jwt()`,
`mcp({ loginPage, consentPage, resource, scopes, clientRegistrationDefaultScopes, ... })`, and
`cimd({ fetchClientMetadataResource, ... })`, plus the framework cookie integration. Enable
dynamic and unauthenticated client registration, set `accessTokenExpiresIn: 15 * 60`, and protect
the MCP route with `requireMcpAuth` using the same resource. The client-side `oauthProviderClient`
preserves the pending authorization flow through sign-in and consent. Verify these APIs against
the installed versions; do not assemble an additional parallel OAuth implementation.

## Permissions and Consent

Choose the permission model from the domain:

- **Stable capabilities**, as in portfolios: define named read/write OAuth scopes and one
  authoritative tool-to-scope mapping. Expose only permitted tools and enforce the same mapping
  on calls, including every call in a batch; hiding a tool from discovery is not authorization.
- **User-selected resources**, as in mail accounts: use an app-level OAuth scope and persist grants
  by user, OAuth client, and resource. Do not create an OAuth scope for every account. Load grants
  on each request and check access before every operation, including bulk actions, related
  resources, and file transfers. New resources have no grant until selected.

For editable resource grants, reuse the same fields and server validation in consent and settings.
Only accept resources the current user owns or may grant. Where the domain needs them, model
cumulative levels (for example, read < organize < send) and limits such as recent data only or
attachment access. Enforce limits on lists, searches, direct reads, mutations, and related content;
UI filtering alone is insufficient. Do not add mail-specific limits to unrelated applications.

Show a dedicated consent screen after login with the registered client's name, return host,
plain-language capabilities or resource choices, and explicit **Allow** and **Deny** actions.
Resolve client metadata through the authorization library and let it validate the pending request;
never authorize a raw `client_id` and redirect supplied by the browser. Preserve the pending
request through login and return through the library's consent result. Save resource choices
successfully before accepting consent, and show recoverable errors for expired or invalid requests.
Explain where access can later be changed or revoked.

## Tools

Keep tools as thin adapters over the same services used by the web UI. Validate inputs with the
project's schemas, scope every resource lookup correctly, and keep business rules out of routes.
Provide clear names, titles, descriptions, and accurate read-only/destructive/idempotency hints.
Server instructions should explain the intended workflow, identifiers, defaults, and meaningful
limitations, including configuration-dependent behavior.

Return concise, bounded results with enough context for the next action. Expose domain errors as
useful `isError` tool results; log unexpected failures server-side and return a generic error.
Never expose credentials or internal stack traces. Where the application supports drafts or
previews before an external action, preserve that workflow and make sending or execution explicit.

If tools transfer files, use short-lived upload/download URLs bound to the user and client, with
size limits and access rechecked when fetched. Keep bulk bytes out of tool-call JSON; return
readable extracted content or supported image content where useful. Add this only when the domain
needs file transfers.

## Connection UI

Add an **MCP server** or **Connect an app** section to the authenticated settings area. Follow the
application's typography, surfaces, borders, spacing, and responsive behavior rather than copying
either reference theme. Keep instructions visible even when no apps are connected.

Use this information hierarchy:

1. A short explanation: “Add this URL as a remote MCP server (Streamable HTTP). The app opens a
   browser window where you sign in with Pocket ID and approve its access. No API key is needed.”
   For resource grants, say that the user chooses which accounts or resources it may use.
2. The full deployed MCP URL in a monospace copy field.
3. **Claude Code** with a copyable command, followed by “Then run `/mcp` and choose Authenticate.”
4. **Codex** with a copyable command, followed by the separate login command.
5. **Claude (web and desktop)** with the settings path for adding a custom connector and pasting
   the MCP URL.
6. **ChatGPT** with the settings path for enabling Developer mode and creating a connector using
   the MCP URL and OAuth authentication.

Generate commands from the same canonical URL and a stable, project-specific server name:

```text
claude mcp add -s user --transport http <server-name> <mcp-url>
codex mcp add <server-name> --url <mcp-url>
codex mcp login <server-name>
```

The reference UI uses “Settings → Connectors → Add custom connector” for Claude and “Settings →
Apps & Connectors → Advanced settings → enable Developer mode” for ChatGPT. Verify client commands
and settings labels against current official documentation when implementing; retain the separate
client instructions and OAuth guidance if labels change. Do not replace these with a generic
“configure your client” link.

Each URL and add command needs an accessible copy button and copied feedback. Keep long commands
selectable and horizontally scrollable inside their fields without widening the page. Explain
the browser authorization step outside the code field so the copied command remains executable.

## Connected Apps UI

Place **Connected apps** below the connection instructions. List only the current user's actual
consents, joining registered client metadata for the display name and optional client URI; fall
back to the client ID when no name exists. Show the access granted and authorization date.

- For scope-only access, use a compact table: **App**, **Access**, **Authorized**, and a **Revoke**
  action. Show the client's scopes or their meaningful descriptions.
- For editable resource grants, use expandable rows with the app name, a concise summary such as
  “5 of 5 accounts,” the authorization date, and the shared grant controls inside. Provide **Save
  access** and **Revoke** actions. State that changes apply to the next request.
- Show a helpful empty state pointing to the connection steps above. Make save/revoke failures
  visible, prevent duplicate submissions, and confirm revocation with the app's name and effect.

Authorize mutations on the server using the browser session. Scope all changes to both the current
user and selected client, never revoke another user's consent or delete a shared client
registration. Revoke transactionally: remove consent, revoke refresh tokens, remove stored access
tokens, and delete resource grants when present. Require authorization again for future access.

Describe revocation honestly. Deleting a stored token does not invalidate an already-issued
stateless JWT. With scope-only authorization, explain that refresh stops immediately and existing
access expires within 15 minutes. With live resource-grant checks, removing the grants prevents
resource access on subsequent requests even while the JWT remains cryptographically valid.

## Verify

Run the smallest reliable project checks and focused authorization tests. Verify discovery and
the unauthenticated challenge, token audience and expiry rejection, scope enforcement, consent
accept/deny, user/client isolation, permission changes, and refresh-token revocation. Include
loopback registration cases when adding the inference hook. For resource grants, cover direct
and bulk access to denied resources and any content limits.

Confirm that the displayed URL and commands agree with the configured resource, all four client
instructions are present, and connected-app access/date/revoke controls reflect persisted state.
Use a browser check only when needed to verify interaction or layout; do not authorize a real
third-party app or change production grants merely to test the implementation.

Report the endpoint, chosen permission model, connection/management UI location, verification,
and any required deployment or identity-provider settings. Never print secret values.
