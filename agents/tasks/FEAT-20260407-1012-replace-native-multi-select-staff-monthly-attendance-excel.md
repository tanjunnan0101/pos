# Replace native HTML multi-select for Staff (optional) on Monthly attendance (Excel) export

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/169

## Problem / goal
The Monthly attendance Excel export screen uses a visible native `<select multiple>` listbox for optional staff filtering. It uses a lot of vertical space and feels inconsistent with a compact month picker plus download button.

Replace it with a **single-line, collapsible** control that opens a panel on click/focus. When closed, it must clearly show selection state (e.g. “All staff” / “Everyone” / “N selected” or chips with names). Behavior must match today: **empty selection** = everyone with attendance that month; **specific users** = filter to those only.

## High-level instructions for coder
- **Stack:** This repo’s frontend is **Angular** (not React/Vue); use existing shared UI patterns and components where possible; if the issue text mentions other frameworks, follow the Angular codebase instead.
- Implement a compact **dropdown-style multi-select** (or combobox pattern) with scrollable list, checkboxes or toggle rows; optional search if low effort and staff lists can grow.
- **Accessibility:** keyboard open/close, focus management, Space/Enter to toggle, proper `aria-*` and association with the “Staff (optional)” label.
- **API / form:** Preserve the same field names and values as the current multi-select so the export request and backend contract stay unchanged.
- **Visual:** Align with the surrounding form (month input, Download Excel): spacing, typography, border radius.
- **Copy:** Keep or shorten the helper hint; do not rely on “Ctrl/Cmd to select multiple” (native multi-select only).
- **Done:** No tall native listbox; compact control; exports still work filtered and unfiltered.
