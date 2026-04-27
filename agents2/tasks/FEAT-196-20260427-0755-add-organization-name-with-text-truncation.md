# Add Organization Name with Text Truncation

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/196
- **196**

## Problem / goal
Show the organization name next to the POS brand in the sidebar logo area (e.g. `POS (Organization Name)`). Long names must not wrap or overlap adjacent UI; truncate with ellipsis within the sidebar layout.

## High-level instructions for coder
- Locate the sidebar / shell branding markup where the logo text is rendered and include the tenant or organization display name as specified in the issue (parenthetical style).
- Apply CSS on the `.logo` (or equivalent) class so long labels stay on one line and truncate with ellipsis: `white-space: nowrap`, `overflow: hidden`, `text-overflow: ellipsis`, and a constrained width (`max-width` tuned to the sidebar — issue suggests ~150px as a starting point).
- Prefer existing tenant/org fields and i18n patterns used elsewhere for staff UI; avoid hard-coded placeholder strings in production templates.
- Verify at narrow sidebar widths and with a very long organization name that layout remains stable and readable.
