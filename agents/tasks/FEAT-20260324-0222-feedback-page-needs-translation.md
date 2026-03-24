# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public feedback URL (e.g. `/feedback/{tenant}` with token) must show **every** part of the form in the user’s selected language. The reporter noted untranslated strings on the live-style URL. Prior implementation and multiple tester **PASS** archives exist under `agents/tasks/done/` (e.g. `CLOSED-20260323-2214-feedback-page-needs-translation.md` and 2026-03-24 close-loop / housekeeping / alignment tasks); issue **#67** is still **open** on GitHub.

## High-level instructions for coder

- Re-verify `/feedback/{tenant}` across supported locales (language picker + direct navigation); confirm `FEEDBACK` (and related) keys in `front/public/i18n/*.json` cover all UI copy, including errors and success states.
- If any gap remains, add or fix keys and bindings only where needed; validate JSON (no syntax regressions like past `de.json` issues).
- Run targeted smoke / Puppeteer if documented for feedback or landing; align with `docs/agent-loop.md` for GitHub handoff when product accepts closure of **#67**.
