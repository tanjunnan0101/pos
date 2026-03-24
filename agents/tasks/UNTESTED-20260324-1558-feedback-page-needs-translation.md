# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (`/feedback/{tenant}`, e.g. with `?token=…` on production URLs) must show **fully translated** UI: every form label, message, error, and document title in the **selected** language—no mixed languages, missing strings, or raw `FEEDBACK.*` keys. Reporter cited `https://satisfecho.de/feedback/1?token=…` as an example.

Relevant areas: `front/src/app/feedback-public/`, locale JSON under `front/public/i18n/`, and `front/scripts/test-feedback-public-i18n.mjs` for regression coverage. Prior closed tasks under `agents/tasks/done/` document many verification passes on **development**; issue may still need production sign-off or gap fixes.

## High-level instructions for coder

- Reproduce on local Docker and optionally production: open `/feedback/{tenant}` with and without token; exercise the language picker and `Accept-Language`; confirm no untranslated segments or wrong-language copy.
- Ensure `FeedbackPublicComponent` template and programmatic strings (API errors, titles) use ngx-translate consistently; extend locale files for any missing keys across supported languages.
- Run or extend `npm run` / `node front/scripts/test-feedback-public-i18n.mjs` (with `BASE_URL` pointing at HAProxy dev port) so regressions are caught in CI or local smoke.
- If **development** already matches acceptance, document evidence for the issue; support a short GitHub verification comment and closing **#67** when product agrees (`docs/agent-loop.md`).

## Coder notes (2026-03-24)

- **Locales:** Compared `FEEDBACK` objects in `front/public/i18n/{en,de,fr,es,ca,zh-CN,hi}.json` — all **37** keys present in every file (no missing translations for public form strings).
- **Front:** `FeedbackPublicComponent` uses ngx-translate for template copy and `translate.stream()` for the document title (avoids raw keys before JSON load). Submit errors use `translate.instant` for known codes; invalid `reservation_token` comes from the API with `Accept-Language` (`back/app/messages.py`).
- **Automated check:** On local Docker (HAProxy `4202`), `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs` completed with **exit 0** (browser `es-ES` stub, picker de/fr/es/ca/zh-CN/hi, token URL, invalid-token submit DE message, thank-you DE, `/feedback/0`, `/feedback/999999999`).

## Testing instructions

1. Start the dev stack so the app is reachable (e.g. HAProxy on `4202`).
2. From repo root: `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs` — expect exit **0** and no `FEEDBACK.` substrings in the DOM assertions.
3. Optional manual: open `/feedback/1` with and without `?token=…`, switch languages, submit once — confirm no raw keys or mixed-language chrome.
4. For GitHub **#67** closure on production: repeat spot-check on `https://satisfecho.de/feedback/1` (or tenant under test) if product wants prod sign-off.
