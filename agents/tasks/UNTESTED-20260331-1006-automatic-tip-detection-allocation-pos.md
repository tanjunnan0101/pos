# Automatic tip detection and allocation (checkout / payments)

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/123

## Problem / goal

When a payment total exceeds the bill (e.g. card charge above menu total), treat the difference as a potential **tip**, let staff confirm or adjust before closing, attribute tips to the right **employee/session**, and keep **revenue vs tips** separable for reporting and compliance. Align with existing orders, payments, and reporting models.

## High-level instructions for coder

- **Detection:** On payment capture (especially card), compare amount paid to bill total; when the amount paid exceeds the bill, compute the difference and surface a clear confirmation step (“assign as tip?”) before finalizing.
- **Attribution:** Link confirmed tips to the waiter/employee tied to the table or POS session per product rules.
- **Reporting:** Ensure daily/Z-style and related reports show revenue vs tips distinctly (tips not rolled into taxable sales as configured by product/accounting rules).
- **Settings:** Add a tenant-level toggle between **manual tip entry** and **automatic difference detection** (or equivalent modes).
- **Workforce exports:** Extend timesheet / working-plan style exports with a **Tips** column so owners can see per-employee tip totals over that month where data exists.
- Respect **multi-tenant** boundaries and existing payment flows; add tests for critical calculation and reporting paths where practical.

## Implementation summary (2026-03-31)

- **Tenant** `tip_entry_mode`: `preset` (default) or `overpayment`. **Settings → POS tip buttons** includes a select for this mode.
- **Overpayment mode:** Staff marks paid / finish with **amount charged** and **tip** (major units); tip defaults to `max(0, amount − subtotal)` when amount changes; API sends `tip_amount_cents` and optional `amount_paid_cents` on `PUT /orders/{id}/mark-paid` and `/finish`.
- **Preset mode:** Unchanged (percentage presets only); `tip_amount_cents` / `amount_paid_cents` rejected by API.
- **Order** `tip_attributed_user_id`: set on pay from table `assigned_waiter_id` or floor `default_waiter_id`; cleared on unmark-paid.
- **Reports:** `GET /reports/sales` summary includes `total_tips_cents`; daily rows include `tips_cents`; `by_waiter` includes `tips_cents`. CSV/Excel summary and waiter exports include tips columns.
- **Working plan Excel** (`GET /schedule/export`): footer row with **Tips (month total, cents)** for tips on paid orders attributed to that `user_id` in the calendar month.
- **Migration:** `20260331190000_tenant_tip_entry_mode_order_tip_attribution.sql`

## Testing instructions

1. **Migrate:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate` — schema version **20260331190000**.
2. **Preset mode (default):** Settings → set tip entry to preset; open Orders → mark paid on an unpaid order → percentage buttons still work; mark paid succeeds.
3. **Overpayment mode:** Settings → tip entry **Card/terminal amount (tip = difference)**; open mark paid → enter amount charged (e.g. subtotal 10.00, charge 11.50) → tip field should default to 1.50; adjust tip and confirm; order shows correct `tip_amount_cents`; unmark paid clears tip.
4. **Reporting:** Reports page shows **Tips (total)** card and waiter table **Tips** column; export CSV/Excel summary includes tips columns.
5. **Schedule export:** Working plan → export month Excel for a user; footer shows monthly tips total when applicable.
6. **Smoke:** `npm run test:landing-version`; confirm Angular build clean in `docker compose logs --tail=80 front`.
