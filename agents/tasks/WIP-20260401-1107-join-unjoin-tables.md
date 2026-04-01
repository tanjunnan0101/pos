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

## Testing instructions

1. **Migrate:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate` — expect **`20260401140000_table_group`** applied.
2. **Backend:** From `back/` with DB up: `PYTHONPATH=. python3 -m pytest tests/test_reservable_capacity_turn_walkin.py -q` (note: SQLite in-memory tests may fail on `Tenant` JSONB; use Postgres-backed runs if needed). Manually verify **`POST /table-groups`** with two same-floor tables (no orders/reservations) returns **`id`** + **`table_ids`**; **`DELETE /table-groups/{id}`** clears **`table_group_id`** on members.
3. **Frontend:** Restart **`front`** if needed so **`package.json`** version matches the landing bar. Open **`/tables/canvas`**, **Ctrl+click** two tables on the same floor → **Join tables** → confirm violet outline and **Group** line in the panel; **Unjoin** → outlines clear. **`GET /tables/with-status`** in network tab should show **`group_member_ids`** / **`group_seat_total`**.
4. **Staff orders:** With an order on a grouped table, confirm **`table_group_label`** (e.g. `T1 + T2`) appears next to the table name on active / not-paid cards.
5. **Smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (after dev server picks up **`front/package.json`** version / commit hash).
6. **Docs:** Skim **`docs/0051-table-groups-mvp.md`** for QR/session MVP behaviour.

---

## Test report

1. **Date/time (UTC):** 2026-04-01 ~11:20–11:35 UTC. **Log window:** same (back container lines around `POST /table-groups` / `DELETE /table-groups`).

2. **Environment:** `docker-compose.yml` + `docker-compose.dev.yml`; **`BASE_URL=http://127.0.0.1:4202`** (HAProxy); branch **`development`** after `./scripts/git-sync-development.sh` (already up to date).

3. **What was tested:** Testing instructions §1–6 (migrate, pytest, POST/DELETE table-groups, tables/with-status group fields, staff orders `table_group_label`, landing smoke, docs skim).

4. **Results:**

| Criterion | Result | Evidence |
|-----------|--------|----------|
| Migration `20260401140000_table_group` applied | **PASS** | `app.migrate` reports version **20260401140000**, file **`20260401140000_table_group.sql`**, “Database is up to date”. |
| `pytest tests/test_reservable_capacity_turn_walkin.py -q` | **FAIL** | 6 failed: SQLite `create_all` on `Tenant` hits **JSONB** (`SQLiteTypeCompiler` has no `visit_JSONB`). In-memory suite not runnable as written; needs Postgres-backed harness or narrowed metadata. |
| `POST /table-groups` returns `id` + `table_ids`; `DELETE` clears `table_group_id` | **FAIL** | With owner token and two same-floor tables forced inactive to satisfy validators: **`POST /table-groups` → HTTP 500**. **`DELETE /table-groups/{id}` → HTTP 500**. Back log: **`Exception: parameter 'response' must be an instance of starlette.responses.Response`** in **slowapi** `_inject_headers` (rate limit decorator on endpoints returning a plain **dict**). |
| `GET /tables/with-status` includes `group_member_ids` / `group_seat_total` | **PASS** | For existing group (e.g. tables **634/635**): both rows show **`group_member_ids` [634,635]**, **`group_seat_total` 8**, **`table_group_id` 1**. |
| Frontend canvas join/unjoin + visuals | **FAIL** (not executed end-to-end) | Join/unjoin API path returns 500; browser flow not completed. **No full URL list** for canvas (blocked by API). |
| Staff orders: `table_group_label` on cards | **PARTIAL** | **`GET /orders`** implementation includes **`table_group_label`** when `_table_group_display_label` is set; **no tenant-1 order** in this DB on a grouped table, so **0** orders returned **`table_group_label`** — could not confirm UI copy end-to-end. |
| Smoke `npm run test:landing-version` | **FAIL** | **`Landing semver "2.0.66" !== package.json "2.0.68"`** — dev footer out of sync with `front/package.json` (restart/rebuild front or refresh hash per script message). |
| Docs **`docs/0051-table-groups-mvp.md`** | **PASS** | Skimmed: staff canvas, join rules, capacity/reservation pool, per-token menu MVP — consistent with task scope. |

5. **Overall:** **FAIL** — Failed criteria: pytest suite, **`POST`/`DELETE /table-groups`** (500 / slowapi–Response interaction), landing smoke; partial verification only for **`table_group_label`** (no suitable order on grouped table).

6. **Product owner feedback:** Table-group **data and read paths** (migration, **`/tables/with-status`** enrichment) look coherent, but **create/dissolve APIs are broken at runtime** due to the rate-limiter wrapper, so staff cannot rely on join/unjoin until that is fixed. Automated **capacity tests** should run on **Postgres** (or the SQLite test setup must avoid JSONB `Tenant` columns). After fixing the API, re-run smoke with a **restarted front** so the landing semver matches **`package.json`**.

7. **URLs tested:** **N/A — no browser** (API scripted via `http://127.0.0.1:8020` from `back` container; **`http://127.0.0.1:4202/api/health`** → 200).

8. **Relevant log excerpts:**

```
pos-back | INFO:     127.0.0.1:43502 - "POST /table-groups HTTP/1.1" 500 Internal Server Error
pos-back |   File ".../slowapi/extension.py", line 382, in _inject_headers
pos-back |     raise Exception(
pos-back | Exception: parameter `response` must be an instance of starlette.responses.Response
```

```
> front@2.0.68 test:landing-version
> FAIL: Landing semver "2.0.66" !== package.json "2.0.68"
```
