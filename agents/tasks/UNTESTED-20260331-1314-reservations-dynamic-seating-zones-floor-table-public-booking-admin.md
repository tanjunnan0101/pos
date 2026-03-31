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
