# Reservation dialog should match public /book/ form inputs

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/84

## Problem / goal
The reservation dialog used on **satisfecho.de** should present the same input layout and form patterns as the public booking page (**https://satisfecho.de/book/** — date/time, party size, contact fields, etc.). Align UX so staff or embedded flows do not feel like a different product than the customer-facing book flow. See `docs/` for reservation/booking behaviour if relevant.

## High-level instructions for coder
- Locate the reservation dialog component(s) vs the public **book** route components and templates.
- Compare field order, labels, validation messaging, spacing, and control types; reuse shared form pieces or styles where the codebase already factors them.
- Ensure responsive behaviour matches or is intentionally documented if the dialog must differ (e.g. modal width).
- Smoke-test: open dialog and public `/book/{tenant}` for the same tenant and verify visual and functional parity for the same inputs.

## Implementation notes (coder)
- **File:** `front/src/app/reservations/reservations.component.ts` (inline template + styles).
- Reordered modal fields to mirror `/book`: date → time → party size → contact block (name, phone, email) → reservation notes → customer notes → staff owner notes.
- Wrapped fields in `<form (ngSubmit)="saveReservation()">`; submit uses `BOOK.INVALID_PHONE` / `BOOK.INVALID_EMAIL` and shared `contact-validators` like `book.component.ts`.
- Removed local overrides that duplicated global `_forms.scss` `.form-group` styling; modal width slightly increased; hint string `RESERVATIONS.MODAL_DATE_TIME_HINT` documents staff calendar/time vs. public week grid.
- List cards label `client_notes` with `RESERVATIONS.RESERVATION_NOTES` for terminology parity with the book page.
- New i18n keys: `RESERVATIONS.MODAL_DATE_TIME_HINT`, `RESERVATIONS.ERROR_DATE_TIME_REQUIRED`, `RESERVATIONS.ERROR_PARTY_SIZE_RANGE` in all `front/public/i18n/*.json` locales.

---

## Testing instructions

### What to verify
- Staff **Reservations** create/edit modal shows fields in the same **order** and with the same **translation keys** for guest-visible fields as `/book/{tenant}` (date/time/party, then name, phone, email, reservation notes, customer notes).
- Inputs use the **global form** look (focus ring, borders, spacing), not the old compact grey border style.
- **Validation:** invalid phone or non-empty invalid email shows the same messages as the book page (`BOOK.INVALID_PHONE`, `BOOK.INVALID_EMAIL`).
- **Staff-only:** Owner notes block remains; hint at top explains calendar/time vs. public week grid.
- **Regression:** Save still creates/updates reservations; prefill-from-phone still works on create.

### How to test
1. Stack up: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (or `./run.sh`); note HAProxy port (e.g. `4202`).
2. Log in as a user with `reservation:write`; open `/reservations`, click **New reservation**. Confirm field order and styling; try Save with empty phone → expect invalid phone message; with `not-an-email` in email → invalid email.
3. Open `/book/1` (or your tenant id) in another tab: compare labels and order for the overlapping fields (public page uses week grid for slot; staff uses date/time inputs — expected difference, documented by hint).
4. Quick automated smoke: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`.
5. Optional: `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no Angular build errors after changes.

### Pass / fail criteria
- **Pass:** Modal field order matches spec; guest-facing labels match book keys; phone/email validation matches book; build succeeds; landing smoke test passes.
- **Fail:** Wrong field order, missing translations, save broken, or front build errors in logs.
