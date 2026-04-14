# Floor plan: decouple payment state from table fill — bottom chip for payment; operational color shows service phase only

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/187
- **187**

## Problem / goal
When payment-pending is shown as a full-table background color, it overrides operational meaning (open order, ready to serve, seated, etc.). Staff need two channels: **service/kitchen phase** via fill color, and **payment/collection** via a small indicator.

- Table surface fill and legend should reflect **operational/service status only** (available, reserved, occupied/seated, open order, ready to serve, etc., per existing rules).
- A **small label/chip at the bottom** of each table shape (SVG) shows payment text: “Payment pending” when payment is pending or bill is requested; “Paid” when applicable; **hidden** when there is no relevant payment state.
- **Backend (`GET /tables/with-status`):** Avoid one `operational_status` that mixes payment with service phases if that currently drives fill. Either split fields (e.g. service-only operational status plus `payment_status`: none | pending | paid, derived from bill/order data) or keep one enum with **clear priority** so fill is service-first and payment only drives the chip. Return what the canvas needs in one response where practical.
- **Frontend (`tables-canvas` + types):** Extend canvas/API types with payment field(s); map fill/stroke/legend from **service-only** operational mapping; add SVG group for payment chip (readable on dark canvas; does not obscure table name). i18n keys e.g. `TABLES.PAYMENT_PENDING`, `TABLES.PAID` (all locales). Default: hide chip when none; if “paid” implies table released and no active order, “Paid” may not need to show — document chosen behavior in comments.
- **Edge cases:** Joined table groups — align with existing group merge rules for operational status. Accessibility: title or aria-label on chip.
- **Tests:** Backend unit tests for `/tables/with-status` combinations; manual checks for small/large shapes, long translations, zoom.

## Out of scope
Redesigning the entire legend palette unless required for contrast with the new chip.

## High-level instructions for coder
- Review issue body and floor-plan docs in `docs/` if present; align with tenant scoping on API changes.
- Implement backend response shape and priority rules so **fill = service pipeline**, **chip = payment**.
- Update Angular types, canvas rendering, and legend; add i18n for all supported locales.
- Add focused backend tests for `/tables/with-status` combinations; note manual verification steps in the task when ready for testing.

## Testing instructions

1. **Backend:** From repo root, `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back python3 -m pytest tests/test_tables_with_status_operational.py -q` (expect 5 passes).
2. **Frontend smoke:** With the stack up on port **4202**, `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` (includes navigation to `/tables`).
3. **Manual (floor canvas):** Open staff **Tables** → **Table view** / canvas. For a table with an active order and **bill requested** (`bill_requested_at`), confirm **fill** matches kitchen/service state (e.g. purple when order is **ready**) and a **bottom chip** shows payment pending (orange); not full-table orange. After **paid** while the table still links the paid order briefly, optional green **Paid** chip.
4. **i18n:** Spot-check **Payment (bottom chip)** legend and chip strings in another locale (e.g. DE).
5. **Zoom:** Pinch/zoom canvas; chip stays anchored to table bottom (SVG group transform).

---

## Agent handoff note

Renamed **WIP → UNTESTED** after verifying implementation (backend `payment_status` + service-first `operational_status`, `tables-canvas` payment chip, i18n). Regenerated `front/src/environments/commit-hash.ts` via `node front/scripts/get-commit-hash.js` so displayed semver matches `package.json` (addresses the prior landing smoke failure on criterion #2). GitHub issue **#187** labeled **`agent:untested`**. The **Test report** section below is from an earlier run; the tester should re-run **Testing instructions** items 1–5.

---

## Test report

**Date/time (UTC):** 2026-04-14 11:47:45 – ~11:52 UTC (log window below).

**Environment:** `docker-compose.yml` + `docker-compose.dev.yml`; `BASE_URL=http://127.0.0.1:4202`; branch `development` @ `4bf90f4`.

**What was tested:** Items 1–5 from **Testing instructions** above.

**Results:**

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Backend pytest `test_tables_with_status_operational.py` (5 tests) | **PASS** | `5 passed in 1.77s` |
| 2 | Frontend smoke `npm run test:landing-version` (as written, no env skip) | **FAIL** | App footer shows semver **2.0.74** while `front/package.json` is **2.0.75** — `front/src/environments/commit-hash.ts` exports `version = '2.0.74'`. Script error: `Landing semver "2.0.74" !== package.json "2.0.75"`. |
| 3 | Manual floor canvas (bill requested + fill vs chip) | **NOT VERIFIED** | No order with `bill_requested_at` prepared in this run; backend tests cover API split. Re-verify in UI after fixing item 2. |
| 4 | i18n DE (legend + chip strings) | **PASS** (spot-check) | `front/public/i18n/de.json`: `TABLES.PAYMENT_PENDING` / `TABLES.LEGEND_PAYMENT_PENDING` / `TABLES.PAID` present (e.g. “Zahlung ausstehend”, “Bezahlt”). |
| 5 | Zoom: chip anchored to table bottom | **NOT VERIFIED** | Not exercised in this automated run. |

**Supplementary (non-substitute):** With `SKIP_LANDING_PACKAGE_VERSION_CHECK=1`, the same Puppeteer script completed: login OK; **all sidebar routes including `/tables`** navigated OK.

**Overall:** **FAIL** — failed criterion **#2** (mandatory smoke command).

**Product owner feedback:** Backend coverage for `/tables/with-status` looks solid. The release checklist is blocked because the landing version check fails: the displayed app version must match `package.json` (update `commit-hash.ts` or align versioning when the committer bumps the front package). Full confirmation of the payment chip versus fill colors still needs a staff session with a bill-requested order and a quick zoom pass on the canvas.

**URLs tested (Puppeteer, with skip flag for supplementary run):**

1. `http://127.0.0.1:4202/`
2. `http://127.0.0.1:4202/dashboard`
3. `http://127.0.0.1:4202/my-shift`
4. `http://127.0.0.1:4202/staff/orders`
5. `http://127.0.0.1:4202/reservations`
6. `http://127.0.0.1:4202/guest-feedback`
7. `http://127.0.0.1:4202/tables`
8. `http://127.0.0.1:4202/kitchen`
9. `http://127.0.0.1:4202/bar`
10. `http://127.0.0.1:4202/customers`
11. `http://127.0.0.1:4202/products`
12. `http://127.0.0.1:4202/catalog`
13. `http://127.0.0.1:4202/reports`
14. `http://127.0.0.1:4202/working-plan`
15. `http://127.0.0.1:4202/users`
16. `http://127.0.0.1:4202/contracts`
17. `http://127.0.0.1:4202/settings`
18. `http://127.0.0.1:4202/inventory/items` (and other inventory sublinks as exercised by script)

**Relevant log excerpts**

- **Backend (pytest):** `..... [100%]` / `5 passed in 1.77s`
- **Frontend (strict smoke, fail):** `FAIL: Landing semver "2.0.74" !== package.json "2.0.75"`
- **Frontend (`pos-front`, ~11:45Z):** `Application bundle generation complete` (no compile errors in sampled window)
- **Backend (`pos-back`, ~5m window):** no errors in grep for `error|exception|traceback|500`
