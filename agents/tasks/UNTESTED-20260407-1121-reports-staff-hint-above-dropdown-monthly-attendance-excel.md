# Reports: staff hint above dropdown — Monthly attendance (Excel) layout

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/171

## Problem / goal
In Reports, the **Monthly attendance (Excel)** / **Asistencia mensual (Excel)** block shows the help text **below** the staff selector. The intended reading order is: optional section label → **hint** → staff control → download actions (or keep button alignment per existing design). Do **not** change i18n copy—only template structure and CSS/layout so the hint appears **above** the dropdown (including fixing flex/order if a horizontal toolbar currently inverts visual order).

## High-level instructions for coder
- Locate the component template for the Monthly attendance (Excel) section (likely `ReportsComponent` or a child template for that block).
- Move the hint element (`<p>` or equivalent) **before** the staff `<select>` / custom multi-select in the DOM.
- If the block uses a horizontal flex toolbar, stack the staff column vertically (`flex-direction: column`) with hint first, control second, so flex does not push the hint under the control.
- Remove or adjust `order`, `flex-wrap`, or `align-items` rules that visually invert hint vs control.
- Do not change translation strings; only structure and CSS.
- After edits, confirm `docker compose … logs front` shows a successful Angular build (no standing template/type errors).

## Implementation summary
- **`front/src/app/reports/reports.component.html`:** Moved `<p class="muted attendance-excel-staff-hint">` (staff filter hint) to sit **after** the staff section label and **before** `.attendance-excel-staff-dropdown` so DOM order is label → hint → trigger/panel. Existing `.attendance-excel-staff { flex-direction: column }` in SCSS already stacks children; no i18n or copy changes.

## Testing instructions
1. **Build:** From `front/`, `npm run build` — expect success (no template/TS errors).
2. **Smoke (optional):** With stack up on HAProxy (e.g. `http://127.0.0.1:4202`), `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` — navigates `/reports` among other routes.
3. **Manual UI:** Log in as a user with **`report:read`** and open **Reports**. In **Monthly attendance (Excel)** (`data-testid="reports-attendance-excel"`), when staff users exist, confirm the muted **staff filter hint** paragraph appears **above** the staff dropdown trigger (not below it). Month picker and download buttons unchanged.
