# Split shift logic for "Add Shift" modal (Working Plan)

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/135

## Problem / goal

In **Working plan**, the **Add Shift** modal should support **split shifts** (two time blocks on the same day): optional split mode, a second start/end pair when enabled, validation that the second block starts after the first block ends, correct **total hours** for monthly/yearly views, and the **day timeline** showing **two separate blocks** for the same employee on that day (see issue for UI labels and bilingual checkbox text).

## High-level instructions for coder

- Add a **checkbox** below **Use any hour**, labeled **Split Shift? / ¿Turno partido?** (per issue).
- **Default:** one **Start time** / **End time** pair (first block). **When split is checked:** show a **second** start/end pair; use clear labels for block 1 vs block 2 (e.g. morning/evening or Shift A / Shift B as in the issue).
- **Validation:** second block **start** must be **strictly after** first block **end**; surface clear validation errors in the modal.
- **Totals:** monthly/yearly (and any related reports) must **sum both blocks** for duration.
- **Working Plan visualization:** same-day row shows **two distinct blocks** on the timeline for that shift day, not a single merged span.
