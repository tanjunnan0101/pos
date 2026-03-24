# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **every part of the form** in the user’s selected language; several strings were still untranslated. Prior implementation and tester archives live under `agents/tasks/done/` (multiple **CLOSED** entries for this theme); confirm behaviour on dev and production, close any real i18n gaps, and align GitHub (verification comment, labels, close when product accepts). See `front/public/i18n/`, `docs/agent-loop.md`, and Puppeteer `test-feedback-public-i18n` if present.

## High-level instructions for coder

- Re-read **#67** and spot-check `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`).
- Ensure no raw `FEEDBACK.*` keys leak in the DOM or document title; titles should follow translation load (avoid brief key flashes after first paint).
- Run the project’s public feedback i18n smoke / Puppeteer coverage and fix any failures.
- If dev matches acceptance: optional production spot-check on **satisfecho.de**; coordinate **close #67** with a short verification comment when product agrees.

---

## Coder verification (2026-03-24 UTC)

- **Locales:** `FEEDBACK` key parity `en` vs `de`, `es`, `fr`, `ca`, `zh-CN`, `hi` — all keys present (script check).
- **UI / title:** `feedback-public` already uses `translate` pipe / `TranslateService`; document title uses `translate.get()` with lang / translation change subscriptions (issue #67).
- **Tests:** Extended `front/scripts/test-feedback-public-i18n.mjs` with a **POST submit → thank-you** step (locale `de`, asserts “Vielen Dank” in body, no `FEEDBACK.` in body or tab title). Existing coverage unchanged (es first-load stub, picker loop, `?token=`, `/feedback/0`).

---

## Testing instructions

1. Stack up (e.g. HAProxy on **4202**). Run:
   `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`  
   Expect exit **0** and **six** `>>> RESULT:` lines (including post-submit thank-you); no `FEEDBACK.` substring in asserted body/title checks.
2. Regression: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit **0**.
3. Optional manual: `/feedback/1`, switch locale, hard refresh — no raw keys; tab title matches locale.
4. Optional prod: spot-check **satisfecho.de** if product wants **#67** closed with a prod note.

**Closer / product:** On tester **PASS**, mirror verification on GitHub **#67** when agreed; archive per `agents/tasks/README.md`.
