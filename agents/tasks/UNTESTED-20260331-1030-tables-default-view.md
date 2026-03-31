# Tables default view

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/124

## Problem / goal

Improve the Tables area so navigation preserves context and works better on tablets:

- Remember the last Tables sub-view (e.g. canvas vs list). If the user was on `/tables/canvas`, returning from Orders should land on canvas again, not reset.
- Provide a clear top control to switch between Orders and Tables (copy should follow i18n, e.g. “Pedidos” / “Orders” per language).
- On double-click of a table, scope the UI so the user sees only that table’s order (not a generic mixed view).
- Add a control to hide/show the main sidebar navigation (useful for tablet “fullscreen” style use).
- Add a fullscreen toggle using an icon only (no text on the button); place it where it fits the existing layout.

## High-level instructions for coder

- Persist or restore the last Tables view mode across route changes (Orders ↔ Tables) using existing Angular routing/state patterns; avoid breaking deep links.
- Add the Orders/Tables switcher in the shell/header for this flow and wire translations.
- Define double-click behavior on table entities so order scope filters to that table; align with current order/table models and APIs.
- Implement sidebar visibility toggle and fullscreen toggle (e.g. Fullscreen API or layout-only fullscreen) with accessible icon buttons and mobile/tablet testing.

## Implementation summary

- **`TablesAreaPreferenceService`:** `localStorage` key `pos.tables.area` (`canvas` | `list`); **`entryPath`** drives sidebar Tables link and toolbar “Tables” link. Set on **`/tables`** → list, **`/tables/canvas`** → canvas.
- **`StaffLayoutService`:** `sidebarCollapsed` + **`StaffLayoutService` / `sidebar.component`:** class **`layout--nav-collapsed`** (tablet portrait and up) hides sidebar; main content full width.
- **`StaffPosToolbarComponent`:** Segment **Orders | Tables**, icon-only **sidebar** + **fullscreen** (with `aria-label` / `title` from i18n). Used on orders + both tables views.
- **Orders:** Query **`table`** persists scope; **`tableScopeId`** filters active / not paid / history; banner + **Show all orders**; **`focusTableId` / `focusOrder`** handling keeps **`table`** when appropriate; focus resolution uses **unfiltered** order lists.
- **Double-click:** Canvas SVG table group + tiles **`table-card`** → `/staff/orders?focusTableId=&table=` (same as panel links with `table`).

## Testing instructions

1. With app on **`http://127.0.0.1:4202`** (or your HAProxy port), log in as staff with **Orders** and **Tables** modules.
2. **Last sub-view:** Open **Tables → floor plan** (`/tables/canvas`). Go to **Orders** via toolbar, then **Tables** again → should return to **floor plan** (not only `/tables`). Repeat with **list** (`/tables`) and confirm return to list.
3. **Switcher:** On **Orders** and **Tables** pages, use **Orders | Tables** segment; URLs and highlights should match.
4. **Double-click:** On **floor plan**, double-click a table → **Staff Orders** with banner “Showing orders for …” when `?table=` applies; **Show all orders** clears filter. Repeat on **tiles** view on `/tables`.
5. **Sidebar / fullscreen:** From Orders or Tables (viewport ≥ ~600px), use **hide nav** icon → main sidebar hides; **show nav** restores. Use **fullscreen** icon → document fullscreen; exit again.

**Automated:** `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` (passes; touches `/staff/orders` and `/tables`).
