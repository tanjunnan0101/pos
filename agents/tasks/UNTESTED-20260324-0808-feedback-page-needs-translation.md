# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (`/feedback/{tenant}`, e.g. with `?token=…`) must show **fully translated** UI: every part of the form and related states in the selected language—no leftover English or raw translation keys. Reporter cited **satisfecho.de** example URL. Prior **`agents/tasks/done/`** archives record repeated dev/test **PASS** on **`development`**; the issue may still be open until **production** verification and product sign-off. See `front/public/i18n/`, `FeedbackPublicComponent` (`front/src/app/feedback-public/`), and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and reproduce on local Docker (`/feedback/{tenant}`, with and without token) across supported locales (language picker and `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If gaps remain, extend JSON in `front/public/i18n/` and wire any missing strings in `FeedbackPublicComponent` (template + title + error paths).
- If dev already matches acceptance, capture concise evidence; optional production check on **https://satisfecho.de**; support product/GitHub closure of **#67** when agreed (`docs/agent-loop.md`).

## Coder verification (2026-03-24 UTC)

- **i18n parity:** Ran a small Node check on `front/public/i18n/*.json`: every locale’s `FEEDBACK` object has the **same 37 keys** as `en.json` (de, es, fr, ca, hi, zh-CN included). `BOOK.ADDRESS` and `BOOK.OPEN_IN_GOOGLE_MAPS` exist in all files (used on the public feedback page next to `FEEDBACK.*` strings).
- **Component:** `FeedbackPublicComponent` template uses the translate pipe for all guest-visible `FEEDBACK.*` strings; document title uses `TranslateService.stream()` and reacts to `onLangChange` / `onTranslationChange` / `onDefaultLangChange` (avoids raw keys in the tab, issue **#67**).
- **API localization:** `acceptLanguageInterceptor` adds `Accept-Language` from `LanguageService`; backend guest-feedback endpoint uses `_get_requested_language` + `get_message()` for localized 400/404 details where applicable.
- **Smoke:** `GET http://127.0.0.1:4202/feedback/1` → **200**. `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` → **exit 0** (2026-03-24). Front container logs: bundle generation **complete**, no TS errors in tail.
- **Code change:** None required in this pass; acceptance on **development** already met by current tree.

## Testing instructions (for tester)

1. **Stack:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml up` (or project norm); HAProxy e.g. **4202**.
2. **Happy path:** Open `http://127.0.0.1:4202/feedback/1` (replace `1` with a real tenant id). With and without `?token=…` when a valid reservation token exists for that tenant.
3. **Locales:** Use the header language picker for **en, de, es, fr, ca, hi, zh-CN**. Confirm: no visible raw keys like `FEEDBACK.TITLE`; form, loading state, error shell, thank-you block, and **browser tab title** are all in the selected language.
4. **Error states:** `http://127.0.0.1:4202/feedback/0` (or non-numeric id) → invalid-tenant message translated. Unknown tenant id → not-found message translated.
5. **Submit errors (optional):** With UI in e.g. **Deutsch**, submit invalid contact email/phone or trigger rate limit; confirm user-visible message is German (frontend `FEEDBACK.*` and/or backend `detail` via `Accept-Language`), not a bare key.
6. **Regression:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` → exit **0**.
7. **Production (optional):** After deploy, spot-check `https://satisfecho.de/feedback/<tenant>` for the same checks; close **#67** when product agrees.
