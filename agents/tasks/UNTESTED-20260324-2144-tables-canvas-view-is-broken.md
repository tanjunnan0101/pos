# tables > canvas view is broken

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/71

## Problem / goal
Visiting `/tables/canvas` (e.g. `http://127.0.0.1:4202/tables/canvas`) redirects to the dashboard instead of showing the floor-plan canvas. Expected: canvas loads; investigate routing, guards, and any redirect rules.

See **`docs/testing.md`** — `test:tables-canvas-view-options` / `front/scripts/test-tables-canvas-view-options.mjs` for the intended Floor plan ↔ Tiles ↔ Table navigation around `/tables/canvas`.

## High-level instructions for coder
- Reproduce locally (Docker HAProxy port, logged-in staff with table access).
- Trace Angular route config and guards for `tables/canvas` vs dashboard default redirect.
- Fix the minimal cause (route order, guard, lazy load failure, or bad link) so `/tables/canvas` renders the canvas component without bouncing to dashboard.
- Run or extend the Puppeteer tables-canvas test if behaviour changes; confirm no regression on `/tables` list/tiles views.

## Implementation note (coder)

- **Cause:** In `app.routes.ts`, `path: 'tables'` was listed before `path: 'tables/canvas'`. The router’s default **prefix** matching treats `/tables/canvas` as matching the `tables` route first, so the tables list component was activated instead of `TablesCanvasComponent`.
- **Fix:** Register `tables/canvas` **before** `tables`.

## Testing instructions

**What to verify**

- After login as **owner** or **admin**, `GET` / direct navigation to `/tables/canvas` shows the floor-plan canvas (header `data-testid="tables-canvas-header"`), not an unexpected redirect to `/dashboard` and not the tiles/table list UI for that URL.
- `/tables` still loads the tables list; view toggles and links behave as before.

**How to test**

- With the stack up (e.g. HAProxy on `4202`), from repo root:
  - `BASE_URL=http://127.0.0.1:4202 LOGIN_EMAIL=… LOGIN_PASSWORD=… node front/scripts/test-tables-canvas-view-options.mjs`
  - Or `npm run test:tables-canvas-view-options --prefix front` with the same env (see `docs/testing.md`).
- Optional quick check: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4202/` → `200` (app up).

**Pass / fail**

- **Pass:** Puppeteer script completes with exit code **0** and logs `Tables canvas view-options test passed`.
- **Fail:** Script errors, canvas header missing, or navigation ends on `/dashboard` for an owner/admin user when opening `/tables/canvas`.
