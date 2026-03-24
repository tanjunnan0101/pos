# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **the entire form** in the user’s selected language. The reporter saw untranslated strings. Prior implementation and tester archives live under `agents/tasks/done/` (multiple **CLOSED** entries for this theme); **#67** remains **open** — finish verification, close any real i18n gaps, and align GitHub (comment / labels / close when product accepts). See `front/public/i18n/` and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and spot-check `/feedback/{tenant}` with and without token across several locales (picker + `Accept-Language`).
- Confirm no raw `FEEDBACK.*` keys in visible UI, titles, or validation copy; extend locale JSON if anything is missing.
- Run or extend the public feedback Puppeteer / smoke scripts documented in `AGENTS.md` / `docs/testing.md` if useful.
- When behaviour matches acceptance: hand off to tester; coordinate **close #67** per `docs/agent-loop.md` (human may need to post if automation lacks Issues write).

## Coder notes (2026-03-24 UTC)

- **FEEDBACK / BOOK keys:** Scripted diff — every locale’s `FEEDBACK` object matches `en.json` keys; `BOOK.ADDRESS` and `BOOK.OPEN_IN_GOOGLE_MAPS` (used on the public feedback hero) exist in all seven locale files.
- **Product change:** `FeedbackPublicComponent` merges `TranslateService.onLangChange` and `onTranslationChange` so the browser tab title updates when translations arrive after first paint (issue **#67**).
- **Automated smoke:** `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs` → **exit 0**; `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` → **exit 0**. Front container logs: **Application bundle generation complete** after the edit (no TS/NG errors in tail).
- **GitHub #67:** Closing the issue still needs a human/token with **Issues: write** if `gh issue comment` / close is blocked (see prior archived tasks).

## Testing instructions

### What to verify

1. Public `/feedback/1` (and optional `?token=…`): language picker cycles **en, de, fr, es, ca, zh-CN, hi** — form, thank-you path, and **SETTINGS.SELECT_LANGUAGE** aria context show no raw `FEEDBACK.*` in the DOM.
2. **Browser tab title** while loading and after load matches the selected locale (tenant name prefix when tenant is valid).
3. Invalid tenant **`/feedback/0`**: error copy and title follow locale after switching language (including **de** “Ungültiger …”).
4. No Angular build errors in the front container after any edits.

### How to test

- Stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (e.g. `http://127.0.0.1:4202`).
- Automated: `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`
- Regression: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`
- Logs: `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front`

### Pass / fail criteria

- **PASS:** `test-feedback-public-i18n` **exit 0**; no visible `FEEDBACK.` key leaks; document titles assert as in script; landing-version **exit 0**; front rebuild succeeds.
- **FAIL:** Any raw `FEEDBACK.*` in body text, wrong-locale copy where a translation exists, or front build failure.

### Suggested GitHub comment (human with token)

> Verified 2026-03-24: public `/feedback/:id` i18n + tab title refresh on translation load; Puppeteer `test-feedback-public-i18n` passes. Please close **#67** if product agrees.
