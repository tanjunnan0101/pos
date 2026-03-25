# Working plan

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/88

## Problem / goal

The **working plan** flow (**Workin plan > new shift**) should be **more flexible**: allow assigning the **same schedule to an employee for an entire month** at once (schedules often stay constant), while still supporting **per-day overrides** for shift rotations and exceptions.

## High-level instructions for coder

- Map the current **working plan / shift** UI and APIs (tenant staff scheduling, “new shift”, calendar views).
- Design UX for **bulk month assignment** (select employee, month, default pattern) vs **single-day edit** without blocking exceptions.
- Ensure data model and validation support recurring or copied patterns plus day-level diffs (avoid silent data loss when editing one day vs the month).
- Add tests or smoke coverage for the bulk-assign and override paths if the stack already has patterns for this area.

## Coder notes (implementation)

- **Model:** `ShiftBulkCreate` in `back/app/models.py` — `weekdays` uses **JavaScript `Date.getDay()`**: 0=Sunday … 6=Saturday (documented on the model).
- **API:** `POST /schedule/bulk` in `back/app/main.py` (after `POST /schedule`). Requires `SCHEDULE_WRITE`. Validates target user like single-shift create. **`skip_days_with_existing_shift`** (default true) skips any calendar day where that user already has ≥1 shift so bulk apply does not overwrite exceptions; set false to add another shift on those days too.
- **Frontend:** `working-plan.component.ts` — **Apply to month** (`data-testid="working-plan-bulk-month"`), modal with staff, weekday checkboxes (default Mon–Fri), times, optional label, skip-existing checkbox. Target month = same rules as Excel export (`exportYearMonth()`).
- **Client:** `ApiService.bulkCreateShifts`.
- **Tests:** `back/tests/test_schedule_bulk.py`; `front/scripts/test-working-plan.mjs` asserts bulk button.

---

## Testing instructions

### What to verify

- **Apply to month** opens a modal scoped to the visible month (calendar = that month; week = month of Monday of displayed week).
- Mon–Fri bulk for a month creates one shift per selected weekday; toast shows created and skipped counts.
- With **skip** on, running bulk again creates 0 new rows and skips all matching days; per-day edits (different times on one day) stay if that day was skipped on first run or if user edited after bulk.
- API rejects `user_id` outside tenant; Angular build clean.

### How to test

1. **Backend (Docker):** from repo root, stack up:
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back python3 -m pytest tests/test_schedule_bulk.py -q`
2. **Frontend smoke:** `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:working-plan` (needs schedule-capable login).
3. **Manual:** Working plan → **Apply to month** → pick staff, weekdays, times → Apply; switch to calendar and confirm rows; run bulk again with skip on → 0 new shifts; toggle skip off on a day that already has a shift → second shift appears that day.

### Pass / fail criteria

- **Pass:** All three `test_schedule_bulk` tests pass; Puppeteer working-plan test passes; manual flow matches expectations; no TS/build errors in `docker compose … logs front`.
- **Fail:** 403/400 on valid tenant worker, wrong shift count for obvious Mon–Fri month, missing bulk control, or silent overwrite of existing per-day shifts when skip is enabled.
