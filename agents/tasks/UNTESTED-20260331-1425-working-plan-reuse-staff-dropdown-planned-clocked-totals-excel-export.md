# Working plan: reuse staff dropdown for collapsible “Planned vs clocked” + totals; optional Excel export

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/130

## Problem / goal

On the Working plan screen, improve how owners see **planned** (scheduled shifts) vs **clocked** (attendance / net time by UTC day from clock-in), tied to the **existing staff/user dropdown**—no duplicate employee selector unless an explicit “All staff” aggregate mode is required. Keep the page light: wrap the planned-vs-clocked block in a **collapsible/disclosure** (default **collapsed**, e.g. “Show planned vs clocked”; optional persistence of open state). Show **totals** (planned hours, clocked hours, variance—positive when clocked exceeds planned) for quick scanning. Optionally add **Export to Excel** aligned with other reports (columns match visible data or a documented superset). Permissions unchanged; **i18n** for new UI strings. Align date boundaries and timezone display with existing attendance APIs and tenant expectations.

## High-level instructions for coder

- Reuse the Working plan **existing user/staff dropdown** as the single source of selection for planned-vs-clocked metrics for the current page context (date range / week as the screen already defines).
- Implement a **collapsible section** (default collapsed) for the planned-vs-clocked UI; expand/collapse must work reliably.
- Surface **summary totals** for the selected period/worker (and include them in export if Excel is implemented).
- If adding Excel export, follow patterns used elsewhere in the app for exports and column naming.
- Add/update translations for any new user-visible strings.
- Confirm behaviour with existing backend contracts for working plan and attendance; do not weaken authorization.

## Implementation summary (coder)

- **Staff dropdown** (`working-plan-staff-scope`): first option **All staff** (default); single control filters the planned-vs-clocked table and gates **Export Excel** (shifts) to a selected person only.
- **Planned vs clocked**: collapsible block (button **Show/Hide planned vs clocked**), default collapsed; open state in `localStorage` key `workingPlanPvaOpen`.
- **Table**: footer **Totals** for planned, clocked, variance over visible rows; empty state when a single staff is selected but has no rows in range.
- **Backend**: `GET /schedule/planned-vs-actual/export` — Excel with date, staff, planned, clocked, variance + totals row; optional `user_id`; `SCHEDULE_READ` + tenant checks; shared data builder `_schedule_planned_vs_actual_row_dicts`.
- **i18n**: all `front/public/i18n/*.json`; backend column labels in `back/app/schedule_export_i18n.py` (`planned_vs_export_labels`).

## Follow-up fix (coder, 2026-03-31)

- **PVA section visibility:** `exportUserId` is now an Angular **`signal`** (`exportUserId = signal<number | null>(null)`). `showPvaSection` and `plannedVsActualDisplayed` are `computed()`s that read `exportUserId()` so the planned-vs-clocked block appears as soon as a specific staff member is selected (previously a plain field was not tracked by `computed()`).
- **Staff select:** `[ngModel]="exportUserId()"` + `onExportUserIdSelected($event)` sets the signal and calls `fetchPlannedVsActual()`.
- **Tests:** `back/tests/test_schedule_export.py` expectations updated for `/schedule/export` workbook shape: header + shift rows + blank row + **Tips (month total)** summary row (`max_row` 4 with one shift, 3 for empty month).

## Testing instructions

1. **Stack**: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (or `./run.sh`); app on HAProxy port (e.g. `http://127.0.0.1:4202`).
2. **Smoke**: `BASE_URL=http://127.0.0.1:4202 npm run test:working-plan --prefix front` (needs staff login with schedule access).
3. **Manual — staff scope**: Open **Working plan**. Confirm dropdown label **Staff**, options **All staff** + named users. With **All staff**, shift **Export Excel** is disabled; planned-vs-clocked section appears when there is any planned/clocked data in the visible range (or when a specific staff is selected).
4. **Manual — disclosure**: Section starts **collapsed**; expand shows hint, **Export comparison (Excel)** (disabled if no data rows), and table with **Totals** row. Collapse/expand; reload page and confirm open state persists if you had left it open.
5. **Manual — filter**: Select one staff member; table shows only that user’s rows; totals match sum of visible rows; empty message if none.
6. **Manual — exports**: With a staff member selected, **Export Excel** downloads shift month file as before. With at least one comparison row, **Export comparison (Excel)** downloads `planned-vs-clocked-<from>-to-<to>.xlsx` with headers + totals; try with **All staff** and with one user filtered.
7. **Backend**: Optional `curl` with Bearer token: `GET /schedule/planned-vs-actual/export?from_date=...&to_date=...` and with `&user_id=<id>`; expect 400 for wrong tenant user id.
8. **i18n**: Switch UI language; verify new strings (staff hint, show/hide, export comparison, empty filtered).

### Pass / fail (coder self-check, 2026-03-31)

- **What to verify:** PVA block appears when a specific staff member is selected even if there are zero comparison rows in range; `/schedule/export` XLSX includes tips footer rows; Angular build clean.
- **How tested:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` (no errors after rebuild); `BASE_URL=http://127.0.0.1:4202 npm run test:working-plan --prefix front`; `docker compose … exec back python3 -m pytest tests/test_schedule_export.py -q` (5 passed).
- **Pass criteria:** Working-plan smoke exits 0; schedule export tests pass; front logs show successful bundle generation.
