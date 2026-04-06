# Monthly attendance Excel — optional staff filter before download

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/168
- **168**

## Problem / goal
The goal is to allow users to download the monthly attendance Excel file while optionally filtering by specific staff members.

## High-level instructions for coder
- Implement the optional staff filter functionality on the attendance download endpoint.
- Ensure the filtering logic works correctly when provided staff IDs.
- The downloaded file must still be an Excel format suitable for direct viewing in Excel.

## Implementation summary
- **Backend** (`back/app/attendance_routes.py`): Optional repeated query parameter `staff_ids` on `GET /reports/attendance-excel`. Omitted = all staff with sessions in the month. Each ID must be a user in the current tenant; duplicates are accepted; empty list when the parameter is used returns 400.
- **Frontend** (`reports` + `api.service`): Multi-select of tenant users next to the month picker; no selection = export everyone (no `staff_ids` sent). XLSX download unchanged.

## Feature-coder verification (2026-04-06)
Duplicate **FEAT-168-20260406-1627-monthly-attendance-excel.md** was removed; scope was already implemented on `development`. Confirmed: `attendance_routes` is mounted in `main.py` under `/reports`; optional `staff_ids` query matches issue **#168**. Quick checks: `tests/test_work_session.py` (9 passed); `curl` to HAProxy `http://127.0.0.1:4202/` returned 200.

## Testing instructions
1. Log in as a user with `report:read` on a tenant that has multiple users and at least some work sessions in a chosen month.
2. Open **Reports** → **Monthly attendance (Excel)**.
3. Pick a month that has attendance data. Leave **Staff** unselected → **Download Excel** → confirm file opens and includes all staff who had sessions that month.
4. Select one staff member only → download again → spreadsheet must only contain rows for that user (employee name/number columns only on that user’s block).
5. Select two staff members → download → both appear; others must not.
6. **API (optional):** With a valid bearer token, `GET /reports/attendance-excel?year=YYYY&month=M&staff_ids=<id>` (repeat `staff_ids` for multiple) returns `200` and `Content-Type` suitable for XLSX; invalid tenant user id → `400` with detail about invalid staff IDs; wrong month with filter but no matching sessions → `404`.
