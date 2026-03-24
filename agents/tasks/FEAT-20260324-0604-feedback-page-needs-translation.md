# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **the entire form and UI** in the selected language. The reporter still saw untranslated fragments on that flow.

Implementation and multiple tester **PASS** archives already exist under `agents/tasks/done/` for this theme; **#67** remains **open** on GitHub. Treat remaining work as **verification** (dev and, if product requires, production), any **real i18n gaps** found there, and **GitHub alignment** (short verification comment, labels, close when product accepts). See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If dev/staging already match acceptance: optional production spot-check on **satisfecho.de**; if product agrees, post a verification comment on **#67** and support closing the issue (human may need to post if automation lacks **Issues** write on `gh`).
- Run or extend automated coverage if gaps appear (e.g. `front/scripts` feedback-public i18n tests when applicable).
