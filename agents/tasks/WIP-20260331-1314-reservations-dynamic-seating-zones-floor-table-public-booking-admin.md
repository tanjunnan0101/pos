# Reservations: dynamic seating zones from Floor/Table data (public booking + admin)

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/129

## Problem / goal

Public booking should follow the real floor layout: only offer seating zones that exist, have reservable tables, and are active; use owner-defined zone names; hide the location control when a single zone applies; support inactive zones (for example a closed terrace). Today, floors and `Table.floor_id` exist for staff layout, but public `/book` has no zone field, reservations do not carry floor preference, and slot capacity uses all tenant tables without floor filtering.

## High-level instructions for coder

- Add a tenant-scoped public API that lists bookable zones (reuse or extend `Floor` / equivalent): each zone has at least one reservable table, respect sort order, exclude inactive zones and zones with no tables.
- Extend admin/owner UI so zones can be created, renamed, reordered, and marked active/inactive (build on existing floor management if present).
- Public booking UI: show a location/zone selector only when there are two or more active bookable zones; otherwise omit it and define whether capacity is that zone only or unchanged global behavior per product decision.
- When a zone is selected, availability and `createReservationPublic` must count only tables on that floor; document and implement behavior for `floor_id` null tables.
- Optionally persist `preferred_floor_id` (or equivalent) on `Reservation` for staff visibility.
- Preserve tenant isolation on all new/changed endpoints; align with existing capacity rules (walk-in reserved tables, turn times, etc.).
- Add migrations and i18n for new strings; extend smoke/Puppeteer for `/book/:tenantId` if the flow changes.

## Implementation summary (coder)

- **Migration:** `back/migrations/20260331131400_floor_is_active_reservation_preferred_floor.sql` — `floor.is_active` (default true), `reservation.preferred_floor_id` (FK, nullable, ON DELETE SET NULL).
- **Public API:** `GET /public/tenants/{tenant_id}/reservation-book-zones` returns `{ floors: [{ id, name, sort_order }] }` for active floors that have at least one table on that floor.
- **Slot APIs:** `floor_id` optional query on `book-week-slots`, `book-month-day-states`, `book-day-slots`, `next-available`; staff `GET /reservations/slot-capacity` also accepts `floor_id`.
- **Venue-wide capacity:** When no `floor_id` is used, all tenant tables participate (including `table.floor_id` null). **Zone-scoped capacity:** Only tables with `table.floor_id == floor_id`; null-floor tables do not count toward a specific zone’s pool.
- **Demand:** Global = all parties on the slot. Zone = parties with `preferred_floor_id == floor`, plus parties with no preferred floor but a **seated** table on that floor (`table.floor_id`).
- **Public POST `/reservations`:** If there are ≥2 bookable zones, `preferred_floor_id` is required (or send the chosen zone). If exactly one bookable zone, backend defaults to that zone. If none (e.g. only unassigned tables), booking stays venue-wide. Staff may set any tenant floor id or omit.
- **Admin UI:** Tables → list/tiles view — per-floor checkbox “Open for online booking” (`is_active`) and ↑↓ reorder (`sort_order`). Rename/add/delete floors unchanged (canvas + existing APIs).

## Testing instructions

### What to verify

- Migrate applies on dev DB; `/book/:tenantId` loads; with **two** active bookable zones, a **Seating area** dropdown appears and slot grid respects the selection; with **one** zone, no dropdown and booking still works.
- Inactive floor (unchecked) disappears from public zones list; capacity for other zones unchanged.
- New reservation row has `preferred_floor_id` when applicable; API responses include `preferred_floor_id` / `preferred_floor_name` where loaded.

### How to test

- Run migrations: `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate`
- **API smoke:** `curl -s "http://127.0.0.1:4202/api/public/tenants/1/reservation-book-zones"` (via HAProxy) or direct back port — expect JSON `floors` array.
- **Frontend:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (build + basic nav).
- **Optional:** `node front/scripts/debug-reservations-public.mjs` with `BASE_URL` for public book flow; manual `/book/1` with two floors in DB.

### Pass / fail criteria

- Pass: migration succeeds; Angular build clean (`docker compose … logs --tail=80 front`); landing smoke test exits 0; public book page shows zone UI only when ≥2 bookable zones and submits without 400 from location rule.

- Fail: migration errors; TS/build errors in front logs; 400 on public booking when zones are misconfigured; cross-tenant data in zone endpoint.

---

## Test report

1. **Date/time (UTC) and log window**  
   - Started: **2026-03-31T13:21Z** (approx.).  
   - Finished: **2026-03-31T13:23Z**.  
   - Backend log window: same window around `GET /public/tenants/1/reservation-book-zones` and landing test navigation.

2. **Environment**  
   - Compose: `docker-compose.yml` + `docker-compose.dev.yml`.  
   - **BASE_URL:** `http://127.0.0.1:4202` (HAProxy).  
   - Branch: **development** @ **531eaff**.

3. **What was tested** (from “What to verify” + task “How to test”)  
   - `python -m app.migrate` in `back` container.  
   - `GET /api/public/tenants/1/reservation-book-zones` via HAProxy.  
   - `docker compose … logs --tail=80 front`.  
   - `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`.  
   - DB spot-check: `\d floor`, `\d reservation` in Postgres (`pos` / user `pos`).  
   - **Not completed:** manual `/book/1` two-zone UI, inactive floor filtering, `preferred_floor_id` on new rows (blocked by API/DB failure).

4. **Results**  
   - **Migrate applies cleanly / schema matches feature:** **FAIL** — `app.migrate` exits 0 and lists `20260331131400_floor_is_active_reservation_preferred_floor.sql` as **applied**, but **`floor` has no `is_active`** and **`reservation` has no `preferred_floor_id`** (`psql \d floor` / `\d reservation`). Schema version is out of sync with actual DDL.  
   - **`/book/:tenantId` loads + zone dropdown behavior (≥2 / 1 zone):** **FAIL** (not verified; public zones endpoint broken).  
   - **Inactive floor excluded from public zones; capacity unchanged for others:** **FAIL** (not exercised; endpoint 500).  
   - **`preferred_floor_id` / names in API:** **FAIL** (columns absent; not verified).  
   - **API smoke `reservation-book-zones`:** **FAIL** — `curl` returned **HTTP 500** and body `Internal Server Error`.  
   - **Angular build clean:** **PASS** — `front` logs show “Application bundle generation complete” with no TS errors in tail.  
   - **Landing smoke test:** **PASS** — `test:landing-version` **exit 0** (~44.5s); browser showed some **500**s on `/reservations`, `/tables`, `/reports` during nav (likely same missing-column issue on related queries).  
   - **Cross-tenant data in zone endpoint:** **N/A** — endpoint errors before meaningful JSON; no evidence of cross-tenant leak.

5. **Overall:** **FAIL** — Failed: migrate/schema consistency, public zones API, feature verification for booking zones and `preferred_floor_id`.

6. **Product owner feedback**  
   The feature cannot be accepted in this environment: the migration runner believes the floor/reservation migration is applied, but the database tables do not contain the new columns, so any code path selecting `floor.is_active` crashes with **ProgrammingError**. After repairing schema (re-run migration SQL or `migrate --sync-idempotent` / manual repair per ops docs), re-test the public zones endpoint and `/book/1` with one vs two active floors.

7. **URLs tested**  
   1. `http://127.0.0.1:4202/`  
   2. `http://127.0.0.1:4202/dashboard`  
   3. `http://127.0.0.1:4202/api/public/tenants/1/reservation-book-zones` (500)  
   4. Sidebar routes exercised by `test:landing-version` (16 top-level + inventory sublinks), including `/reservations`, `/tables`, `/reports` (500s observed in browser console during test).

8. **Relevant log excerpts**  

`pos-back` (traceback on zones endpoint):

```
sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedColumn) column floor.is_active does not exist
[SQL: SELECT floor.tenant_id, floor.id, floor.name, floor.sort_order, floor.is_active, ...
```

`curl` (HAProxy):

```
Internal Server Error
HTTP_CODE:500
```

`pos-front` (build):

```
Application bundle generation complete. [0.735 seconds] - 2026-03-31T13:21:33.079Z
```
