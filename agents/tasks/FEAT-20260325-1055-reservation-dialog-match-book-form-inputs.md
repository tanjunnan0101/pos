# Reservation dialog should match public /book/ form inputs

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/84

## Problem / goal
The reservation dialog used on **satisfecho.de** should present the same input layout and form patterns as the public booking page (**https://satisfecho.de/book/** — date/time, party size, contact fields, etc.). Align UX so staff or embedded flows do not feel like a different product than the customer-facing book flow. See `docs/` for reservation/booking behaviour if relevant.

## High-level instructions for coder
- Locate the reservation dialog component(s) vs the public **book** route components and templates.
- Compare field order, labels, validation messaging, spacing, and control types; reuse shared form pieces or styles where the codebase already factors them.
- Ensure responsive behaviour matches or is intentionally documented if the dialog must differ (e.g. modal width).
- Smoke-test: open dialog and public `/book/{tenant}` for the same tenant and verify visual and functional parity for the same inputs.
