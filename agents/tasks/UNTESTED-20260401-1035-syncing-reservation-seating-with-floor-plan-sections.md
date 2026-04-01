# Technical requirement: syncing reservation seating with floor plan sections

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/139

## Problem / goal

Reservation “Seating” choices (e.g. no preference, indoor, terrace/outdoor) must align with the tenant’s floor model (floor tabs in Tables / canvas) so bookings and table assignment stay consistent with physical zones. Today seating is not validated against floors; slot capacity and table availability are effectively tenant-wide without floor/zone partitioning. The issue asks to classify floors (e.g. indoor vs outdoor), filter availability and assignment by that classification, and sync UI defaults (e.g. when the user is on an indoor floor tab, open the reservation modal with matching seating when sensible). Confirm whether public `/book` and staff flows share the same seating UX. Implementation notes in the issue: `Floor` (not `FloorPlan`) drives tabs; `Table` has `floor_id`; staff UI lives in `ReservationsComponent`; consider extending `Floor` rather than a separate section model unless product requires it.

## High-level instructions for coder

- Model: add or reuse a floor-level classification for seating zones (indoor / outdoor / any) and keep it consistent in API and admin/settings where floors are named or edited.
- Availability: when a seating preference is selected, limit slots and assignable tables to matching floors; define clear behavior for “no preference” (e.g. all active floors).
- UI: keep floor tabs and seating controls in sync—default seating from active floor context where appropriate; optional highlight or auto-switch floor context per product decision.
- Verify staff and public booking paths; extend tests or Puppeteer flows as needed for multi-zone tenants.

## Implementation summary (coder)

- **DB / model:** `floor.seating_zone` — `indoor` | `outdoor` | `any` (default `any`). Migration `20260401103000_floor_seating_zone.sql`.
- **API:** `GET /public/tenants/{id}/reservation-book-zones` includes `seating_zone` per floor. `FloorCreate` / `FloorUpdate` accept `seating_zone`. Reservation create (public/staff) resolves `preferred_floor_id` using floors that **match** `seating_preference` (terrace ↔ outdoor). New user-facing errors when no zone matches or floor conflicts with preference. `PUT /reservations/{id}/seat` rejects seating at a table whose floor does not match the reservation’s seating preference (when `table.floor_id` is set). `PUT /reservations/{id}` validates `preferred_floor_id` vs `seating_preference` after updates.
- **Front:** Public `/book` — seating preference is **above** the zone dropdown; zone list and slot grid use only floors compatible with the selected preference; hint when none match; auto-pick single matching zone. **Tables** list view (owner/admin): per-floor **Reservation seating** select (any / indoor / terrace-outdoor).
- **Tests:** `back/tests/test_reservation_floor_seating_zone.py` (helpers + matching). SQLite in-memory tests in this repo may fail on full `Tenant` DDL (JSONB); run against project DB or rely on integration checks below.

## Testing instructions

1. **Migrate:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m app.migrate` — schema version includes `20260401103000`.
2. **API:** `curl -s "http://127.0.0.1:4202/api/public/tenants/1/reservation-book-zones"` — each floor has `seating_zone` (`any` if unset).
3. **Tables UI:** Log in as staff with floor permissions → `/tables` → per floor, set **Reservation seating** to indoor vs outdoor vs any; save and reload.
4. **Public book:** `/book/1` — with two zones classified differently, pick **Indoor** vs **Terrace** and confirm only matching zones appear and slots load with the chosen `bookFloorId`; submit should succeed only when zone matches preference.
5. **Seat guest:** Create a reservation with indoor preference; try to seat on an outdoor-only floor’s table — expect **400** with seating mismatch message.
6. **Smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit 0; `docker compose ... logs --tail=50 front` — no TS errors.
