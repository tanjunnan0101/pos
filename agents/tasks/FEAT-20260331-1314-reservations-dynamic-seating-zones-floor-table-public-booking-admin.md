# Reservations: dynamic seating zones from Floor/Table data (public booking + admin)

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/129

## Problem / goal

Public booking should follow the real floor layout: only offer seating zones that exist, have reservable tables, and are active; use owner-defined zone names; hide the location control when a single zone applies; support inactive zones (for example a closed terrace). Today, floors and `Table.floor_id` exist for staff layout, but public `/book` has no zone field, reservations do not carry floor preference, and slot capacity uses all tenant tables without floor filtering.

## High-level instructions for coder

- Add a tenant-scoped public API that lists bookable zones (reuse or extend `Floor` / equivalent): each zone has at least one reservable table, respect sort order, exclude inactive zones and zones with no tables.
- Extend admin/owner UI so zones can be created, renamed, reordered, and marked active/inactive (build on existing floor management if present).
- Public booking UI: show a location/zone selector only when there are two or more active bookable zones; otherwise omit it and define whether capacity is that zone only or unchanged global behavior per product decision.
- When a zone is selected, availability and `createReservationPublic` must count only tables on that floor; document and implement behavior for `floor_id` null tables.
- Optionally persist `preferred_floor_id` (or equivalent) on `Reservation` for staff visibility.
- Preserve tenant isolation on all new/changed endpoints; align with existing capacity rules (walk-in reserved tables, turn times, etc.).
- Add migrations and i18n for new strings; extend smoke/Puppeteer for `/book/:tenantId` if the flow changes.
