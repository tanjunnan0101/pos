# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **the entire form and UI** in the user’s selected language. The reporter saw untranslated strings on production-style URLs.

Many **CLOSED** archives under `agents/tasks/done/` document repeated implementation and tester **PASS** on local Docker for this theme; **#67** remains **open** on GitHub. Remaining work is typically **product verification** (especially production), any **real i18n gaps** found there, and **GitHub alignment** (verification comment, labels, close when product accepts). See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If dev/staging already match acceptance: optional production spot-check on **satisfecho.de**; if product agrees, post a short verification comment on **#67** and support closing the issue.
- If gaps remain, fix i18n JSON, template bindings, or title/update timing; extend automated coverage if a regression path is identified.

## Implementation notes (coder, 2026-03-24 UTC)

- **Code review:** `front/src/app/feedback-public/feedback-public.component.html` uses `translate` for all guest-visible copy; shared `BOOK.*` keys (address / Google Maps) exist in every locale under `front/public/i18n/*.json`.
- **Title:** `feedback-public.component.ts` sets the document title via `translate.get(...)` and subscribes to `onLangChange` / `onTranslationChange` so the tab title does not show raw `FEEDBACK.*` keys (issue #67).
- **Locale parity:** Script check: all `FEEDBACK` keys in `en.json` are present in `de`, `es`, `fr`, `ca`, `zh-CN`, `hi` (37 keys each).
- **No product code changes** were required in this pass; behaviour matches acceptance on local Docker.

---

## Testing instructions

1. **Automated (primary):** With stack up (`docker-compose.yml` + `docker-compose.dev.yml`, HAProxy e.g. `http://127.0.0.1:4202`):
   ```bash
   BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs
   ```
   Expect exit **0** and log lines ending in: browser default **es** stub OK; **en + de + fr + es + ca + zh-CN + hi** no `FEEDBACK.*` in DOM; **token** URL OK; post-submit **thank-you** (de) OK; **invalid** `/feedback/0` error UI i18n OK.

2. **Manual spot-check:** Open `/feedback/1` (and with a real `?token=` if available). Use the language picker: confirm form, errors, thank-you state, and **browser tab title** are localized (no literal `FEEDBACK.` in the page).

3. **Accept-Language:** First visit with cleared `localStorage` (`pos_language`): `LanguageService` maps `navigator.language` to a supported code (see `test-feedback-public-i18n.mjs` es-ES stub). API requests send `Accept-Language` via `accept-language.interceptor.ts`.

4. **Regression:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` exits **0**.

5. **Production / GitHub:** Optional: repeat (2) on **satisfecho.de**. If product accepts, add a short verification comment on **#67** and close when appropriate.

---

## Test report (coder self-check, 2026-03-24 UTC)

| Step | Result |
|------|--------|
| `test-feedback-public-i18n.mjs` | **PASS** |
| `test:landing-version` | **PASS** |
| Front Docker logs (recent) | **PASS** (bundle complete, no TS errors) |

**GitHub:** **#67** still needs human/product confirmation and close when satisfied.
