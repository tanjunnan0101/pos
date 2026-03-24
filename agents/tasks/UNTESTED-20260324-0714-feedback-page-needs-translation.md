# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (e.g. `/feedback/{tenant}` with optional `?token=…`, including production URLs) must show **fully localized** UI: no untranslated segments in the form or related states for the user’s selected language. Issue reporter listed several untranslated spots on the token deep link.

Prior **`agents/tasks/done/`** archives document repeated dev/test **PASS** on **`development`**; **#67** may remain open until optional production spot-check and product sign-off. See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and exercise `/feedback/{tenant}` with and without `?token=…` across supported locales (language picker and `Accept-Language`).
- Confirm no raw `FEEDBACK.*` keys (or other i18n leaks) in visible DOM, document title, or post-submit states.
- If anything is still missing, add keys in all locale JSON files under `front/public/i18n/` and bind in the guest feedback templates/components.
- Run or extend the existing feedback i18n smoke (Puppeteer under `front/scripts/` if present) and note results for the closer.
- If dev matches acceptance: optional verification on **satisfecho.de**; support a short GitHub verification comment and closing **#67** when product agrees.

## Coder verification (2026-03-24 UTC, feature-coder)

- **Flow:** `FEAT-20260324-0714-…` → `WIP-20260324-0714-…` on start.
- **Code review:** `FeedbackPublicComponent` (`front/src/app/feedback-public/`) uses `TranslateModule` / pipes for all guest-visible strings; document title uses `translate.get(…)` with subscriptions on `onLangChange` / `onTranslationChange` (issue **#67**). API error paths use `translate.instant` for rate limit, validation, and generic submit errors.
- **Locale parity:** `FEEDBACK` keys in `front/public/i18n/en.json` match the key set in `de`, `fr`, `es`, `ca`, `zh-CN`, `hi` (script check: no missing keys).
- **No product code changes** required in this pass; behaviour matches acceptance in dev.

### Evidence (automated)

- `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front` — **PASS** (commit **3435dce**, branch **development**).
- `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — **PASS**.

**Product:** Optional spot-check on **https://satisfecho.de/feedback/1** (and with a real reservation `?token=` if available); close **#67** when product agrees.

---

## Testing instructions

1. **Primary:** With app reachable (e.g. Docker dev on **4202**), from repo root:  
   `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front`  
   Expect exit **0** and log lines ending with “no FEEDBACK.* leaks” / “Invalid tenant … OK”.
2. **Regression:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit **0**.
3. **Manual (optional):** Open `/feedback/1`, cycle language picker; repeat with `?token=…`; open `/feedback/0` and confirm error strings are translated, not raw keys.
4. **Production (optional):** Same checks on **satisfecho.de** before closing **#67**.
