# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback at `/feedback/{tenant}` (e.g. with `?token=…`) must be fully localized: every part of the form and UI in the selected language, no raw `FEEDBACK.*` keys, consistent document title across locale picker and `Accept-Language`. Prior **FEAT-**/**CLOSED-** archives under `agents/tasks/done/` document repeated dev verification; issue may still be open pending product/production confirmation.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (`front/public/i18n/`, `FeedbackPublicComponent`).
- Confirm no untranslated strings or title leaks; fix any gaps in templates, `TranslateService`, or JSON keys.
- Run the dedicated feedback i18n / landing smoke scripts from `docs/testing.md` or `AGENTS.md` on the dev stack.
- If dev matches acceptance: optional production spot-check on **satisfecho.de**; coordinate verification comment and close **#67** with product per `docs/agent-loop.md`.

## Implementation notes (coder, 2026-03-24 UTC)

- Renamed **FEAT-20260324-0640** → **WIP-20260324-0641** on pickup.
- Compared `FEEDBACK` keys in `front/public/i18n/{en,de,es,fr,ca,zh-CN,hi}.json`: **37** keys each, no gaps vs `en.json`.
- `FeedbackPublicComponent` already uses the translate pipe for all user-visible copy; tab title uses `TranslateService.get` with subscriptions on `onLangChange` / `onTranslationChange` so the document title stays aligned with the picker and does not show raw keys before JSON loads (**#67**).
- **No application code changes** were required in this pass; behaviour matches acceptance on the dev stack.

---

## Testing instructions

1. **Stack:** Dev compose with HAProxy (e.g. port **4202**): `docker compose -f docker-compose.yml -f docker-compose.dev.yml ps` shows services up.
2. **Feedback i18n (required):** From repo root:
   `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`  
   Expect success logs for: browser default `es` stub, locale switches (en/de/fr/es/ca/zh-CN/hi), `?token=` path, post-submit thank-you (de), invalid `/feedback/0` (en + de); **no** `FEEDBACK.` substring in asserted UI.
3. **Regression:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` exits **0**.
4. **Optional manual:** Open `/feedback/1` and `/feedback/1?token=…`; switch language in the header picker; confirm form, errors, thank-you, and **browser tab title** are localized (no raw keys).

**Product / GitHub:** If tester passes, optional comment on **#67** and close with product after any production spot-check.
