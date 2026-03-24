# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **every** part of the form and related UI in the **selected** language—not a mix of English and the locale. The reporter saw untranslated strings on that flow. Prior implementation and multiple **CLOSED** tasks under `agents/tasks/done/` document rounds of i18n work and tester passes; the issue remains **open**—treat this queue item as **feature-coder follow-up**: confirm no regressions, close any real gaps, and support **GitHub alignment** (comment / labels / close when product accepts). See `docs/agent-loop.md` and `front/public/i18n/`.

## High-level instructions for coder

- Exercise `/feedback/{tenant}` with and without a valid token across several locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys or English fallbacks where translations exist.
- Ensure API-driven validation or error messages on that flow respect locale where the backend already supports it; extend i18n keys or server messages only if gaps are real.
- Re-run or extend any existing Puppeteer/locale checks for public feedback if documented in `docs/testing.md` or `front/scripts/`.
- When behaviour matches the issue in the environments you test, hand off for tester and for **#67** closure per `docs/agent-loop.md` (human may need to post on GitHub if automation lacks Issues write).
