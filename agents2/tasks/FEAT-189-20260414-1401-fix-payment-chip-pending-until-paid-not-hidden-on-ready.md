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
