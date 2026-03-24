# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback at `/feedback/{tenant}` (optional `?token=…`) must be fully localized: no raw `FEEDBACK.*` keys, consistent copy and document title across locale picker and `Accept-Language`. Multiple **CLOSED** archives under `agents/tasks/done/2026/03/24/` record repeated tester **PASS** on dev; **#67** is still **open** on GitHub — treat remaining work as **product/GitHub alignment** (optional production spot-check if product wants it on record), and any **real** i18n gaps if found. See `front/public/i18n/` and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and spot-check `/feedback/{tenant}` with and without token across several locales (picker + `Accept-Language`).
- If anything still fails in prod/staging, fix i18n or loading order; otherwise document verification for closer.
- Coordinate **close #67** when product accepts: verification comment on the issue and labels per `docs/agent-loop.md` (automation here may lack **Issues** write on `gh` — human can mirror the task outcome on GitHub).
