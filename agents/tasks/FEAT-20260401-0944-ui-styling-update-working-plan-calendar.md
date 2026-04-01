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
