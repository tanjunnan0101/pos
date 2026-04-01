# UI Styling Update: Working Plan Calendar

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/138

## Problem / goal

In **Working Plan** → **main calendar view**, adjust layout spacing: widen the calendar grid container and give day cells more vertical room so shift entries fit better. Changes must stay **scoped to the Working Plan module** (no global stylesheet side effects).

Target CSS (conceptual; implement with the project’s usual encapsulation — component styles / BEM / host selectors as appropriate):

- Main grid container: cap or set max width around **100rem** for the calendar grid.
- Day/cell: **min-height ~7.75rem** so cells are taller.

See **`docs/0021-working-plan.md`** if it documents Working Plan layout or calendar structure.

## High-level instructions for coder

- Locate the Working Plan calendar grid and cell markup/CSS (likely `working-plan` component styles and templates).
- Apply the width and min-height rules **only within the Working Plan container** (e.g. host/component wrapper class), not app-wide.
- Verify visually at desktop widths; avoid breaking week view or other Working Plan tabs.
- Run a relevant smoke check if one exists (e.g. `npm run test:working-plan` from `front/` with `BASE_URL` and login env) and confirm `docker compose` front logs stay clean after the change.

## Implementation

- **`front/src/app/working-plan/working-plan.component.ts`** (component-scoped styles): `.calendar-grid` — `width: 100%`, `max-width: 100rem` (replaces `42rem`). `.calendar-cell` — `min-height: 7.75rem` (was `4.75rem`). `.calendar-cell-header` — `min-height: auto` so the Mon–Sun header row does not inherit the tall day-cell minimum.

## Testing instructions

1. With the stack up (e.g. HAProxy on **4202**), from **`front/`** and repo **`.env`** providing `LOGIN_EMAIL` / `LOGIN_PASSWORD` (or `DEMO_*`):
   - `BASE_URL=http://127.0.0.1:4202 npm run test:working-plan`
   - `BASE_URL=http://127.0.0.1:4202 npm run test:working-plan-calendar`
2. Check **`docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front`** — Angular build completes without errors after the change.
3. **Manual:** `/working-plan/calendar` — calendar grid grows with content width up to ~100rem; day cells are taller; switch to **Week** view and confirm week list still behaves as before.
