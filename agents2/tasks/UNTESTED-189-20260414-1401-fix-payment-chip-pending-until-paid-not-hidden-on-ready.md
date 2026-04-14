# Fix payment chip: keep “Payment pending” until paid; do not hide when order status becomes ready

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/189
- **189**

## Problem / goal
The floor-plan payment-pending chip/label disappears when the order transitions to kitchen ready. Product rule: **payment collection is independent of food readiness** — “Payment pending” must stay visible while a bill/payment request is active, including when `Order.status` is ready. It should clear only when the order is paid (or explicitly cancelled per product rules), not when the order becomes ready.

## High-level instructions for coder
- Audit **backend** sources for table/payment status (e.g. `GET /tables/with-status` or equivalent) and how `payment_status` / bill-request fields are derived; ensure pending payment is not dropped when the operational/order state is “ready”.
- Audit **frontend** (`tables-canvas.component.ts` and template): chip `*ngIf` / conditions — remove logic that hides the chip because operational status is only `open_order` or that excludes the ready state while payment is still requested.
- Align with existing domain fields (`bill_requested_at`, menu payment request flags, etc.); do not invent new secrets or paste issue-only payloads.
- Add or adjust tests: scenario **payment requested → kitchen marks order ready → chip still shows “Payment pending”**; after **marked paid** → chip hidden or brief “Paid” per product copy.
- Manually verify acceptance in the floor plan flow described in the issue.

## Implementation summary
- **`GET /tables/with-status` (`back/app/main.py`):** Resolve the in-flight order by **preferring `table.active_order_id`** (same idea as `get_current_order`), then **newest order id** as fallback — avoids `.first()` picking another row when multiple in-flight orders exist on the same table (which could omit `bill_requested_at` on the session order). Include **`OrderStatus.completed`** in in-flight statuses so unpaid “all delivered” sessions still participate; **`ready_to_serve`** applies to **`ready`** and **`completed`**. If `payment_status` is still **`none`**, the existing **`table.active_order_id`** fallback now sets **`pending`** when that order has **`bill_requested_at`** and is not paid/cancelled (not only **`paid`**).
- **Frontend:** Audited **`tables-canvas.component.ts`** — **`showPaymentChip`** already depends only on **`payment_status`** (`pending` | `paid`); no template change required once the API returns **`pending`** consistently.
- **Tests:** **`back/tests/test_tables_with_status_operational.py`** — added coverage for **multiple in-flight orders** (canonical `active_order_id` wins) and **completed + bill requested**.

## Testing instructions
1. **Backend (container):**  
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest /app/tests/test_tables_with_status_operational.py -q`  
   Expect **7 passed**.
2. **Regression:**  
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest /app/tests/test_close_table_finishes_seated_reservation.py -q`
3. **Manual floor plan:** Activate a table, place an order, request payment from the guest menu, then move the order to **kitchen ready** (and optionally **completed** / all delivered) **without** marking paid — the orange **Payment pending** chip should remain until paid or cancelled per product rules.
