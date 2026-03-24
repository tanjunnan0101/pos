# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public feedback flows (`/feedback/{tenant}`, tokenized links) must be fully localized: no raw `FEEDBACK.*` keys, validation and error copy respecting `Accept-Language` / locale picker. Implementation and repeated tester **PASS** are archived under `agents/tasks/done/` (e.g. `CLOSED-20260324-0345-feedback-page-needs-translation.md`). Issue **#67** remains **open** — treat as **final verification** (dev/staging/prod as needed), any **real i18n gaps**, and **GitHub alignment** (comment, labels, close when product accepts). See `docs/agent-loop.md` and `front/public/i18n/`.

## High-level instructions for coder

- Re-run smoke / Puppeteer paths for public feedback and landing if documented; confirm locales load on first paint and document titles are localized.
- If QA finds untranslated strings or API error text in the wrong language, trace `Accept-Language` / i18n keys in front and FastAPI validation messages; fix and add regression coverage where practical.
- When behaviour matches the issue everywhere tested: coordinate **close #67** on GitHub per `docs/agent-loop.md` (human with **Issues: write** if automation token cannot comment).
