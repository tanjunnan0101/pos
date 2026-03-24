# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **no untranslated UI**: every part of the form and related states should follow the selected language. Prior **CLOSED** archives under `agents/tasks/done/` document repeated dev/test **PASS**; the issue may stay open until optional production verification and product sign-off. See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (language picker and `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If dev already matches acceptance, capture evidence for GitHub; optional production spot-check on **satisfecho.de**; support a short verification comment and closing **#67** when product agrees.
- If gaps remain, extend `front/public/i18n/*.json` and `feedback-public` templates so all guest-visible strings and titles stay localized.
