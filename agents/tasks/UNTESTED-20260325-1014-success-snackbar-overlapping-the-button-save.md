# Success snackbar overlapping the button save

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/80

## Problem / goal

In **Settings**, after **Save**, the success snackbar/toast overlaps the save control. Desired behaviour: show the message more centrally on the page with a little offset from the top/bottom as appropriate, and **auto-dismiss after about one minute** (per reporter).

## High-level instructions for coder

- Identify which snackbar service / MatSnackBar config is used for settings save success.
- Adjust **position** (e.g. vertical/horizontal panel class or global config) so it does not cover the primary save action; prefer consistency with other success toasts in the app.
- Set **duration** to ~60 seconds (or configurable constant) for this flow if product agrees; ensure users can still dismiss manually if the component allows.
- Manually verify save flow on a typical settings screen after the change.

## Coder notes

- Settings uses **inline `.toast` elements** in `front/src/app/settings/settings.component.ts` (not Angular Material `MatSnackBar`). Success copy is set in `updateSettings()` after `updateTenantSettings` succeeds.
- **Change:** Toasts are **fixed, horizontally centered** below the safe-area top inset (with light shadow). **Save success** auto-hides after **60s**; **×** still clears immediately and cancels the timer. **Error** toasts use the same position but are not auto-dismissed.

## Testing instructions

### What to verify

- After **Save changes** on Settings (e.g. General or any tab with the shared form actions), the **success** message appears **near the top center** of the viewport and does **not** cover the Save/Cancel row.
- The success message **disappears on its own** after about **one minute** (or sooner if you click **×**).
- **Error** toasts (if triggered) also appear top-centered and remain until dismissed.

### How to test

1. Stack up: `docker compose -f docker-compose.yml -f docker-compose.dev.yml ps` (ensure `front` / `haproxy` healthy); app URL typically `http://127.0.0.1:4202`.
2. Log in as a user with Settings access; open **Settings** → e.g. **Business profile** or **Navigation & UI**.
3. Change a harmless field (or toggle) and click **Save changes**; confirm green toast position and that Save stays usable.
4. Optional: wait ~60s or use **×** to confirm dismiss behaviour.
5. Quick regression: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (with app reachable).

### Pass / fail

- **Pass:** Success toast is top-centered (not over Save), auto-dismiss ~60s works, manual dismiss works, Angular build clean (`docker compose … logs --tail=80 front` shows no errors).
- **Fail:** Toast still anchored to bottom over actions, no auto-dismiss for save success, or build errors.
