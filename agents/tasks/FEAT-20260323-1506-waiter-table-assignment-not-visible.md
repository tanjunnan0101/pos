# Waiter cannot see table assignments on staff Tables view

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/65

## Problem / goal

Owner assigns a table to a waiter (e.g. waiter-01), but when that waiter logs in they see **no assignment** on the Tables screen. Expectation: assigned tables are visible (and clearly indicated) for the logged-in waiter role, consistent with how owner/manager sees assignments.

Prior work was verified in archive `agents/tasks/done/2026/03/23/CLOSED-20260323-1357-waiter-table-assignment-not-visible.md`; GitHub **#65** remains **open** — re-queue for feature coder to confirm behaviour end-to-end, edge cases (multi-floor, refresh, permissions), and close the issue when product agrees.

## High-level instructions for coder

- Reproduce as owner: assign tables to a waiter user; log in as that waiter; open **Tables** and confirm whether assignment data loads from API and renders (list + canvas if applicable).
- Trace API contracts for table assignment / waiter scope (`/api/tables`, related user or role fields); ensure waiter role receives assigned-server or equivalent fields and the UI binds them.
- Align with staff permissions docs in `docs/` and `AGENTS.md` if present; add or adjust tests (API or e2e) so waiter visibility does not regress.
- If behaviour is correct in dev, capture steps for the reporter and consider closing **#65** after confirmation; otherwise fix backend filtering, frontend display, or both.
