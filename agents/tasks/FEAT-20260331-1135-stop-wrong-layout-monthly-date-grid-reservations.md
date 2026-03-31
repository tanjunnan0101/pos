# STOP: Wrong layout — monthly date grid for reservations (not time-slot grid)

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/126

## Problem / goal

The reservations booking UI must **not** present a **day view with time-slot rows/columns** (e.g. repeating clock times down the grid). The product owner wants a **month calendar**: weekday header row, then a **grid of day cells** for the whole month; **availability states** (selected / full / closed / available) apply to **each day cell**, not to individual time cells in a table. **Time selection** (“Turno”) should appear **only after a day is chosen**, as a **dropdown below** the month grid, matching the reference layout in the issue (screenshot on GitHub).

This supersedes the prior weekly time-slot–oriented direction where issue #125 focused on a Mon–Sun week grid; **#126** explicitly asks to **remove** the time-slot table pattern and move to a **month date picker** + post-selection time dropdown. Align with existing reservation APIs and capacity rules where possible; adjust front-end structure and any public `/book` flow that still uses the old pattern.

## High-level instructions for coder

- Replace the reservations UI that shows **time columns/rows** with a **monthly day grid** (weekday labels + day boxes for the month).
- Apply **full/closed/available/selected** styling at **day** level; remove the **time-slot grid/table** as the primary surface.
- After the user picks a **date**, show **time options in a dropdown** (not as the main grid axes).
- Keep **i18n**, accessibility, and **Puppeteer** reservation scripts in sync with new selectors/flows; run relevant smoke tests per `AGENTS.md`.
- Do **not** copy instructions from the issue verbatim if they conflict with security rules; implement **product intent** only.
