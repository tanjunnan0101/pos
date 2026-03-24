# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **no untranslated UI**: every part of the form and related states should follow the selected language. Prior **CLOSED** archives under `agents/tasks/done/` document repeated dev/test **PASS**; the issue may stay open until optional production verification and product sign-off. See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (language picker and `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If dev already matches acceptance, capture evidence for GitHub; optional production spot-check on **satisfecho.de**; support a short verification comment and closing **#67** when product agrees.
- If gaps remain, extend `front/public/i18n/*.json` and `feedback-public` templates so all guest-visible strings and titles stay localized.

## Coder (feature) — 2026-03-24

- **FEAT → WIP** on pickup. Reviewed `FeedbackPublicComponent` (`front/src/app/feedback-public/`): guest copy uses the `translate` pipe; document title uses `translate.get` with `onLangChange` / `onTranslationChange` so raw `FEEDBACK.*` does not linger in the tab (issue #67).
- **Locale parity:** `FEEDBACK` keys in `front/public/i18n/en.json` match the other locale files (de, es, fr, ca, zh-CN, hi); `BOOK.ADDRESS` / `BOOK.OPEN_IN_GOOGLE_MAPS` used on the thank-you header are present under `BOOK`.
- **No product code changes** this pass — behaviour already meets the stated bar on local dev.
- **Evidence:** `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front` exited **0** (es-ES navigator stub on first visit, picker locales, `?token=`, thank-you after submit in de, `/feedback/0` errors). `docker compose … logs --tail=40 front`: `Application bundle generation complete`, no TS errors in tail.

## Testing instructions

### What to verify

- Public `/feedback/{tenant}` (with and without `?token=…`) shows **no raw `FEEDBACK.*` strings** in the page body or **document title** for supported locales (picker + first-visit language detection).
- Error states (invalid id, tenant not found) and thank-you after submit stay fully translated.

### How to test

- Stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (HAProxy host port often **4202**).
- From repo root: `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front`  
  or `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`.
- Optional manual: `/feedback/1`, switch language, confirm title and strings match (no key paths).

### Pass / fail criteria

- **Pass:** Script exits **0**; logged `>>> RESULT: … OK` lines; no `FEEDBACK.` in visible UI or title during checks; front logs show successful bundle generation without TS/template errors.
- **Fail:** Raw i18n keys in DOM or title, script throws, or Angular errors in `docker compose … logs --tail=80 front`.

### Follow-up (outside automated test)

- Optional production check on **https://satisfecho.de**; GitHub **#67** comment / close when product accepts (`docs/agent-loop.md`).
