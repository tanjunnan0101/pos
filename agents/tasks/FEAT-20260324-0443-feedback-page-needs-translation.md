# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **the entire form** in the user’s selected language. The reporter saw untranslated strings. Prior implementation and tester archives live under `agents/tasks/done/` (multiple **CLOSED** entries for this theme); **#67** remains **open** — finish verification, close any real i18n gaps, and align GitHub (comment / labels / close when product accepts). See `front/public/i18n/` and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and spot-check `/feedback/{tenant}` with and without token across several locales (picker + `Accept-Language`).
- Confirm no raw `FEEDBACK.*` keys in visible UI, titles, or validation copy; extend locale JSON if anything is missing.
- Run or extend the public feedback Puppeteer / smoke scripts documented in `AGENTS.md` / `docs/testing.md` if useful.
- When behaviour matches acceptance: hand off to tester; coordinate **close #67** per `docs/agent-loop.md` (human may need to post if automation lacks Issues write).
