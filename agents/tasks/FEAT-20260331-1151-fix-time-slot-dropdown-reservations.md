# Fix the Time Slot Dropdown immediately with this logic (Reservations)

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/127

## Problem / goal

In the reservations flow, the time slot control (Turno) does not respect “now” when the user has **today** selected: past slots still appear (e.g. around 13:43 local time, **12:00** still shows as the first option). For a real-time booking experience, **today’s** list must only offer slots from the current time onward, aligned with the tenant’s slot step (e.g. next boundary after the current time such as **14:00** or **14:15**). See existing reservation / public book docs under `docs/` if they define slot rules or APIs.

## High-level instructions for coder

- Trace where reservation and public book UIs build the time-slot options for the selected calendar day (staff reservations vs `/book` if both share logic).
- When the selected date is **today** (in the relevant timezone / tenant context already used elsewhere), **filter out** any slot whose end time is before “now” (or strictly before the next valid slot per product rules—match what the issue describes: no options before the first still-bookable slot).
- Ensure the **first visible option** is the next available slot after the current time, not a fixed morning time.
- Add or extend automated coverage if there is an existing pattern (unit or e2e); otherwise document manual checks: pick today at a time after midday and confirm the dropdown starts at the expected next slot only.
- After front changes, confirm `ng serve` / Docker `pos-front` logs show a clean bundle build.
