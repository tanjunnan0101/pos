# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public feedback (`/feedback/{tenant}`) should be fully localized. Implementation and tester verification are already archived under `agents/tasks/done/2026/03/23/CLOSED-20260323-2214-feedback-page-needs-translation.md` and follow-ups in `agents/tasks/done/2026/03/24/` (close-loop and housekeeping). Issue **#67** remains **open** on GitHub; remaining work is mainly **alignment**: confirm behaviour still matches the issue, then **comment**, **labels**, and **close** on GitHub when product accepts (per `docs/agent-loop.md`). Re-open or extend scope only if QA finds untranslated strings or regressions.

## High-level instructions for coder

- Re-smoke public feedback for tenant 1 (or a test tenant): language picker, `FEEDBACK` strings, and invalid-tenant path; spot-check `front/public/i18n/*.json` for syntax if locales fail to load.
- If anything is broken, fix in `front/` only; otherwise document **PASS** with short test notes for the tester handoff.
- **GitHub:** Post a short verification or closing comment on **#67**, add label **`agent-planned`** if appropriate (repo uses hyphen; prompt’s `agent:planned` may not exist), and **close** when product agrees. If `gh issue comment` / `gh issue edit` fails with `Resource not accessible by personal access token`, hand off to a human with **Issues: write** (known automation limit in prior runs).
