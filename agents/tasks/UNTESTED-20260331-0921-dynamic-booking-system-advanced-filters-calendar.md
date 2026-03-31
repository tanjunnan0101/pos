# Dynamic booking system with advanced filters and calendar logic

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/119

## Problem / goal

Evolve the restaurant **reservations / booking** flow (staff-facing **Reservations** area) toward a richer UI: configurable guest and service controls, allergy capture, indoor vs terrace preference, and a **weekly calendar grid** (Mon–Sun) that reflects slot capacity and closed days. Backend must enforce **per-slot guest capacity** (configurable per tenant/restaurant, not hardcoded) and support **editing existing bookings** so totals recalc and slots become “full” when capacity is reached.

Align with existing reservation models, public book flow, and `docs/` where the product already describes reservations.

## High-level instructions for coder

- Add or extend **tenant-configurable** max guests per time slot (and any related settings) in backend + admin/settings UI as appropriate.
- Implement the **top section** before the calendar: guest count selector, service type (e.g. lunch/dinner) with i18n keys, allergies yes/no with conditional detail text, indoor/terrace preference.
- Build the **7-column weekly grid** with states: selected, full (at capacity), closed/unavailable; ensure legend and styling match product intent.
- Wire **calendar refresh** when guest count or service changes so availability/full states update.
- Ensure **edit booking** paths call APIs that revalidate capacity and update slot occupancy atomically where needed.
- Add or extend tests (Puppeteer/API) for the booking flow if the repo pattern supports it.

## Implementation summary (coder)

- **DB:** `tenant.reservation_max_guests_per_slot`; `reservation` columns `service_type`, `seating_preference`, `allergies_has`, `allergies_detail` (migration `20260331120000_reservation_booking_dynamic_filters.sql`).
- **Backend:** Capacity cap applied in `_reservable_capacity_for_tenant`; optional `service` query (`lunch`|`dinner`) on `GET /reservations/book-week-slots` and `GET /reservations/next-available`; opening-hours validation + create/update use new booking fields; `PUT /reservations/{id}` uses `model_dump(exclude_unset=True)` for service/allergies updates; public `TenantSummary` includes `reservation_max_guests_per_slot`.
- **Front:** Settings → Reservations: max guests per slot. Public `/book` and staff Reservations modal: party size, service (when `hasBreak` in opening hours), seating, allergies; week grid `[serviceType]` input; list cards show service/seating/allergies when set.
- **Tests:** `pytest tests/test_book_week_slots_public.py` (pass). `npm run test:landing-version` with `BASE_URL=http://127.0.0.1:4202` (pass).

## Testing instructions

1. **Migrate:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate`
2. **Backend:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m pytest tests/test_book_week_slots_public.py -q`
3. **Frontend:** `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`
4. **Manual /book:** Open `/book/1` — set party size, optional service (if tenant has lunch/dinner break in opening hours), seating, allergies; pick a green slot; submit; confirm API stores preferences (staff list shows new lines).
5. **Settings:** Settings → Reservations — set “Max guests per time slot (optional)”; reload `/book` and confirm party max input respects cap; slot grid shows full when cap reached.
6. **Staff:** Reservations → New/Edit — same controls above grid; edit booking changes date/time/party and saves; server rejects over-capacity updates (existing `400` message).
