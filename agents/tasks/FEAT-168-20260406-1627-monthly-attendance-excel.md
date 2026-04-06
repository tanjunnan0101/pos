# Monthly attendance Excel — optional staff filter before download

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/168
- **168**

## Problem / goal
The POS system needs functionality to export monthly attendance records into an Excel format. This export must support an optional filtering mechanism based on staff members.

## High-level instructions for coder
- Implement the necessary API endpoint in the backend (back/app/) to gather and format the attendance data required for export.
- The endpoint must accept parameters for the required reporting month/year and an optional staff filter list/ID.
- The response must be structured to facilitate an Excel download (e.g., CSV format or an attachment that Excel can interpret easily).
- The feature should interface with the existing user/staff data models.

## Coder note (2026-04-06)
The Excel endpoint and Reports download were already on **`development`**. Optional **`staff_ids`** filter and UI are implemented under **`agents/tasks/UNTESTED-168-20260406-164452-monthly-attendance.md`** (GitHub **#168**). If this file is still **`feat`**, treat as duplicate scope: verify only or archive—do not re-implement the export.
