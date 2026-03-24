# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (`/feedback/{tenant}`, e.g. with `?token=…`) must show **fully translated** UI: every part of the form and related states in the selected language—no leftover English or raw translation keys. Reporter cited **satisfecho.de** example URL. Prior **`agents/tasks/done/`** archives record repeated dev/test **PASS** on **`development`**; the issue may still be open until **production** verification and product sign-off. See `front/public/i18n/`, `FeedbackPublicComponent` (`front/src/app/feedback-public/`), and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and reproduce on local Docker (`/feedback/{tenant}`, with and without token) across supported locales (language picker and `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If gaps remain, extend JSON in `front/public/i18n/` and wire any missing strings in `FeedbackPublicComponent` (template + title + error paths).
- If dev already matches acceptance, capture concise evidence; optional production check on **https://satisfecho.de**; support product/GitHub closure of **#67** when agreed (`docs/agent-loop.md`).
