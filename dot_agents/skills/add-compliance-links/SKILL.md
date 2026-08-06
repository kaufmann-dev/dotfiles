---
name: add-compliance-links
description: Implement centralized Imprint and Privacy links for a website by linking its public UI to legal.kaufmann.dev with the site's domain. Use only when the user explicitly invokes this skill.
---

# Add Compliance Links

Add direct links to the centralized compliance site instead of creating local imprint or privacy
pages. Fit the links into the target site's existing design and page structure.

## Require the Domain

Require the user to explicitly provide the website's canonical production domain, or an absolute
production URL containing it, before inspecting or changing the implementation. If the user has not
provided either, stop and ask for the domain before continuing. Do not infer it from repository
names, deployment configuration, environment variables, or URLs discovered in the project.

Use only the domain or hostname registered with the compliance site, without a scheme, port, path,
query, fragment, or trailing slash. Extract the hostname from an unambiguous absolute URL supplied
by the user. Preserve subdomains when they are part of the registered domain. If it is unclear which
hostname is registered—for example, `example.com` versus `www.example.com`—ask the user before
continuing.

## Use the Centralized URLs

Create both links using the same domain value:

```text
https://legal.kaufmann.dev/imprint?site=<domain>
https://legal.kaufmann.dev/privacy?site=<domain>
```

Label them `Imprint` and `Privacy`. URL-encode a dynamic domain query value with the project's
standard URL API. A known, validated static domain may be written directly in markup. Keep the
links as ordinary navigation unless the target project already applies a consistent external-link
policy.

Do not create local legal pages, duplicate legal text, fetch the legal documents into the target
application, or add fallback routes.

## Choose Where the Links Appear

Inspect the application's routes, authentication boundary, layouts, and shared navigation, then
apply these rules:

- For a public website, place both links in shared public chrome—normally the existing footer—so
  they are available throughout the public site.
- For an otherwise protected or admin-only application with a publicly reachable sign-in screen,
  place both links on the sign-in screen. Do not add them to the authenticated application.
- For a site whose public and admin areas intentionally share the same structure or layout, keep
  both links in that shared structure, including the admin area, for consistency.
- For an application with no publicly reachable user interface, do not add the links.

Treat public accessibility, not route naming, as the deciding factor. Do not expose authenticated
navigation or other private application details while adding links to a public sign-in screen.

## Integrate and Verify

- Reuse the project's existing layout, footer, typography, spacing, responsive behavior, and link
  states. Keep the legal links visually subordinate but readable and keyboard accessible.
- Prefer one shared implementation for all applicable public pages. Avoid duplicated per-page
  markup when an existing shared layout or component can own the links.
- Preserve unrelated behavior and avoid introducing dependencies solely for these links.
- Run the smallest reliable project check after editing. Confirm that both final href values contain
  the exact provided domain and that the links appear only in the intended public or shared UI.
- Report the domain used, the surfaces where the links appear, and the verification performed.
