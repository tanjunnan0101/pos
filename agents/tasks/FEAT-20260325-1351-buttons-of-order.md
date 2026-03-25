# Buttons of order

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/92

## Problem / goal
In the order UI, **`order-header-actions`** (buttons of order) should be **removed or hidden only in the orders context** — not globally elsewhere. Layout: ensure **`align-items: center`** applies as intended for that area. See issue body and any related order-header / staff order components in `front/`.

## High-level instructions for coder
- Locate **`order-header-actions`** usage (templates + styles) and distinguish **orders** views from other screens that reuse similar chrome.
- Remove or conditionally omit those header action buttons **only where orders are shown**, without breaking other flows.
- Adjust styling so **`align-items: center`** (or equivalent flex alignment) matches the desired vertical alignment for the order header row.
- Smoke-test an order flow (create/view order) and a non-order screen that might share components to confirm no regression.
