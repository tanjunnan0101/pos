# Fix payment-pending chip lost after marking order unpaid in Orders; restore correct persistence on Tables view

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/190
- **190**

## Problem / goal
After staff marks an order **Unpaid** (or equivalent) in **Orders**, returning to **Tables** no longer shows the **Payment pending** chip when it should. Payment-request / bill-request state must stay consistent across views and after toggling paid/unpaid.

**Expected:** If a payment or bill request is still valid, data used by the floor canvas (e.g. `/tables/with-status` or equivalent) must still expose pending payment status. Marking unpaid must not permanently clear markers that drive `payment_pending` unless product rules say so (e.g. only fully **paid** clears the request).

## High-level instructions for coder
- Trace the **Orders → Unpaid** handler: confirm it does not wipe `bill_requested_at`, request-payment metadata (`payment_method`, etc.), or other fields that feed **payment pending**, unless a deliberate reset is required.
- Ensure **GET `/tables/with-status`** (or the API the canvas uses) recomputes payment chip state from authoritative order/table fields after an unpaid transition.
- Verify the **Tables** canvas does not keep stale table payloads after navigation; refetch or merge so the view matches server truth after leaving Orders.
- **Acceptance:** Request payment → exercise unpaid flows → return to **Tables** → chip visibility matches whether payment is still outstanding per product rules.
- Add a **regression test** if the backend test suite has a suitable place for it.
