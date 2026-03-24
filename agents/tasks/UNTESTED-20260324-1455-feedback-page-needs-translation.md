# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (`/feedback/{tenant}`, e.g. with `?token=…`) must show fully translated UI: no missing strings, wrong language, or raw `FEEDBACK.*` keys in visible copy or document title. Reporter cited production-style URLs (e.g. satisfecho.de). Many **CLOSED** archives under `agents/tasks/done/` cover this theme; **#67** remains open until product verification and GitHub closure align with `docs/agent-loop.md`.

## High-level instructions for coder

- Reproduce `/feedback/{tenant}` with and without token across supported locales (`front/public/i18n/`, `FeedbackPublicComponent` under `front/src/app/feedback-public/`).
- Fix any remaining i18n gaps (JSON parity vs `en.json`, translate pipe / title handling, API error display).
- Run or extend automated checks (e.g. `front/scripts/test-feedback-public-i18n.mjs`) and document results for testers / product.

## Coder notes (2026-03-24)

- Checked **FEEDBACK** key parity: all locale files under `front/public/i18n/` match **en.json** (37 keys); no missing translations for public form strings.
- **Product code:** no change required for this pass — `FeedbackPublicComponent` already pipes copy through **ngx-translate**, sets the document title via **`translate.stream`**, and **`acceptLanguageInterceptor`** sends **Accept-Language** so FastAPI **`get_message`** errors match the picker.
- **Automation:** extended **`front/scripts/test-feedback-public-i18n.mjs`** with a submit on **`?token=`** bogus value while UI is **de**, asserting the German API **detail** string appears in **`.form-error`** and the DOM/title contain no raw **`FEEDBACK.*`** keys.

## Testing instructions

### What to verify

- Public **`/feedback/{tenant}`** (with and without **`?token=`**) shows no raw **`FEEDBACK.*`** keys in visible text or the browser tab title, for every language in the picker.
- After submit with an **invalid reservation token**, the inline error is **localized** (not English when **de** is selected) and still not a raw i18n key.

### How to test

- Stack up (e.g. `docker compose -f docker-compose.yml -f docker-compose.dev.yml`), note HAProxy port (often **4202**).
- From repo root or **`front/`**:
  - `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front`
  - Or: `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`
- Optional manual spot-check: open **`/feedback/1`**, switch languages, confirm headings/thank-you/error states and tab titles.

### Pass/fail criteria

- **Pass:** Puppeteer script exits **0**; all **`>>> RESULT:`** lines print; no assertion failures.
- **Fail:** Any visible **`FEEDBACK.`** substring in body text or document title, wrong language for the selected picker after load, or script timeout/error.
