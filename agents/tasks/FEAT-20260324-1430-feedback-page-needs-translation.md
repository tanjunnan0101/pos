# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URL (e.g. `/feedback/{tenant}` with optional `?token=…`) shows parts of the form or UI that are not translated for the selected language. Acceptance: every guest-visible part of the flow uses the active locale—no raw `FEEDBACK.*` keys in the DOM or document title. See `front/public/i18n/` and `FeedbackPublicComponent` (`front/src/app/feedback-public/`). Prior CLOSED archives under `agents/tasks/done/` document repeated dev/test passes; issue may stay open until product/production sign-off.

## High-level instructions for coder

- Reproduce on local Docker across supported locales (language picker and `Accept-Language`), with and without a valid reservation token.
- Confirm templates, dynamic strings, API error paths, and document title stay localized; fix any missing keys or pipe/`TranslateService` usage gaps.
- Align all locale JSON files under `front/public/i18n/` for `FEEDBACK` (and related keys) where needed.
- Run or extend feedback-public i18n smoke / Puppeteer coverage if present; document evidence for GitHub when dev matches acceptance.
- Optional: spot-check production (`https://satisfecho.de`) per `docs/agent-loop.md`; support closing **#67** when product agrees.
