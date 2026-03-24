# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public feedback URLs (e.g. `/feedback/{tenant}` with token) must show **every** part of the form in the user’s selected language. The reporter saw untranslated strings on production-style URLs.

Prior implementation and multiple **CLOSED** archives under `agents/tasks/done/` document i18n work and tester **PASS** for this scope; **#67** may still need **final QA on production**, any **remaining gaps**, and **GitHub alignment** (comment / labels / close when product accepts). See `docs/agent-loop.md`.

## High-level instructions for coder

- Re-verify `/feedback/{tenant}` (with and without token) across locales using the shared language picker; confirm invalid-tenant and loading paths stay localized.
- If anything is still English or missing keys, extend `front/public/i18n/*` and templates; keep JSON valid (syntax errors block whole locales).
- Run documented smoke / Puppeteer for feedback or landing if available; check `docker compose` **front** logs for build errors after edits.
- When behaviour matches the issue: coordinate **close #67** on GitHub (or note handoff if automation lacks Issues write).

## Coder implementation notes (2026-03-24)

- **API language:** `_get_requested_language` now reads the real **`Accept-Language`** header (still supports `?lang=` and legacy `?accept-language=` query). The Angular app adds **`Accept-Language`** on all requests to `environment.apiUrl` via `acceptLanguageInterceptor` (runs before `authInterceptor`).
- **Guest feedback errors:** `invalid_email`, `invalid_phone`, and `invalid_reservation_token` were only defined for English in `back/app/messages.py`, so validation errors always appeared in English for `es`/`de`/etc. Those keys are now translated for **es, ca, de, zh-CN, hi**; a full **`fr`** message map was added so French UI matches API messages. Public guest-feedback **404** uses `get_message("tenant_not_found", lang)` instead of a hardcoded English string.
- **Loading state:** Public feedback loading shell shows **`FEEDBACK.LOADING`** (localized) above the skeleton.
- **Auth interceptor:** `/feedback/` is treated as a public route (same idea as `/book/`) so stray **401** responses do not trigger login redirect on the public form.

## Testing instructions

1. **Backend:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back pytest tests/test_guest_feedback.py -q` — expect **5 passed** (includes `Accept-Language: de` check on invalid reservation token).
2. **Frontend build:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no TS/Angular errors after rebuild.
3. **Smoke:** From `front/`, `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`.
4. **Manual `/feedback/1`:** Open the language picker, choose **Deutsch** (or **Français**), enter an invalid optional email (e.g. `x`) and submit — the inline error from the API should be in that language, not English. Repeat with **invalid tenant** (`/feedback/0`) and confirm UI strings stay translated. Loading state should show the localized loading line briefly.
5. **GitHub #67:** After tester pass, comment / close per product acceptance.
