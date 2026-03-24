# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `/feedback/{tenant}` with optional `?token=…`) must show **every part of the form** in the user’s selected language. The reporter still sees untranslated strings on production-style URLs. Prior implementation and tester archives live under `agents/tasks/done/` (multiple **CLOSED** entries for this theme); align remaining work with `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys in UI or document title.
- If dev/staging already match acceptance, optional production spot-check on **satisfecho.de**; if product agrees, support closing **#67** with a short verification comment (human may post if automation lacks Issues write).
- Run or extend automated coverage for public feedback i18n if present under `front/scripts/`; keep landing/staff smoke passing per `AGENTS.md`.
- Do not open a **NEW-** task for this issue—GitHub-driven work stays in **FEAT-** queue.
