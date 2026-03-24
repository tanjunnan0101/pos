# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback at `/feedback/{tenant}` (e.g. with `?token=…`) must show **no untranslated UI**: the full form and related states in the selected language. Implementation and multiple tester **PASS** archives exist under `agents/tasks/done/` for this theme; **#67** remains **open** on GitHub. Remaining work is **product verification** (optional production on **satisfecho.de**), any **real i18n gaps** found there, and **GitHub alignment** (verification comment, labels, close when product accepts). See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If dev already matches acceptance, capture evidence for the issue; optional production spot-check on **satisfecho.de**; support a short verification comment and closing **#67** when product agrees.
- If gaps remain, fix copy, keys, or title handling in `FeedbackPublicComponent` and locale JSON; re-run the feedback i18n Puppeteer smoke if present.
