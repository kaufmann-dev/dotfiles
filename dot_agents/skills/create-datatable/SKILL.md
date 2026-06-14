---
name: create-datatable
description: Create, extend, or review production-quality data tables across frontend and full-stack projects. Use when the user explicitly asks to build or improve a tabular data view, define table columns and row actions, implement table search/filter/sort/pagination, build a server-backed table API, or review table correctness, responsiveness, accessibility, states, selection, or mutations.
---

# Create Data Table

Build data tables that are correct, accessible, responsive, and proportionate to the data size and product requirements. Inspect the project first, reuse its established patterns, and implement the complete behavior across every affected layer.

## Inspect Before Editing

Identify the project's:

- Framework, language, styling system, component library, table library, ORM, validation library, and test tools.
- Existing table primitives, reusable table components, list controllers, query helpers, API conventions, and representative table pages.
- Data source, expected row count, growth rate, sort/filter requirements, row identity, mutation behavior, and mobile requirements.
- Existing documentation and commands that apply to the change.

Prefer the project's existing table architecture when it is sound. Improve concrete defects or missing behavior instead of replacing working conventions for stylistic reasons.

Use current official documentation for installed table, framework, component, and ORM libraries before relying on library-specific APIs.

## Choose the Smallest Correct Architecture

Choose architecture from actual requirements. Do not assume every table needs a data-grid library or server-backed pagination.

### Use a Simple Semantic Table

Use native table markup or the project's table primitives when:

- The data set is small and already available.
- Search, sorting, and filtering are absent or inexpensive in memory.
- The table does not need complex selection, column state, virtualization, or server synchronization.

Do not introduce a headless table library merely to render rows and columns.

### Use a Client-Managed Data Table

Use a headless table library or existing client table abstraction when:

- The complete relevant data set is safely available on the client.
- Users need client-side sorting, filtering, pagination, selection, or column visibility.
- The added abstraction removes real state-management complexity.

Keep related operations on the same side. Client-side sorting of one server-paginated slice produces incorrect global ordering.

### Use a Server-Managed Data Table

Use server-owned search, filtering, sorting, and pagination when:

- The result set is large, unbounded, expensive, sensitive, or changes frequently.
- Queries require database indexes, authorization, joins, aggregates, or server-only data.
- The client must not download the complete result set.

The client table should render server-processed rows and must not apply conflicting local sorting, filtering, or pagination.

### Choose Pagination Deliberately

Use cursor/keyset pagination when results are large or mutable, deep sequential traversal matters, and supported sorts can be expressed as stable database orderings.

Use offset/page pagination when users need page numbers, direct page jumps, or the data set is modest and the database cost is acceptable.

Use virtualization when rendering many already-loaded rows is the bottleneck. Virtualization is not a replacement for server pagination.

Document or encode the decision in existing project conventions when it materially affects future table work.

## Define the Contract First

Before building UI, define:

- Stable row identity.
- Column meanings and displayed values.
- Allowed sort keys and directions.
- Filter names, types, defaults, and inactive representations.
- Search fields and normalization rules.
- Pagination request and response shape.
- Total-count semantics.
- Empty, no-match, loading, refreshing, and error behavior.
- Row navigation, row actions, selection, and mutation behavior.

Keep the contract typed and shared where the stack supports it. Avoid stringly typed sort and filter values scattered across UI, endpoints, and queries.

For a server-backed table, implement a complete vertical flow:

1. Shared request, response, filter, and sort types.
2. Validated server input.
3. Authorization and database query.
4. Deterministic ordering and pagination.
5. API or server-function response.
6. Initial server-rendered data when it matches the existing architecture or materially improves the required user experience.
7. Client request/controller state.
8. Presentational table and page-specific columns.
9. Focused tests across the contract.

Prefer a shared typed sort registry when it can drive allowed values, initial directions, query ordering, cursor fields, and UI metadata without becoming harder to understand than explicit branches.

## Build Correct Server Queries

Validate and normalize every inbound search, filter, sort, and pagination value. Apply authorization before returning rows or counts.

Enforce a bounded page size on the server. Validate page numbers, offsets, and cursor shapes before querying; do not trust client-side limits or controls.

For search:

- Trim input and enforce a reasonable maximum length.
- Search only intended fields.
- Escape or parameterize values through the ORM or query builder.
- Use appropriate search infrastructure when wildcard matching cannot scale.

For sorting:

- Define explicit behavior for null values.
- Define case sensitivity and locale behavior for text.
- Add a unique final tie-breaker for deterministic ordering.
- Add or verify indexes that support common filters and orderings.
- Avoid claiming an index is useful without checking the database's query behavior.

For totals:

- Return only counts the UI uses.
- Distinguish matching rows from all rows only when that distinction helps users.
- Avoid expensive exact counts when an estimate or `hasMore` signal satisfies the requirement.
- Run independent page and count queries concurrently when supported and appropriate.

Fetch one extra row to determine `hasMore` when using cursor pagination and no exact remaining count is required.

## Implement Cursor Pagination Correctly

For each cursor-supported sort:

- Define a deterministic total order ending with a unique tie-breaker.
- Encode every value required to continue that exact order.
- Validate decoded cursors before use.
- Bind cursors to the active sort and relevant filter scope.
- Mirror the database `ORDER BY` exactly in the continuation predicate.
- Handle nulls, composite sorts, custom ranking, and sort direction explicitly.
- Derive the next cursor from the last returned row, not the extra fetched row.

Opaque cursors may use validated encoded data or signed/encrypted tokens depending on sensitivity and tamper requirements. Never place secrets in a cursor.

Choose malformed-cursor behavior deliberately:

- Return a clear client error when invalid pagination input should be rejected.
- Restart from the beginning only when that behavior is harmless and intentional.

Test duplicate sort values, null values, first and final pages, changed sort/filter state, malformed cursors, and rows inserted or removed between requests.

## Structure Client State

Keep reusable request state separate from page-specific column rendering and business actions.

A reusable server-list controller or query abstraction should normally expose:

- Rows.
- Current request parameters.
- Next cursor or page state.
- Loading and refreshing state.
- Error state.
- Matching and total counts when used.
- Reset/refetch behavior.
- Load-more or page-navigation behavior.
- Optional immutable patch and reorder helpers.

On search, filter, or sort changes:

- Reset pagination.
- Replace rows rather than append.
- Prevent stale responses from overwriting newer results.
- Remove inactive parameters instead of sending ambiguous empty values.

Use request cancellation where practical. A version or request-token guard is also valid for ignoring stale responses. Prevent concurrent load-more requests.

Preserve the last successful rows during refresh failures unless the product requires clearing them. Keep API response arrays shallow or raw-reactive when the framework supports it and rows are replaced immutably.

Avoid effects for state that can be derived or updated at the event boundary.

## Define Columns Clearly

Use typed column definitions with stable explicit IDs.

For each column:

- Give the header a concise, meaningful label.
- Format raw values before presenting them.
- Use a simple renderer for simple values and a reusable renderer/snippet/component for structured or interactive cells.
- Keep column-specific width, alignment, responsive visibility, and sort metadata together when the local table abstraction supports it.
- Use tabular numerals for vertically compared numbers.
- Align numeric values consistently, normally to the end.
- Display missing values consistently.
- Preserve the full accessible value when visually truncating content.

Give action columns narrow fixed widths. Let the primary identifying column receive available space. Use stable row IDs for keyed rendering and any selection state that must survive sorting, filtering, or pagination.

Do not add selection, column visibility, drag ordering, pinning, grouping, or virtualization until the product requires them.

## Build Responsive Tables

Treat responsiveness as a content-priority problem, not only a CSS problem.

- Keep the row's primary identity and essential action available at every supported width.
- Hide lower-priority columns progressively only when users can still access their information elsewhere.
- Prefer wrapping important descriptive text.
- Use truncation for secondary single-line values when the full value remains accessible.
- Prefer horizontal scrolling over silently removing essential information.
- Consider a card/list presentation on narrow screens only when tabular comparison is no longer the primary task.
- Keep sticky headers within a deliberate scroll container and verify they do not obscure content.

Use the project's design tokens and table primitives. Avoid one-off visual systems inside the table.

## Implement Complete States

Every data table must deliberately handle the applicable states:

- Initial loading.
- Refreshing with existing rows visible.
- Loaded results.
- Empty data source.
- No matches for active search or filters.
- Error with recovery behavior.
- More results available.
- Final page reached.
- Mutation in progress when row actions exist.

Do not invent pagination, refresh, or mutation states for tables that do not support those behaviors. Distinguish an empty data source from a filtered result with zero matches. Use skeletons or a clear progress indicator for initial loading. During refresh, usually preserve rows and indicate busy state instead of replacing useful content with a spinner.

Expose errors visibly and provide retry behavior when appropriate. Never leave failures only in the console.

## Make the Table Accessible

Use native semantic table elements for tabular data. Use an ARIA grid only when spreadsheet-style cell navigation or editing is genuinely required and fully implemented.

- Provide a meaningful caption or equivalent accessible name when surrounding content does not identify the table.
- Use real column and row headers where appropriate.
- Put sorting controls in real buttons inside header cells.
- Apply `aria-sort` only to the currently sorted header.
- Show sort direction visually as well as semantically.
- Preserve visible keyboard focus.
- Set `aria-busy` while results are updating.
- Announce useful result-count or status changes with a polite live region.
- Use `role="alert"` or the project's alert component for failures.
- Give icon-only controls meaningful accessible names.

Do not make a clickable table row the only way to navigate or activate it. Provide a real link or button in the primary cell. Whole-row clicking may be an optional pointer convenience if nested controls remain independent and keyboard users have an equivalent action.

If selection exists, label row and select-all controls clearly and define whether selection applies to visible rows, the current page, or all matching results.

## Handle Search and Filters

Place global search and shared filters in a coherent toolbar. Put filters in headers only when they are genuinely column-specific.

- Label every control.
- Debounce server search requests when appropriate.
- Cancel pending debounce work during reset and component cleanup.
- Reset pagination after every search, filter, or sort change.
- Keep control state aligned with request parameters and documented defaults.
- Make reset restore exact defaults, including defaults that are not empty.
- Clear or update selected details when changed filters remove the selected row.
- Preserve filter state in the URL when shareable, bookmarkable views are valuable.

Do not debounce controls where immediate response is expected and inexpensive.

## Handle Row Actions and Mutations

Keep row actions independently accessible. Use a detail panel, dialog, or dedicated route when showing all row details would harm scanability.

For every server mutation:

- Validate and normalize mutation input independently of the table query.
- Re-authorize the action against the target row on the server.
- Return clear validation, authorization, not-found, and conflict errors.
- Prevent duplicate or conflicting writes when retries or concurrent actions are possible.
- Never rely on hidden controls, disabled buttons, or client-held row data for enforcement.

For optimistic mutations:

- Update the visible row immediately only when rollback is reliable.
- Keep open detail views synchronized with the row.
- Reorder visible rows when the active sort depends on the changed field.
- Roll back and show a clear error when persistence fails.
- Refetch when the mutation changes filters, totals, pagination membership, authorization, or fields not returned by the mutation.

If the server uses a custom composite ordering and optimistic changes affect it, maintain a small client-side comparator only for reordering already-loaded rows. It must mirror the server order and must not pretend to reorder unloaded rows.

## Apply Existing Stack Patterns Conditionally

When the project uses Svelte 5:

- Use `$props`, `$state`, `$state.raw`, `$derived`, snippets, and keyed each blocks appropriately.
- Treat props as changeable.
- Prefer event-boundary updates over `$effect`.
- Run the project's required Svelte analysis and autofix tools.

When the project uses TanStack Table:

- Use the core row model for rendering.
- Enable manual server modes when data is already sorted, filtered, or paginated by the server.
- Do not add client sorted, filtered, or paginated row models for server-owned operations.
- Configure stable `getRowId` when row state must survive reordering.

When the project uses local shadcn-style table primitives:

- Import local components rather than reinstalling or importing a separate package.
- Treat local component source as the implementation source of truth.

When the project uses Drizzle or another typed ORM:

- Express filters and orderings through typed query APIs.
- Keep schema, indexes, query behavior, and migrations aligned.
- Test generated continuation predicates or query behavior for every supported sort.

Adapt these patterns to equivalent capabilities in other stacks. Do not introduce Svelte, TanStack Table, shadcn, Drizzle, Zod, or cursor pagination merely because this skill mentions them.

## Test the Contract

Use the smallest reliable verification supported by the project.

For all tables, verify:

- Semantic structure and keyboard access.
- Responsive behavior at relevant widths.
- Loading, empty, no-match, error, and loaded states.
- Formatting and missing-value behavior.
- Row actions and nested controls.

For client-managed tables, test:

- Sort, filter, pagination, selection, and stable row identity as applicable.

For server-managed tables, test:

- Input validation and authorization.
- Every supported sort and filter.
- Reset versus append behavior.
- Stale-response and concurrent-load protection.
- Pagination boundaries and deterministic ordering.
- Cursor round trips and continuation predicates when cursors are used.
- Null and duplicate sort values.
- Clear API errors.
- Mutation validation, authorization, conflict behavior, and duplicate-submit protection where row actions exist.
- Optimistic success and rollback where meaningful.

Run the project's formatter, typecheck, focused tests, lint, and build according to the change's risk. Do not run broad end-to-end tests by default.

## Review Before Finishing

Confirm:

- The chosen architecture is no more complex than required.
- Server-owned and client-owned operations are not mixed incorrectly.
- Sorting is deterministic and pagination cannot skip or duplicate rows.
- Filters, sort options, defaults, UI state, API validation, and queries agree.
- Essential information and actions remain available on narrow screens.
- Every interactive behavior is keyboard accessible.
- All meaningful table states are visible.
- New indexes, abstractions, and dependencies are justified.
- Existing documentation is updated only when behavior or conventions materially changed.
