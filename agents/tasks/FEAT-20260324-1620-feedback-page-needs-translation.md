# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (`/feedback/{tenant}`, e.g. with `?token=…` on production-style URLs) must show **fully translated** UI: every part of the form and related states in the selected language, with **no raw `FEEDBACK.*` keys** in visible copy or document title. Prior agent archives under `agents/tasks/done/` record repeated **PASS** on local Docker; the GitHub issue remains **open**—align **production** behaviour, capture evidence, and close the loop on the issue when product agrees (`docs/agent-loop.md`).

## High-level instructions for coder

- Re-verify on local stack: `FeedbackPublicComponent` (`front/src/app/feedback-public/`), locale files under `front/public/i18n/`, and automated check `npm run test:feedback-public-i18n --prefix front` (or `node front/scripts/test-feedback-public-i18n.mjs` with `BASE_URL`).
- Spot-check **production** (`https://satisfecho.de/feedback/…` or tenant under test) for the same acceptance bar; fix any real gaps (missing keys, title flicker, wrong locale) rather than re-litigating already-green dev-only paths.
- If behaviour matches acceptance, post a short verification summary on **#67** (or hand to closer with `issues:write`) and support closing the issue when product accepts.
