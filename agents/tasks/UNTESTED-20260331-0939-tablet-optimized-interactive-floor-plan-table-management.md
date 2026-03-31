# Tablet-optimized interactive floor plan (table management)

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/120

## Problem / goal

Deliver an interactive **floor plan** for restaurant table management, **optimized for tablets**: dark theme, grid or free-form canvas, touch-first controls, and clear visual status for each table. Tables should show capacity in a compact label (e.g. `T10 - 2`) instead of per-chair icons. Support **merge** and **unmerge/separate** for combined tables with combined capacity shown, and a **legend** mapping colors to operational states (available, open order, bill issued, occupied, reserved). Multi-area navigation (e.g. room vs terrace) and quick actions (e.g. add table/order) should match a professional POS tablet workflow.

See existing **Tables** / canvas work and `docs/` for floor and table models.

## High-level instructions for coder

- Extend or replace the current tables/floor UI toward the layout and interaction model above (drag, tap, merge/split) without breaking existing tenant data flows.
- Implement the **status color legend** and ensure colors/icons align with backend or local state for orders, bills, and reservations where applicable.
- Keep **large tap targets** and responsive layout for tablet breakpoints; verify on touch devices or emulated viewport.
- Wire merge/split to persistent representation (API/model) if not already present; avoid orphan UI-only merges.
- Add or extend smoke/Puppeteer coverage for the floor view if the repo pattern supports it.

## Implementation notes (this pass)

- **`GET /tables/with-status`:** Adds `operational_status` (`available` | `reserved` | `occupied` | `open_order` | `bill_issued`), plus `is_active` and `active_order_id` on each row. `bill_issued` maps to an active order in **`ready`** status; `open_order` to **`pending` / `preparing` / `partially_delivered`**.
- **Floor canvas (`tables-canvas.component.ts`):** Dark tablet styling, status **legend** (`data-testid="floor-plan-legend"`), compact **two-line table label** (name + seat count) instead of per-chair SVG chairs; colors driven by `operational_status`. Larger floor tabs and zoom controls (44px min) for touch.
- **Not in this pass:** Persistent **table merge/split** (requires schema/API design); follow-up when product prioritizes it.

## Testing instructions

1. Sync DB/backend; restart **`back`** if needed so **`GET /tables/with-status`** returns `operational_status`.
2. Log in as staff with **Tables** module; open **`/tables/canvas`**.
3. Confirm **dark** canvas background, **legend** (five states) top-left, tables show **name + “— N”** seats (no chair icons).
4. With a table that has an active order: verify **open_order** vs **bill_issued** colors when order status moves between kitchen pipeline and **`ready`** (e.g. from staff orders / KDS).
5. **i18n:** Spot-check **`TABLES.LEGEND_TITLE`** / **`TABLES.OP_*`** in a second locale.
6. **Regression:** `cd front && npx ng build --configuration=development` (passes). Optional: `LANDING_VERSION_ONLY=1 BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` from **`front/`**.
