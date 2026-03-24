# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URL (e.g. `/feedback/{tenant}` with optional `?token=…`) shows parts of the form or UI that are not translated for the selected language. Acceptance: every guest-visible part of the flow uses the active locale—no raw `FEEDBACK.*` keys in the DOM or document title. See `front/public/i18n/` and `FeedbackPublicComponent` (`front/src/app/feedback-public/`). Prior CLOSED archives under `agents/tasks/done/` document repeated dev/test passes; issue may stay open until product/production sign-off.

## High-level instructions for coder

- Reproduce on local Docker across supported locales (language picker and `Accept-Language`), with and without a valid reservation token.
- Confirm templates, dynamic strings, API error paths, and document title stay localized; fix any missing keys or pipe/`TranslateService` usage gaps.
- Align all locale JSON files under `front/public/i18n/` for `FEEDBACK` (and related keys) where needed.
- Run or extend feedback-public i18n smoke / Puppeteer coverage if present; document evidence for GitHub when dev matches acceptance.
- Optional: spot-check production (`https://satisfecho.de`) per `docs/agent-loop.md`; support closing **#67** when product agrees.

## Coder notes (2026-03-24)

- **`front/public/i18n/fr.json`:** The `FEEDBACK` block had been **invalid JSON** (missing comma after `RATE_LIMIT`, then a duplicate key block). That prevents the locale from loading and surfaces raw `FEEDBACK.*` in the UI for French. Corrected to one `FEEDBACK` object matching the `en.json` key set and order (working tree now matches valid `development` content).
- **Other locales:** `de`, `es`, `ca`, `zh-CN`, `hi` already had complete `FEEDBACK` keys; validated with `python3 -m json.tool` on all `front/public/i18n/*.json`.
- **Component/API:** No code changes; `FeedbackPublicComponent` already uses the translate pipe / `stream()` for the document title; API errors use `Accept-Language` via the existing interceptor for localized `detail` where the backend returns `get_message(...)`.

## Testing instructions

- **What to verify:** Public `/feedback/:tenantId` (with and without `?token=…`) shows no raw `FEEDBACK.*` strings in the DOM or tab title for **en, de, fr, es, ca, zh-CN, hi**; form submit reaches thank-you with localized copy; `/feedback/0` shows localized error.
- **How to test:** Stack up with `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (HAProxy e.g. `http://127.0.0.1:4202`). Run:
  - `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`
  - Optional: `python3 -m json.tool front/public/i18n/fr.json` (and other locales) — must exit 0.
  - After front edits: `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no Angular/TS build errors.
- **Pass/fail:** Puppeteer script exits 0 and prints all `>>> RESULT: … OK` lines; French locale shows human-readable French strings, not keys.
