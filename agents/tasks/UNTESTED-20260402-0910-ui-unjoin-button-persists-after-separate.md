# UI: "Unjoin" button persists after tables are separated

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/147

## Problem / goal
After a successful **Unjoin**, the UI does not fully reset: the **Unjoin** control in the header stays visible/active though tables are already separated on the map; the side panel can still show stale “joined group” metadata (e.g. wrong group label); a red **“Table group not found”** banner may appear because the client still references a deleted group id. Expected: immediately hide or disable **Unjoin**, clear joined-group labels and selection state, and avoid error banners from stale group references once unjoin completes.

## High-level instructions for coder
- On successful unjoin, refresh or reset component state so header actions, selection, and detail panel match the new non-grouped reality.
- Clear any cached table-group id used for UI so API calls do not reference a removed group.
- Align with existing tables/floor-plan state management and error handling patterns.

## Testing instructions

1. Stack up (e.g. HAProxy on `http://127.0.0.1:4202`). Log in as staff with tables access.
2. Open **`/tables/canvas`**. Join two tables (Ctrl/Cmd+click → **Join**, or drag-overlap flow if used).
3. Select a grouped table; confirm **Unjoin** appears and the side panel shows joined-group fields.
4. Click **Unjoin** once. **Expected:** **Unjoin** disappears (or stays disabled only while the request runs); side panel no longer shows joined-group-only UI; no red **Table group not found** banner; floor canvas shows tables ungrouped (no purple group stroke).
5. Optional: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` for a quick compile/smoke check.
