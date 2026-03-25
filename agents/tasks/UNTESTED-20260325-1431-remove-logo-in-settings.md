# Remove logo in settings

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/95

## Problem / goal

- On `/settings`, deleting the restaurant logo via the delete control does not remove the uploaded logo (background image delete works).
- Fix logo removal end-to-end (UI, API payload, tenant `logo_filename` / storage) so it behaves like header background deletion.

## High-level instructions for coder

- Trace the settings branding UI: logo vs header background delete handlers and API calls.
- Fix the logo delete path (frontend request shape and/or backend handler) so the tenant no longer references a logo file after delete.
- Verify in browser: upload logo → delete → logo cleared and does not reappear on reload.

## Coder notes (2026-03-25)

- **Cause:** `removeLogo()` only cleared local preview; header background already called `DELETE /tenant/header-background`.
- **Change:** Added `DELETE /tenant/logo` (unlink file, set `logo_filename` null, redacted tenant JSON like header delete). Frontend: `ApiService.deleteTenantLogo()`, settings `removeLogo()` calls it and `settings.set(updated)`.

## Testing instructions

### What to verify

- Logo remove control clears the preview and persisted tenant logo (reload settings: no logo; public/book pages if applicable show no logo).
- File removed from `uploads/{tenant_id}/logo/` when a logo existed.

### How to test

- Stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (HAProxy e.g. `http://127.0.0.1:4202`).
- **API (optional):** With staff session cookie / bearer, `DELETE /api/tenant/logo` (or `/tenant/logo` via same base as app) returns JSON with `logo_filename: null`.
- **UI:** Settings → Business profile → upload a small logo → ✕ remove → hard refresh: logo slot empty; re-open book/menu for tenant if you use logo there.
- **Smoke:** `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` (includes navigating to `/settings`).

### Pass / fail

- **Pass:** After delete + reload, `GET /tenant` (settings) shows `logo_filename` null and UI shows no server logo; no error toast; smoke test exit 0.
- **Fail:** Logo reappears after reload, 4xx/5xx on delete, or smoke test fails.
