# My shift

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/87

## Problem / goal

Staff use **My shift** / **Start shift** to clock in. The product should **detect when an open shift exceeds a normal contract length (8 hours)** and **alert the worker** so overtime is visible. Contracts are typically 8 hours; behaviour should be investigated and designed (what counts as “exceeded”, timezone, whether only UI vs persisted flags, owner configuration, etc.). See existing **`WorkSession`** / **`/my-shift`** flow and any reports that consume work sessions (`docs/` if present).

## High-level instructions for coder

- Review current **work session** model and UI (`/my-shift`, dashboard card if applicable): how start/end and duration are computed.
- Define product rules for the **8-hour threshold** (fixed default vs tenant setting; use tenant timezone for display; edge cases: overnight, manual corrections).
- Implement **user-visible alert** when an active session passes the threshold (e.g. banner, dialog, or inline on My shift) without breaking clock-in/out APIs.
- Consider whether **owners/admins** need reporting or visibility; keep scope aligned with the issue unless docs say otherwise.
- Add or extend tests (API and/or UI smoke) so the alert path is covered where practical.

## Coder notes (2026-03-25 UTC)

- **Rule:** Open shift “over contract” when elapsed wall time from `started_at` to **now (UTC)** is **≥ 480 minutes** (8 hours). Same for overnight shifts (continuous elapsed time). No DB migration; threshold is a shared constant `WORK_SESSION_CONTRACT_THRESHOLD_MINUTES` in `back/app/work_session_serialization.py` (future: could read from tenant settings).
- **API:** Every serialized `WorkSession` includes `open_duration_minutes` (null when ended), `contract_threshold_minutes`, `over_contract` (open sessions only). Used by `GET /users/me/work-session`, `POST …/start|end`, `GET /users/me/work-sessions`, and `GET /reports/work-sessions`.
- **UI:** My shift shows a warning banner + elapsed row while clocked in; dashboard “My shift” card shows a short overtime line when applicable. Client recomputes threshold crossing from `started_at` + `contract_threshold_minutes` on a timer so the banner appears without manual refresh.
- **Display times** on My shift remain `toLocaleString()` (browser locale); duration threshold is not calendar-day-based.

## Testing instructions

### What to verify

- Open work session responses include `contract_threshold_minutes`, `open_duration_minutes`, and `over_contract` consistent with elapsed time.
- After **≥ 8 hours** clocked in, **My shift** shows the overtime banner (`data-testid="my-shift-overtime-banner"`) and dashboard shows the overtime hint on the My shift card when the user is still past threshold (`data-testid="dashboard-my-shift-overtime"`).
- Clock-in/out still works; closed sessions list/report responses remain valid JSON with the new fields.

### How to test

- **Backend:** With Docker dev stack:  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back python3 -m pytest tests/test_work_session.py -q`
- **Frontend build:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no TS/Angular errors after rebuild.
- **Smoke:** From `front/`: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` (navigates `/my-shift`).
- **Manual UI:** Log in as staff, open **My shift**, start shift; to simulate overtime without waiting, temporarily move `started_at` in DB to \>8h ago (or rely on API test), reload **My shift** — banner should appear; end shift — banner gone.

### Pass/fail criteria

- **Pass:** All three pytest cases in `test_work_session.py` green; front build clean; landing smoke exits 0; overtime banner visible when open session age ≥ threshold.
- **Fail:** Any pytest failure, Angular build error in front logs, or banner missing when session is clearly over 8 hours open.
