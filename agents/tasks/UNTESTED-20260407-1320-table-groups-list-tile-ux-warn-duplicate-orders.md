# Table groups: grouped List + Tile UX + warn on duplicate orders across joined tables

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/174

## Problem / goal
**Part A — List & Tile:** Tables that share `table_group_id` are joined on the floor plan, but List and Tile views should show **one combined row (List)** and **one combined card (Tile)** per group, not one per physical table. Primary line: combined names, combined seat count, floor once. Nested/expandable area: each member table keeps its own actions (QR, Activate, menu, copy, etc.) per `docs/0051-table-groups-mvp.md`. Ungrouped tables behave as today. Add i18n for new labels; sort groups and ungrouped tables predictably.

**Part B — Staff safety:** Warn when staff might duplicate work: if another member of the same group already has an open order or active session, show a banner or modal when activating/opening menu (name sibling tables; nudge to use existing ticket or confirm). Optional badges on List/Tile/Floor when any group member has activity. Prefer warnings and visibility (MVP); full single-order-per-group only if the API already supports it cleanly.

## High-level instructions for coder
- Read `docs/0051-table-groups-mvp.md` and current tables List/Tile/Floor data models.
- Implement grouped List/Tile presentation with nested per-table details and tokens unchanged.
- Add duplicate-order / active-session detection using existing APIs or minimal backend hooks; avoid scope creep into full order merging unless clearly supported.
- Cover i18n and predictable ordering; smoke-test join/unjoin and ordering flows.

## Implementation summary (coder)
- **`tables.component.ts`:** List view uses one summary row per group (expand to show member rows with full actions). Tile view uses one grouped card with shared banner + per-member sections reusing a shared `ng-template`. **`activateTableSession`** / **`openStaffMenu`** show **`app-confirmation-modal`** when another group member has `is_active` or `active_order_id`. Ordering: by floor name, then combined label or table name.
- **`tables-canvas.component.ts`:** Small orange dot on a table when a **sibling** in the same group has activity (SVG `<title>` for tooltip).
- **i18n:** New **`TABLES.GROUP_*`** keys in all **`front/public/i18n/*.json`**.
- **CHANGELOG:** `[Unreleased]` entry for GitHub #174.

## Testing instructions (tester)
1. **Build:** `cd front && npx ng build --configuration=development` (expect success).
2. **Smoke:** With app on `http://127.0.0.1:4202`, `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (expect exit 0).
3. **Manual / joined tables:** On **`/tables/canvas`**, join two tables (same floor, no sessions). Open **`/tables`**: confirm **List** shows one row per group (combined names, total seats); expand shows both members with independent QR/actions. **Tiles** shows one grouped card per floor section with combined header and two member blocks.
4. **Warnings:** Activate or open staff menu on table B while table A (sibling) has an active session or open order — confirm modal appears with sibling names; **Continue anyway** proceeds; Cancel dismisses.
5. **Floor dot:** With sibling activity, hover the orange dot on the inactive table shape — tooltip from **`TABLES.GROUP_SIBLING_FLOOR_DOT`**.
