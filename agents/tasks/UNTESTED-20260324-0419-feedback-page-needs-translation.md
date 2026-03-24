# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **every** part of the form and related UI in the **selected** language—not a mix of English and the locale. The reporter saw untranslated strings on that flow. Prior implementation and multiple **CLOSED** tasks under `agents/tasks/done/` document rounds of i18n work and tester passes; the issue remains **open**—treat this queue item as **feature-coder follow-up**: confirm no regressions, close any real gaps, and support **GitHub alignment** (comment / labels / close when product accepts). See `docs/agent-loop.md` and `front/public/i18n/`.

## High-level instructions for coder

- Exercise `/feedback/{tenant}` with and without a valid token across several locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys or English fallbacks where translations exist.
- Ensure API-driven validation or error messages on that flow respect locale where the backend already supports it; extend i18n keys or server messages only if gaps are real.
- Re-run or extend any existing Puppeteer/locale checks for public feedback if documented in `docs/testing.md` or `front/scripts/`.
- When behaviour matches the issue in the environments you test, hand off for tester and for **#67** closure per `docs/agent-loop.md` (human may need to post on GitHub if automation lacks Issues write).

## Coder implementation (2026-03-24)

- **Document title:** `FeedbackPublicComponent` now sets the tab title via `TranslateService.get()` instead of `instant()`, so the browser tab does not briefly show raw keys like `FEEDBACK.LOADING` while `/i18n/*.json` is still loading (GitHub #67).
- **Automated coverage:** `front/scripts/test-feedback-public-i18n.mjs` now switches the language picker to **ca** and **zh-CN** in addition to de/fr/es, and asserts body text and `document.title` contain expected localized phrases with no `FEEDBACK.*` substrings.
- **API locale:** No backend change; guest-feedback POST already uses `_get_requested_language` and the Angular `acceptLanguageInterceptor` already sends `Accept-Language` from the picker.

---

## Testing instructions

1. Stack up (e.g. HAProxy on `http://127.0.0.1:4202`).
2. **Automated:** `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front` — expect two `>>> RESULT:` lines (main locales + token URL), exit **0**.
3. **Manual spot-check:** Open `/feedback/1` (and with a real or dummy `?token=`). Switch **English → Deutsch → Français → Español → Català → 中文（简体）**; confirm form labels, buttons, intro, and thank-you copy are fully translated (no `FEEDBACK.` literals). Optionally hard-refresh and confirm the **tab title** never flashes a raw key during load.
4. **Regression:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` exits **0**.
5. **Product / GitHub:** If all pass, note on **#67** for closure when product agrees.
