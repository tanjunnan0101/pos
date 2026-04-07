# Tables floor plan: center/fit all tables in view on load

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/172

## Problem / goal
When the floor plan loads (and when switching floor/area tabs), the full set of tables should be visible, centered in the viewport with comfortable padding—not stuck in a corner or flush to an edge. Match typical “fit to content” / “zoom to fit” canvas behavior.

If there are no tables, define an explicit default (e.g. centered empty canvas, scale 1). Optional: any existing “Reset view” control should reuse the same fit/center logic. Clarify whether switching floors re-fits the view (recommended: yes). Do not disrupt manual pan/zoom during a session unless the user resets or navigates away.

See **`docs/testing.md`** for tables canvas smoke scripts (e.g. `test-tables-canvas-view-options`) after changes.

## High-level instructions for coder
- Locate the tables canvas / floor plan component and how pan/zoom (or SVG/viewBox transforms) are applied today.
- On initial render for a floor and when the active floor/area changes, compute a bounding box over all table elements for that view.
- Adjust pan and zoom (or equivalent) so that bounding box is centered with a margin; avoid edge-clipping.
- Handle empty floors explicitly; align “Reset view” with the same logic if it exists.
- Smoke the floor plan after edits (switch floors, pan/zoom, ensure no regressions to drag/join flows documented in recent tables canvas work).

## Implementation summary (coder)
- **`front/src/app/tables/tables-canvas.component.ts`:** `fitViewToCurrentFloorTables()` computes an axis-aligned bounding box from existing `tableCanvasBounds`, applies padding (`viewFitPadding` 48px), sets `zoomLevel` (clamped to min/max) and `panOffset` so the content center matches the canvas center. Empty floor → `zoomLevel = 1`, `panOffset = {0,0}`.
- **Initial load:** `tryInitialViewFit()` runs once after both a tables API snapshot (`tablesSnapshotReceived`) and floors + `selectedFloorId` are ready — does **not** run on every `loadData()` refresh (join/layout reloads keep user pan/zoom).
- **Floor switch / new floor / after delete floor:** `fitViewToCurrentFloorTables()` after selection changes.
- **Reset control:** `resetZoom()` now calls `fitViewToCurrentFloorTables()` (same as fit/center).

## Testing instructions (for tester)
1. **Stack:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml` with app on HAProxy (e.g. `BASE_URL=http://127.0.0.1:4202`).
2. **Automated:** From `front/`: `BASE_URL=http://127.0.0.1:4202 HEADLESS=1 npm run test:tables-canvas-view-options` — exit 0. Also `npm run test:landing-version` — exit 0.
3. **Manual /tables/canvas:** Open floor plan with multiple tables — all should be visible with margin on first load. Switch floor tabs — view should re-fit to that floor’s tables. Empty floor — full canvas at 100% with no odd offset. Pan/zoom, then use reset — should snap to fit. Reload data without changing floor (e.g. after operations that call `loadData`) — pan/zoom should **not** reset unexpectedly.
