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

## Coder implementation notes (2026-04-01 UTC)

1. **`POST /table-groups` / `DELETE /table-groups/{id}` HTTP 500 (slowapi):** Handlers returned plain `dict` while `@limiter.limit` is applied. slowapi requires a `starlette.responses.Response` instance to inject rate-limit headers (same pattern as `POST /tables` / `PUT /tables/{id}`). Fixed by returning **`JSONResponse`** with appropriate status codes (**201** create, **200** delete).

2. **`tests/test_reservable_capacity_turn_walkin.py` on SQLite:** In-memory `create_all` failed on `Tenant` columns using PostgreSQL **JSONB**. Tests now temporarily swap JSONB → `sqlalchemy.JSON` on `Tenant.__table__` for DDL only, then restore in `tearDown` so global model state stays correct.

---

## Testing instructions

1. **Migrate:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate` — expect **`20260401140000_table_group`** applied (or “up to date”).

2. **Backend unit:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest tests/test_reservable_capacity_turn_walkin.py -q` — expect **6 passed**.

3. **Table-groups API (auth):** With an owner/staff token that has `TABLE_WRITE`, two **inactive** same-floor tables with no open orders or blocking reservations:
   - **`POST /table-groups`** with body `{"table_ids":[id1,id2]}` → **201**, JSON body `id`, `table_ids`, `tenant_id` (not HTTP 500).
   - **`DELETE /table-groups/{id}`** → **200**, `dissolved`, `id`, `table_ids` (not HTTP 500).

4. **Frontend:** `GET /tables/with-status` should include **`group_member_ids`** / **`group_seat_total`** for grouped tables. Canvas: multi-select → Join → violet outline; Unjoin clears. Restart **`front`** if landing semver smoke compares to `package.json`.

5. **Staff orders:** When an order targets a table in a group, **`table_group_label`** (e.g. `T1 + T2`) should appear where implemented.

6. **Smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (ensure front container picked up current `front/package.json` version).

7. **Docs:** Skim **`docs/0051-table-groups-mvp.md`** for QR/session MVP behaviour.

### What to verify
- Join/unjoin API succeeds (no 500 from rate limiter).
- Capacity tests pass in Docker.
- UI and `/tables/with-status` stay consistent with grouped tables.

### Pass/fail criteria
- **PASS:** §2 all green; §3 returns 201/200 with JSON bodies, not 500; §6 landing semver matches `package.json` after front is current.
- **FAIL:** Any 500 on §3; pytest failures in §2; broken canvas or missing group fields if those areas were touched in this round.
