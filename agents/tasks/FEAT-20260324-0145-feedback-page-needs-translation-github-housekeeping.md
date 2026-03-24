# Feedback page needs translation

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal
Public feedback URL (e.g. `/feedback/{tenant}` with token) should show the full form in the user’s selected language. Prior implementation and tester **PASS** are archived under `agents/tasks/done/2026/03/23/CLOSED-20260323-2214-feedback-page-needs-translation.md` and follow-up verification under `agents/tasks/done/2026/03/24/CLOSED-20260324-0133-feedback-page-needs-translation-close-loop.md`. Issue **#67** remains **open** on GitHub mainly for housekeeping: add a closing comment, apply labels per `docs/agent-loop.md`, and **close** when product agrees. Only reopen or extend scope if QA finds untranslated strings.

## High-level instructions for coder
- Re-verify on dev stack (language picker + key locales) that feedback UI strings still localize; fix any regressions if found.
- If behaviour matches the issue: use **`gh`** (or human with **Issues** write) to comment on **#67** with verification summary, adjust labels (**`agent-planned`** / **`agent:wip`** / **`agent:testing`** as appropriate), and **close** the issue.
- If **`gh`** fails with token scope errors, document outcome in the task and hand off to a human with repo permissions (same pattern as prior CLOSED archives).
