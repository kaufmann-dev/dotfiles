---
name: create-datatable
description: Guide context-sensitive creation, extension, or review of data tables in any project. Use when the user explicitly asks to build, change, or review a tabular data view, including its columns, interactions, data handling, responsiveness, accessibility, or row actions.
---

# Create Data Table

Treat this skill as a decision framework, not a checklist. Make the smallest change that satisfies the request and fits the project. Apply guidance only when the table's actual requirements make it relevant.

## Ground the Decision

Inspect only enough of the project to understand:

- The requested user workflow and expected data scale.
- Existing table components, data-loading patterns, styling, and tests.
- Which behavior already works and must remain unchanged.

Reuse sound project conventions. If a choice could materially change the data contract, interaction model, security, or scope and the answer cannot be discovered, ask before implementing it.

## Choose Proportionate Architecture

Prefer a semantic table or the project's existing primitives for straightforward tabular data.

Add client-managed sorting, filtering, pagination, selection, or column state only when the complete relevant data set can safely be handled on the client and the requested interaction needs it.

Use server-managed operations only when data size, sensitivity, authorization, query cost, or freshness requires them. Keep each operation on one side; do not sort or filter a server-paginated slice as though it were the complete result set.

Introduce a table library, shared abstraction, API, index, migration, cursor, virtualization, or new dependency only when it solves a demonstrated requirement more simply or correctly than the project's existing approach.

## Apply Relevant Guardrails

Consider these concerns only when they are reachable in the requested table:

- **Meaning:** Show the requested columns and actions with clear labels, consistent formatting, stable row identity where state depends on it, and an intentional representation for missing values.
- **Accessibility:** Prefer native table semantics and native links, buttons, and form controls. Preserve keyboard access, visible focus, accessible names, and meaningful sort state for interactive headers.
- **Responsiveness:** Preserve essential identity and actions at supported widths. Choose wrapping, truncation with access to the full value, selective hiding, or horizontal scrolling according to the content and existing layout.
- **States:** Handle only states the data flow can actually enter, such as loading, empty, no-match, error, or mutation progress. Do not add state machinery merely for completeness.
- **Data operations:** Make sorting, filtering, search, and pagination deterministic and mutually consistent. Reset or preserve state according to the established user workflow.
- **Mutations:** Keep row actions independently operable. Use optimistic updates only when failure can be handled safely.

Treat advanced behavior such as cursor pagination, bulk selection, column customization, sticky regions, or spreadsheet-style interaction as separate product requirements, never defaults.

## Protect High-Risk Boundaries

When the requested behavior crosses one of these boundaries, preserve the matching invariant:

- Validate, normalize, and bound server-owned query inputs. Allowlist supported sort and filter values, and enforce authorization for returned rows and row actions on the server.
- Apply global sorting and filtering before server pagination. Use deterministic ordering with a unique tie-breaker, and reset pagination when its sort or filter scope changes.
- When cursor pagination is actually required, validate the cursor and make its continuation values and predicate match the complete database ordering.
- Prevent stale or concurrent requests from overwriting newer results or appending the same page twice.
- Revalidate and reauthorize mutations independently of table-query state. Prevent duplicate writes when retries or concurrent actions are plausible.
- Implement sortable headers as real controls and expose the active direction semantically. If selection exists, define whether it covers visible rows, the current page, or all matching results.

## Prevent Scope Expansion

- Do not redesign a working table for stylistic preference.
- Do not implement speculative scale, states, controls, or extensibility.
- Do not replace project-native patterns without a concrete correctness or usability reason.
- Do not change backend contracts, authorization, or persistence unless the requested behavior requires it.
- Do not refactor unrelated code or create documentation unless the task requires it.

When reviewing a table, report only concrete problems relevant to the request. Distinguish correctness and accessibility defects from optional product or visual preferences, and recommend the smallest effective fix.

## Verify Proportionately

Use the project's smallest reliable check for the changed behavior. Verify applicable semantics, keyboard interaction, data operations, responsive behavior, reachable states, and row actions without inventing tests for features the table does not have. Follow project-specific verification rules and avoid broad end-to-end testing unless explicitly requested or necessary for a high-risk change.
