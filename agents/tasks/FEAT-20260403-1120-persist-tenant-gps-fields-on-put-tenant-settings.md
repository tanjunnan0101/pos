# Persist tenant GPS fields on PUT /tenant/settings

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/158

## Problem / goal
Owner settings for venue location (latitude, longitude, radius, location check toggle) are not persisted on `PUT /tenant/settings`: `update_tenant_settings` in `back/app/main.py` effectively saves only `clock_qr_location_verify` (and related fields), so `Tenant` GPS columns stay NULL. Staff clock flows that require GPS then fail with a message like venue coordinates must be set. The fix should apply `TenantUpdate` fields `latitude`, `longitude`, `location_radius_meters`, and `location_check_enabled` using the same optional-field pattern as other settings (update only when present; validate latitude/longitude ranges and non-negative radius). See `AGENTS.md` / work-session docs for clock-in GPS behavior.

## High-level instructions for coder
- Inspect `update_tenant_settings` (and `TenantUpdate` / `Tenant` models) and extend persistence so GPS-related fields from the request are written to the tenant row when provided.
- Validate inputs: sensible lat/lon bounds, non-negative radius; reject or 422 invalid combinations per existing API style.
- Add or extend tests (e.g. `tests/test_work_session.py` or tenant settings tests): a settings update persists coordinates; with `clock_qr_location_verify` and coords set, clock-in path that needs venue GPS succeeds (or equivalent API-level assertion).
- Run targeted pytest and any relevant smoke path; do not log secrets or full env in commits.
