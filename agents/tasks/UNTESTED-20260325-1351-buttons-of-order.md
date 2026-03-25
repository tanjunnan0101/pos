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

## Implementation
- **`front/src/app/orders/orders.component.ts`:** Removed the **`order-header-actions`** column from order cards on **Active** and **Not paid yet**; the same controls (urgent, edit, pay/finish, status dropdown, delete, then menu + print) live in **`order-actions`** in the card footer so changes stay scoped to this component (no global **`_cards.scss`** / kitchen changes). **`order-header`** uses **`align-items: center`**; **`order-header-main`** has **`flex: 1`**; **`order-actions`** uses **`flex-wrap`**, **`align-items: center`**, **`justify-content: flex-end`**. Repaired the **Not paid** header markup (delete/status had been mis-nested vs **Active**).

## Testing instructions
1. **Build:** With Docker dev stack, `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — expect `Application bundle generation complete` with no TS/NG errors.
2. **Manual:** Log in as staff, open **`/staff/orders`**. On **Active** and **Not paid yet**, confirm order cards show **meta only** in the top header row (no button row beside it); confirm **Edit**, **status**, **Pay/Finish**, **Urgent**, **Delete**, **Open menu**, and **Print** still appear in the **footer** and work. **Order history** (grid) unchanged.
3. **Regression:** Open **Kitchen** — layout unchanged; no missing header content.
4. **Automated:** From repo root with app on **4202** and `.env` demo credentials: `BASE_URL=http://127.0.0.1:4202 node front/scripts/review-order-edit-puppeteer.mjs` (exit 0). Quick smoke: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`.

**Pass criteria:** Build green; staff orders actions work from footer; kitchen unaffected; Puppeteer scripts above exit 0.
