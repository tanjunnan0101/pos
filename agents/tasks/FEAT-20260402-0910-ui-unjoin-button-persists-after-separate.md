# UI: "Unjoin" button persists after tables are separated

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/147

## Problem / goal
After a successful **Unjoin**, the UI does not fully reset: the **Unjoin** control in the header stays visible/active though tables are already separated on the map; the side panel can still show stale “joined group” metadata (e.g. wrong group label); a red **“Table group not found”** banner may appear because the client still references a deleted group id. Expected: immediately hide or disable **Unjoin**, clear joined-group labels and selection state, and avoid error banners from stale group references once unjoin completes.

## High-level instructions for coder
- On successful unjoin, refresh or reset component state so header actions, selection, and detail panel match the new non-grouped reality.
- Clear any cached table-group id used for UI so API calls do not reference a removed group.
- Align with existing tables/floor-plan state management and error handling patterns.
