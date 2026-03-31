# QR-based time tracking and shift management ("My Shift")

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/121

## Problem / goal

Implement a **shift management** module so staff can track work time at the venue using **QR-based clock-in/out**, with optional **location verification** (e.g. GPS) when scanning. Support **breaks**: paused shift state, resume by scanning the venue QR again. Provide **owner/manager manual override** when someone forgets to scan, for payroll and compliance. Deliver a simple **employee** view (status, time worked today, scan action) and an **admin** view (who is on-site, on break, or not clocked in).

Align with existing auth/roles, tenant model, and any HR or employee docs under `docs/` if present.

## High-level instructions for coder

- Model employees, shifts, breaks, and scan events with clear audit fields; respect tenant scoping and privacy rules for legal/identity data storage.
- Generate or configure **per-venue (or per-tenant) QR payloads** that authenticate clock-in/out and tie scans to timestamps (and optional geolocation when enabled).
- Implement **pause/resume** flow: entering break from "My Shift"; returning requires scanning the QR to resume the active shift timer.
- Build **admin manual entry/adjustment** for shifts with appropriate role checks and an audit trail.
- Ship **employee** and **admin** UIs as described; keep mobile-friendly tap targets for the scan entry point.
- Add tests or smoke coverage for critical paths if the repo pattern supports it.

## Implementation summary (coder)

- **DB:** `back/migrations/20260331180000_work_session_clock_qr_breaks.sql` — `tenant.clock_qr_token_hash`, `clock_qr_location_verify`; `work_session` break fields and related tables per models.
- **Backend:** `back/app/clock_qr_util.py` (HMAC; plain token only on regenerate); `work_session_serialization.py`; JSON body on clock endpoints uses **`clock_qr`**; `GET /users/me/clock-qr-status`; `POST /tenant/settings/clock-qr/regenerate`, `DELETE /tenant/settings/clock-qr`; `GET /reports/work-sessions/live`; **`POST /reports/work-sessions/{work_session_id}/adjust`** (REPORT_READ) for manual fixes with audit trail.
- **Front:** My Shift (`?clock_qr=`, breaks, net time); Settings → **Security** (clock QR card); Reports → **Who is on shift now**; `WorkSession` / API types aligned.

## Testing instructions

1. **Migrate:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate` (expect migration **`20260331180000_work_session_clock_qr_breaks.sql`** applied).
2. **Backend:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m pytest tests/test_work_session.py -q`
3. **Manual:** As owner/admin: Settings → **Security** → generate **Staff clock-in QR** (copy token once); optionally enable **Require GPS at venue for clock** with venue coordinates under Payment/location. As staff: open `/my-shift?clock_qr=<token>`; clock in, start/end break, clock out. Reports → **Who is on shift now** and historical attendance. Manual fix: **`POST /api/reports/work-sessions/{id}/adjust`** with JSON body `note`, optional `started_at` / `ended_at` (ISO UTC).
4. **Smoke:** `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`
