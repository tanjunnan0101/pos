# Create a system to recover the password of the account

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/93

## Problem / goal
Users who forget their password need a **self-service recovery** path (request reset, verify identity via email or similar, set a new password) instead of admin-only workarounds. Scope should cover **staff/tenant** accounts as appropriate for this product; align with existing **auth**, **email/SMTP**, and **security** patterns in the repo (see `README.md`, `AGENTS.md`, and any auth-related notes under `docs/`).

## High-level instructions for coder
- Clarify which user types must be supported first (e.g. tenant owner/staff vs provider portal) and mirror the issue’s intent on GitHub if needed.
- Design **backend** endpoints and persistence (tokens, expiry, one-time use, rate limiting) consistent with FastAPI/SQLModel usage elsewhere; avoid leaking whether an email exists where that matters for security.
- Add **frontend** flows: “Forgot password” entry from login, email with link or code, and **set new password** UI with validation and i18n where login/register already use translations.
- Wire **email delivery** using the same SMTP/config path as other transactional mail; document any new env vars in `config.env.example` if required.
- Add tests (pytest for API; Puppeteer or existing patterns for critical UI path) and smoke the full flow locally (Docker stack).

## Coder notes (implementation summary)
- **Staff + provider:** Request body mirrors login disambiguation: optional `tenant_id`, optional `scope: "provider"`. Response is always `{ status, message }` (no email enumeration).
- **Backend:** Migration `20260325140000_password_reset_token.sql`, model `PasswordResetToken`, `POST /password-reset/request` (async, email via `send_password_reset_email`), `POST /password-reset/confirm`. Raw token emailed; SHA-256 hash stored; `token_version` incremented on success.
- **Frontend:** Routes `forgot-password`, `reset-password`, `provider/forgot-password` (reuse `ForgotPasswordComponent` with route `data.passwordResetScope`).
- **Email links:** `{PUBLIC_APP_BASE_URL}/reset-password?token=…` — **must set `PUBLIC_APP_BASE_URL`** in `config.env` for emails to contain a usable link.

---

## Testing instructions

### What to verify
- API accepts reset requests without revealing whether the email exists; confirm endpoint rejects invalid/expired/reused tokens; successful confirm changes password and invalidates existing sessions (`token_version`).
- UI: forgot-password and reset-password pages load, i18n keys resolve, staff login preserves `tenant` query on forgot link when present.
- SMTP: with global or tenant SMTP + `PUBLIC_APP_BASE_URL`, a real request sends an email with a working link (manual).

### How to test
- **Pytest (Docker):**  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back python3 -m pytest /app/tests/test_password_reset.py -v`
- **Apply migration (if needed):**  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back python -m app.migrate`
- **Frontend build:**  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no TS/Angular errors after changes.
- **Smoke:**  
  `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`
- **Manual E2E (optional):** Set `PUBLIC_APP_BASE_URL` (e.g. `http://127.0.0.1:4202`), configure SMTP, open `/login` → Forgot password → submit → use link from inbox → set new password → sign in.

### Pass/fail criteria
- **Pass:** All four tests in `test_password_reset.py` green; front log shows successful bundle generation; landing smoke test exits 0.
- **Fail:** Any pytest failure; Angular build errors in front log; broken routes or confirm accepting bad token.
