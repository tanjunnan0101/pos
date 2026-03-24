# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `/feedback/{tenant}` with `?token=…`) must show **the entire form and UI** in the user’s selected language. The reporter saw untranslated strings on production-style URLs. Multiple **`agents/tasks/done/`** archives document prior implementation and tester passes; **#67** remains **open** — treat remaining work as **final verification** (dev/staging/prod), any **real i18n gaps**, and **GitHub alignment** (comment, labels, close when product accepts). See `front/public/i18n/` and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-check `/feedback/{tenant}` with and without token across supported locales; confirm no raw `FEEDBACK.*` keys, correct document titles, and API validation/error copy respecting `Accept-Language` / locale picker where applicable.
- Run or extend Puppeteer/smoke coverage for public feedback if documented in `docs/testing.md`.
- If behaviour matches the issue everywhere tested: hand off for tester and coordinate **close #67** on GitHub per `docs/agent-loop.md` (human may need to post if automation lacks Issues write).
