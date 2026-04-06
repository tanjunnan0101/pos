# Clarify shared venue GPS for orders and clock-in (settings copy)

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/166

## Problem / goal
Clarify the settings copy regarding shared venue GPS for orders and clock-in processes to avoid user confusion.

## High-level instructions for coder
- Review current settings copy related to GPS and venue sharing.
- Update the text in the frontend (Angular) to be clearer and more descriptive.
- Ensure the changes align with the intended user experience for both ordering and clocking in.

## Coder notes
- Updated **`SETTINGS.LOCATION_VERIFICATION_DESC`**, **`SETTINGS.ENABLE_LOCATION_CHECK_HINT`**, and **`SETTINGS.CLOCK_QR_LOCATION_VERIFY_HINT`** in all **`front/public/i18n/*.json`** locales so managers see that **one** venue coordinate + radius is used for **order location flagging** and (when enabled) **staff clock-in GPS**, not a separate “ordering-only” pin.

## Testing instructions

### What to verify
- Settings → **Location verification** intro and hint explain the shared venue point for orders and optional clock GPS.
- Settings → **Staff clock-in QR** → **Require GPS at venue for clock** hint references the same **Location verification** coordinates (one shared pin).

### How to test
- Stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (app on **`http://127.0.0.1:4202`**).
- Log in as a user who can open **Settings**; switch language in app if needed and open **Settings** → scroll to **Staff clock-in QR** and **Location verification**.
- Smoke (optional): `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`

### Pass/fail criteria
- **Pass:** New copy appears (no raw missing keys); English and at least one other locale read clearly; front build has no errors (`docker compose … logs --tail=80 front`).
- **Fail:** Missing translation keys, misleading text (implies two separate GPS pins), or Angular build errors.
