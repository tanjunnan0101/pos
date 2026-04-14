# Floor plan payment chip: anchor on bottom edge (half outside table shape); operational fill unchanged

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/188
- **188**

## Problem / goal
Service and kitchen state must stay visible via **table fill color** only; **payment** state is a separate **label/chip**, not an inner footer inside the fill. The chip must not crowd the centered name and seat count.

**Layout (visual spec):** For rect/circle/booth/bar shapes, the table body shows only operational color plus centered name and seat count (and existing top-right waiter initials if present). The payment chip (“Payment pending” / “Paid” per i18n) is **not** laid out as an inner footer inside the fill.

**Position:** Horizontally centered on the table; vertically the chip **straddles the bottom edge** of the table shape — roughly **half overlapping the bottom border** and **half extending below** (per product mockup). Use an SVG `g` + **transform** so the pill’s vertical center sits on the bottom edge (or slightly below) of the table bounds. Avoid collisions with adjacent tables at default zoom; tune font size and padding for small shapes.

**Separation of concerns:** Fill color follows **service-only** operational rules; payment drives **only** chip visibility and text. Backend should expose payment state separately from service `operational_status` (e.g. `payment_status`: none | pending | paid, or derive from existing fields) if not already done.

## High-level instructions for coder
- Read issue #188 and align with any floor-plan docs under `docs/`; preserve tenant scoping on API changes.
- **`tables-canvas`:** Implement the chip as a **sibling SVG group** after the table surface; position from known width/height of each shape; use transforms so the chip sits on the **bottom edge**, half outside the shape — name/capacity stay centered in the body without being pushed up by an inner chip.
- **Types/API:** Ensure frontend types match backend for operational vs payment fields; extend as needed.
- **i18n:** Use existing or add keys such as `TABLES.PAYMENT_PENDING`, `TABLES.PAID` across all locales.
- **Acceptance:** With payment pending, table fill reflects operational state; chip appears on the bottom edge straddling the shape, not inside the rectangle content area.
