# Fix UI clipping and z-index overlap on status dropdown

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/179
- **179**

## Problem / goal
In **Orders**, the per-order **status** dropdown (`.status-dropdown` in the orders UI) is visually wrong: options can sit **under** the next card’s badges (e.g. “Pendiente”) or be **clipped** by a parent, so actions like “Retroceder”, “Avanzar”, “Listo” are hard to see or use. The report suggests a **stacking context** problem and/or **`overflow: hidden`** on an ancestor, despite a high z-index on the dropdown.

## High-level instructions for coder
- Inspect **orders** view markup/CSS for `.status-dropdown` and its ancestors (overflow, transform, isolation, stacking).
- Fix layering so the open menu reliably appears **above** adjacent cards and is not clipped; prefer minimal CSS/HTML changes aligned with existing patterns (e.g. portal/overlay, raising stacking context when open, or adjusting `overflow` only where safe).
- Manually verify on a busy Orders list: open the status menu on several rows and confirm all options are visible and clickable.
- If relevant, note any follow-up for docs or i18n; keep scope to this visual bug.
