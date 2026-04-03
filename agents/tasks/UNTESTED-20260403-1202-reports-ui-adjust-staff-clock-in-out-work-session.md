# Reports UI: adjust staff clock-in/out (work session)

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/159

## Problem / goal
Staff with **report:read** need an **Adjust** action on **Reports** to correct a work session’s clock-in/out times and add a note. The flow should open a modal (**datetime-local** for start and end, plus note), call **`postReportWorkSessionAdjust(sessionId, { note, started_at, ended_at })`** with **ISO UTC** derived from the local inputs, reload attendance tables on success, and surface API errors via **`ApiErrorMessageService`**. Remove the duplicate **“Who is on shift now”** block from **`reports.component.html`**. Add **`REPORTS.*`** i18n keys in **all** **`front/public/i18n/*.json`** files.

## High-level instructions for coder
- Add an **Adjust** entry point in the Reports UI gated by **`report:read`** (and any existing permission patterns for report actions).
- Implement a modal: **start**, **end** (**datetime-local**), **note**; map local values to **UTC ISO** strings for the API payload.
- Wire **`postReportWorkSessionAdjust`** (or the existing reports API client) and on success refresh the attendance / work-session tables the page already uses.
- Use **`ApiErrorMessageService`** for failed requests (consistent with other report screens).
- Deduplicate **“Who is on shift now”** in **`reports.component.html`** so it appears once (or as intended by design).
- Add **`REPORTS.*`** translation keys across **every** locale file under **`front/public/i18n/`**; follow **`.cursor/rules/angular-ngx-translate.mdc`** if applicable.
- Smoke: exercise Reports with a user that has **report:read**, open Adjust, submit valid and invalid ranges, confirm reload and error display.

## Implementation notes (coder)

- **Adjust** on **Who is on shift now** and **Staff attendance** tables (`report:read` via existing `canViewAttendance()`). Modal: `datetime-local` → `toISOString()` for `POST /reports/work-sessions/{id}/adjust`; empty clock-out omits `ended_at` (open shifts). Client validates end ≥ start; API errors via **`ApiErrorMessageService`** in-modal. Duplicate live section removed. **`es.json`:** added missing **`WORK_SESSIONS_LIVE_*`** / status keys so Reports live block matches other locales.

## Testing instructions

1. Log in as a user with **`report:read`** (e.g. owner/admin). Open **`/reports`**.
2. Confirm **“Who is on shift now”** appears **once** (not duplicated).
3. If **Staff attendance** or live table has rows: click **Adjust**, confirm modal shows staff name, start/end (**datetime-local**), note.
4. Set clock-out **before** clock-in → expect inline **`REPORTS.WORK_SESSION_ADJUST_INVALID_RANGE`** (or related validation message).
5. Submit a **valid** adjustment (optional note) → modal closes; tables reload (times updated). If the API returns an error (e.g. 400), expect message from **`ApiErrorMessageService`** in the modal.
6. **i18n:** spot-check another language; new keys are under **`REPORTS.WORK_SESSION_ADJUST_*`** (and **`WORK_SESSION_ADJUST_COL_ACTIONS`**).
7. **Automated:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (includes navigating to `/reports`). With credentials: `BASE_URL=… LOGIN_EMAIL=… LOGIN_PASSWORD=… npm run test:reports --prefix front`.
