# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (`/feedback/{tenant}`, optional `?token=…`) must be fully localized: no raw `FEEDBACK.*` keys, consistent copy and document title across locale picker and `Accept-Language`. Multiple **CLOSED** archives under `agents/tasks/done/` record implementation and tester **PASS** on dev; **#67** remains **open** — finish **product verification** (especially production if not yet spot-checked), close any real gaps, and **align GitHub** (comment, labels, close when accepted). See `front/public/i18n/` and `docs/agent-loop.md`.

## High-level instructions for coder

- Confirm behaviour on the stack you use: several locales, with and without token, invalid-tenant paths; document title after translation load.
- If anything still fails in prod/staging, fix i18n or loading order; otherwise hand off to tester and support **close #67** per `docs/agent-loop.md`.
- Run or point to `test-feedback-public-i18n` (or equivalent) from `front/scripts/` / `docs/testing.md` when claiming verification.
- **GitHub:** Post a short verification comment on **#67** and close when product agrees (automation here may lack **Issues** write on `gh`).

---

## Coder verification (2026-03-24 UTC)

- Stack: `docker-compose.yml` + `docker-compose.dev.yml`, **BASE_URL** `http://127.0.0.1:4202`.
- Ran `npm run test:feedback-public-i18n --prefix front` — **PASS** (browser default `es-ES` stub, locale picker `en`→`de`→`fr`→`es`→`ca`→`zh-CN`→`hi`, `?token=` path, invalid tenant `/feedback/0` + DE title/body). No raw `FEEDBACK.*` in DOM; document titles matched expectations.
- **Product code:** No changes required on current `development` for dev verification.

---

## Testing instructions

### What to verify

- Public `/feedback/{tenant}` (and optional `?token=…`) shows translated copy only (no visible `FEEDBACK.*` keys), including loading and error states.
- Locale picker switches all visible strings and the **document title** consistently.
- Invalid tenant (`/feedback/0`) error UI and tab title localize when switching language.

### How to test

- Start dev stack (HAProxy on host port **4202** typical).
- From repo: `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front`
- Optional manual spot-check: production `https://satisfecho.de/feedback/1` (or tenant URL in use) with 2–3 locales and hard refresh.

### Pass / fail criteria

- **PASS:** Script exits **0** and prints the four `>>> RESULT:` lines (browser-default ES, main locale sweep, token URL, invalid tenant).
- **FAIL:** Any timeout, exit **1**, or visible `FEEDBACK.` in page text.

### GitHub (#67)

- If **PASS** and product agrees: comment on **#67** with environment tested (dev/prod) and close the issue; label per `docs/agent-loop.md`.
