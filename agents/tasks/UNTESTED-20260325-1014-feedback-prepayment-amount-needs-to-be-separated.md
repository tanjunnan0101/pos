# Feedback / Prepayment amount needs to be separated

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/82

## Problem / goal

In **Settings → Reservations**, prepayment amount entry is awkward: users must mentally convert between cents and euros. The issue asks for separate controls (e.g. euros and cents) and to respect **multi-currency** behaviour—not a single hard-coded currency assumption.

## High-level instructions for coder

- Find reservation / prepayment settings in the frontend (and any API fields that store the amount).
- Design UX so major and minor units are clear per tenant currency (or use existing money-input patterns elsewhere in the app).
- Align with backend validation and stored representation (integer minor units vs display); avoid rounding surprises.
- Smoke-test with at least one non-EUR currency if the product supports it; document any limits in the issue if scope is constrained.

## Implementation (2026-03-25)

- **`front/src/app/settings/settings.component.ts`:** Replaced single `reservation_prepayment_cents` number field with **whole amount** + **minor units** (0–10^d−1) when `Intl` reports `maximumFractionDigits > 0` for the tenant’s **Payment settings** currency; **one whole-unit field** when the currency has no fractional digits (e.g. **JPY**, **KRW**). Values still stored as **`reservation_prepayment_cents`** (smallest currency unit). Changing **currency** in Payment settings re-splits the same stored total for display. Overflow in the minor field carries into the whole amount.
- **i18n:** Updated `SETTINGS.RESERVATION_PREPAYMENT` / hint; added `PREPAYMENT_MAJOR_LABEL`, `PREPAYMENT_MINOR_LABEL` (param `max`), `PREPAYMENT_WHOLE_AMOUNT_LABEL` in **en, de, es, fr, ca, zh-CN, hi**.
- **Backend:** Unchanged (still integer minor units).

## Testing instructions

### What to verify

- Settings → **Reservations** shows two numeric fields for prepayment when currency has decimals (e.g. **EUR**), and one field when it does not (e.g. **JPY**).
- Entering **5** whole + **50** minor with **EUR** persists **550** smallest units (same as old “cents” field).
- **Save** still works; booking page still treats amount **> 0** as prepayment enabled.
- Changing **currency** under Payment settings updates labels / field layout without corrupting the stored total until amounts are edited.

### How to test

- Stack up: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (HAProxy e.g. **4202**).
- Manual: log in as tenant admin → **Settings** → **Reservations** (or `?section=reservations`) → exercise prepayment fields → **Save** → reload settings and confirm values.
- Repeat with **Payment settings** currency **JPY**: only whole amount; set e.g. **1000**, save, reload → should match.
- Quick smoke: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` (navigates to `/settings`).

### Pass / fail

- **Pass:** Build succeeds (`docker compose … logs --tail=80 front` without TS/Angular errors); manual checks above behave as expected; landing smoke test exits **0**.
- **Fail:** Compile errors, wrong persisted total vs entered whole+minor, or JPY path showing two fraction fields.
