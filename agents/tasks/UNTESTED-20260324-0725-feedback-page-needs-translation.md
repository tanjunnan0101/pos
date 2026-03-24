# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback at `/feedback/{tenant}` (e.g. with `?token=…`) must show **no untranslated UI**: the full form and related states in the selected language. Implementation and multiple tester **PASS** archives exist under `agents/tasks/done/` for this theme; **#67** remains **open** on GitHub. Remaining work is **product verification** (optional production on **satisfecho.de**), any **real i18n gaps** found there, and **GitHub alignment** (verification comment, labels, close when product accepts). See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If dev already matches acceptance, capture evidence for the issue; optional production spot-check on **satisfecho.de**; support a short verification comment and closing **#67** when product agrees.
- If gaps remain, fix copy, keys, or title handling in `FeedbackPublicComponent` and locale JSON; re-run the feedback i18n Puppeteer smoke if present.

## Coder (feature) — 2026-03-24

- **FEAT → WIP** on pickup. Reviewed `front/src/app/feedback-public/feedback-public.component.{ts,html}`: template uses `translate` pipe for all guest-visible copy; document title uses `translate.get` after `onLangChange` / `onTranslationChange` so raw `FEEDBACK.*` does not stick in the tab (issue #67).
- **No further front/i18n code changes** in this pass: locales under `front/public/i18n/` already define the keys used on the public form.
- **Evidence (local dev):** `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs` exited **0** (browser default `es-ES` stub, picker locales, token URL, post-submit thank-you in `de`, invalid `/feedback/0`). Front Docker logs: bundle generation complete, no TS/template errors.

## Testing instructions

### What to verify

- Public `/feedback/{tenant}` (with and without `?token=…`) shows **no raw `FEEDBACK.*` strings** in the page body or **document title** for any supported locale (picker + first-visit language detection).
- Error states (`invalid` id, tenant not found) and thank-you state after submit remain fully translated.

### How to test

- Stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (HAProxy e.g. **4202**).
- From repo root or `front/`:  
  `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`  
  or `npm run test:feedback-public-i18n --prefix front` with the same `BASE_URL` if the app is not on the default port probe list.
- Optional manual: open `/feedback/1`, switch language in the picker, confirm title and form strings match the locale (no key paths visible).

### Pass / fail criteria

- **Pass:** Script exits **0**; all logged lines show `>>> RESULT: … OK`; no `FEEDBACK.` substring in visible UI or title during checks.
- **Fail:** Any raw i18n key in DOM or title, script throws, or Angular build errors in `docker compose … logs --tail=80 front`.

### Follow-up (outside tester script)

- Optional production spot-check on **https://satisfecho.de**; GitHub **#67** verification comment and close when product accepts (see issue and `docs/agent-loop.md`).
