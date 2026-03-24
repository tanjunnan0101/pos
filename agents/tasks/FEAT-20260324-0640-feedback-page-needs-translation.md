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
