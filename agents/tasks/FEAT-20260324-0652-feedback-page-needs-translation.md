# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback at `/feedback/{tenant}` (e.g. with `?token=…`) must show **no untranslated UI**: every part of the form and related states in the selected language. Prior CLOSED archives under `agents/tasks/done/` record repeated dev verification; **#67** remains open — align implementation with issue acceptance, optional production check on **satisfecho.de**, and GitHub closure when product agrees. See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If dev already matches acceptance, document evidence for the issue; optional production spot-check; support verification comment and close **#67** when product accepts.
- If gaps remain, extend JSON under `front/public/i18n/` and template/bindings in `feedback-public` until all guest-visible copy is translated.
- Keep or extend automated checks (e.g. Puppeteer feedback i18n script) so regressions are caught.
