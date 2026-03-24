# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **every** user-visible part of the flow in the **selected** language—not mixed or English-only strings. The reporter wants the full form and related UI translated.

Relevant areas: `front/src/app/feedback-public/`, locale JSON under `front/public/i18n/`, and any API error messages surfaced on that route. See `docs/agent-loop.md` for optional GitHub closure / production sign-off after verification.

## High-level instructions for coder

- Reproduce on local Docker (`/feedback/{tenant}` with and without `?token=`) and compare with production URL pattern from the issue; exercise the language picker and supported locales.
- Ensure templates use translation for all guest-visible copy (including thank-you, validation, rate-limit, and invalid-tenant states); confirm document title tracks locale without flashing raw `FEEDBACK.*` keys.
- Align locale JSON files so no missing keys for strings used on this route.
- Run or extend `front/scripts/test-feedback-public-i18n.mjs` (or equivalent smoke) after changes; note evidence suitable for closing or updating the issue when product agrees.
