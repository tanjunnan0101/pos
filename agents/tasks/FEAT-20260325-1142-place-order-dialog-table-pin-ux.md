# Place an order: table PIN dialog UX

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/86

## Problem / goal
When placing an order, a dialog asks for the **table PIN**. Waiters find it hard to leave that flow to check the tables view and return to continue the order. Reporter suggests showing the **table PIN in the dialog** (e.g. upper area) so the waiter does not need to navigate away.

## High-level instructions for coder
- Find the order-placement dialog that collects the table PIN; trace how table context (table id, name, PIN or hint) is available when the dialog opens.
- Design minimal UX: surface the PIN (or safe hint if PIN must not be shown in full per policy) **inside the dialog** so waiters can complete entry without round-tripping to `/tables`.
- Preserve security expectations: if full PIN must not be displayed, show table name/number and link or secondary affordance that matches product rules.
- Test happy path and cancel/back; ensure keyboard focus and mobile layouts still work.
