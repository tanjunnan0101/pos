# Join / unjoin tables

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/140

## Problem / goal
Staff need to treat multiple physical tables as one party: shared capacity, coherent booking, and clear rules for orders and QR/menu. Deliver a **table group** concept (e.g. `table_group_id` on `Table` or a small `TableGroup` table scoped by tenant), with APIs to create a group from N tables, dissolve it, and validate same-tenant membership and non-conflicting table state. Align session vs multiple orders on grouped tables with `docs/0008-order-management-logic.md` and `docs/0050-github-issue-52-split-plan.md` (Issue 3 — Join tables). When seating reservations, support or document MVP (e.g. join first, then seat; or target a group when party size spans tables).

**Frontend:** Floor/canvas: multi-select or explicit “Join” / “Unjoin” with a clear visual that tables are grouped. Staff orders: show the group and member tables; avoid double-booking merged capacity. **Acceptance (MVP):** staff can create and clear a join from the tables UI; orders/reservations do not double-count capacity on merged tables; document minimal safe behaviour for customer menu / table token (which token, redirects). Keep APIs extensible for possible future split-bill work.

## High-level instructions for coder
- Read `docs/0008-order-management-logic.md`, `docs/0050-github-issue-52-split-plan.md`, and related reservation/table docs before changing data model or APIs.
- Design and implement backend persistence and validation for table groups (tenant-scoped); add endpoints or extend existing table APIs as appropriate.
- Implement floor plan / tables UI for join/unjoin and group indication; wire staff order flows so capacity and booking rules stay consistent.
- Add or extend tests (API and/or e2e) for group create/dissolve, validation failures, and reservation/order behaviour on grouped tables.
- Document table-token / menu behaviour for grouped tables in a short note or existing doc if product behaviour is non-obvious.
