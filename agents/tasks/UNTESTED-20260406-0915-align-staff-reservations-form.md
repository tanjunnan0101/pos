# Align staff /reservations form with public /book (zones & slot grid)

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- **Issue:** https://github.com/satisfecho/pos/issues/164

## Problem / goal
The staff reservation form should be aligned with the public booking form, specifically regarding how zones and the slot grid are displayed and used to ensure consistency between staff and public booking experiences.

## High-level instructions for coder
- Analyze the existing public `/book` component to understand the zone selection and slot grid implementation.
- Update the staff `/reservations` form to use a similar UI pattern for zones and time slot selection.
- Ensure that the logic for availability/slots is consistent across both forms.
- Verify that any differences in business logic (e.g., staff might bypass certain restrictions) are maintained while the UI remains aligned.
- Check for visual consistency in terms of layout, spacing, and interaction patterns.

## Implementation notes (coder)
- **`front/src/app/reservations/reservations.component.ts`:** Added the same zone logic as public **`BookComponent`**: `bookZonesForSeating()`, `zoneMatchesSeating()`, `onSeatingPreferenceChange()`, and **`formFloorId`** for the modal. Staff modal now shows **`BOOK.LOCATION_ZONE`** when **≥2** matching zones, and **`BOOK.NO_ZONE_FOR_SEATING`** when seating filters out all zones. **`app-reservation-week-slot-grid`** receives **`[bookFloorId]="formFloorId"`** (create and edit). **`preferred_floor_id`** is sent on **create** and **update**; **`getSlotCapacity`** uses the selected floor. Prefill-by-phone sets **`formFloorId`** from the last reservation’s **`preferred_floor_id`** before reconciling zones. Removed **`weekGridBookFloorId` / `editBaselineSeating`** in favor of explicit zone state (aligned with `/book`).
- **Duplicate task removed:** `WIP-20260406-0935-align-staff-reservations-form.md` was the same topic as this file; deleted when promoting to UNTESTED.

---

## Testing instructions

### What to verify
- Staff **New / Edit reservation** modal matches public **`/book`** for **seating → zone → week slot grid** when the tenant has reservation book zones (`/api/reservations/book-zones` / floors).
- With **two or more** zones compatible with the current seating preference, a **Location / zone** dropdown is required before save; the grid and **Seats left / Tables left** reflect the chosen zone.
- With **no** zones for the chosen seating, the inline message matches public book (**`BOOK.NO_ZONE_FOR_SEATING`**).
- Save persists **`preferred_floor_id`** (staff create/update).

### How to test
- Run stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d` (use HAProxy port from `docker compose ps`, often **4202**).
- Log in as a user with **`reservation:write`**, open **`/reservations`**, open **New reservation** (and **Edit** on an existing row).
- Exercise: change **Seating** (any / indoor / terrace), confirm zone list updates; pick date/time on the grid; submit when valid.
- Smoke (regression): `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`
- Optional: compare side-by-side with **`/book/{tenantId}`** for the same tenant.

### Pass / fail criteria
- **Pass:** Angular build succeeds (`docker compose … logs --tail=80 front`); no new TS/template errors; staff modal shows zone UI when **`bookZonesForSeating().length >= 2`**; save succeeds without spurious **`BOOK.LOCATION_ZONE_REQUIRED`** / **`BOOK.SLOT_UNAVAILABLE`** when data is valid; landing smoke test passes.
- **Fail:** Missing zone dropdown when public book shows it; grid ignores floor; **`preferred_floor_id`** not sent or wrong capacity.
