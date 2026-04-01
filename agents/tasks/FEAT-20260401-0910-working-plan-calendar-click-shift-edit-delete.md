# Working Plan calendar — click a shift line to edit or delete

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/136

## Problem / goal

Calendar view on the Working Plan page shows shift rows as read-only text. Users who stay in Calendar mode cannot adjust planned hours without switching to Week view. Enable click-to-edit (and optionally delete) on each real shift line using the same modal and API paths as Week view (`openEdit`, `confirmDelete` / `updateShift`, `deleteShift`).

Week view already exposes Edit/Delete per shift card; schedule CRUD exists under `/schedule` via `ApiService`. Calendar builds `shiftLines` with only `{ text, userId }` — no `shift.id`, so rows cannot open the correct shift.

## High-level instructions for coder

- When building `calendarGrid` / `shiftLines`, attach `shiftId` or the full `Shift` for each **real** shift line (not the “+N more” overflow row) so the template can call `openEdit(shift)` with the correct row.
- Make each real shift line interactive (button or clickable row with keyboard support and clear `aria-label`). Click opens the same Add/Edit modal as Week view. Optionally add a small Delete control or overflow menu reusing `confirmDelete(shift)`.
- For the overflow line (`CALENDAR_MORE_SHIFTS` when more than N lines): keep non-editable or handle explicitly (e.g. switch to Week / expand); do not invent fake `shiftId`s.
- Match Week view permissions: show edit/delete only for users who may write the schedule.
- Add i18n keys for any new strings and sync `front/public/i18n/*.json` for all shipped locales per project rules.
- Out of scope unless separately requested: split shifts, new APIs, or changes outside Working Plan calendar UX.
