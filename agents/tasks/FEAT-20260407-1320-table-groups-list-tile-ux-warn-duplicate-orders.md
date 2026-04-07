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
