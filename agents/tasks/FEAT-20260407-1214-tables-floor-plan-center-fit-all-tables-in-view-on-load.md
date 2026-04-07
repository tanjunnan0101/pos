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
