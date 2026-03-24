# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **every** user-visible part of the flow in the **selected** language—not mixed or English-only strings. The reporter wants the full form and related UI translated.

Relevant areas: `front/src/app/feedback-public/`, locale JSON under `front/public/i18n/`, and any API error messages surfaced on that route. See `docs/agent-loop.md` for optional GitHub closure / production sign-off after verification.

## High-level instructions for coder

- Reproduce on local Docker (`/feedback/{tenant}` with and without `?token=`) and compare with production URL pattern from the issue; exercise the language picker and supported locales.
- Ensure templates use translation for all guest-visible copy (including thank-you, validation, rate-limit, and invalid-tenant states); confirm document title tracks locale without flashing raw `FEEDBACK.*` keys.
- Align locale JSON files so no missing keys for strings used on this route.
- Run or extend `front/scripts/test-feedback-public-i18n.mjs` (or equivalent smoke) after changes; note evidence suitable for closing or updating the issue when product agrees.

## Coder notes (verification)

- Picked up as **WIP**; no additional product code changes were required: `feedback-public` already uses `TranslateModule` / keys under `FEEDBACK.*` and `BOOK.*`, document title uses `translate.stream()` with `takeUntilDestroyed` (issue #67 race).
- All seven locale files (`en`, `de`, `fr`, `es`, `ca`, `zh-CN`, `hi`) have the same **37** `FEEDBACK` keys as `en.json`.
- Backend `POST /public/tenants/{id}/guest-feedback` uses `_get_requested_language` + `get_message()` for localized `detail` (e.g. invalid reservation token).
- **Evidence:** `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs` — exit **0** (browser es auto-detect, locale switches, `?token=`, invalid token submit DE message, thank-you DE, `/feedback/0`, `/feedback/999999999`).

## Testing instructions

1. Stack up: `docker compose -f docker-compose.yml -f docker-compose.dev.yml ps` (HAProxy e.g. `127.0.0.1:4202`).
2. Run: `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs` (optional: `TENANT_ID=1`).
3. Manual spot-check: open `/feedback/1` and `/feedback/1?token=test`; switch language picker through **de / fr / es / ca / zh-CN / hi**; confirm no raw `FEEDBACK.` strings in UI or tab title; submit once with valid tenant (no token) and confirm thank-you + title.
4. If all pass, tester may move **UNTESTED → TESTING → CLOSED** per `agents/tasks/README.md` and update GitHub issue #67 if product agrees.
