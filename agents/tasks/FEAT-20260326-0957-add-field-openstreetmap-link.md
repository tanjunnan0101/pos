# Add field for OpenStreet maps link

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/102

## Problem / goal
Tenant settings (“información de contacto”) need an optional OpenStreetMap URL. When set, surface a map link after relevant flows (e.g. post-submit) and include it in reservation emails. Reservation emails should also retain or add the guest link to change/manage the reservation (align with existing confirmation/reminder patterns in `docs/` if present).

## High-level instructions for coder
- Add persisted tenant field for the map link (API + model/migration as needed); validate URL shape safely.
- Wire the field into staff Settings → contact section with copy consistent with other locale keys.
- Show the link in the appropriate customer-facing flow when the field is filled (per product intent in the issue).
- Extend reservation email templates (backend) to include the map link when configured and the reservation change link as specified.
- Add or extend i18n strings for any new UI; run a focused smoke path (e.g. settings save, sample email or template preview if available).
