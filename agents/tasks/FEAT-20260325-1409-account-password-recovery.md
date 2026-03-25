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
