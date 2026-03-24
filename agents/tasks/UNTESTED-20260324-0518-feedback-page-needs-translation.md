# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback at `/feedback/{tenant}` (optional `?token=…`) must be fully localized: no raw `FEEDBACK.*` keys, consistent copy and document title across locale picker and `Accept-Language`. Multiple **CLOSED** archives under `agents/tasks/done/2026/03/24/` record repeated tester **PASS** on dev; **#67** is still **open** on GitHub — treat remaining work as **product/GitHub alignment** (optional production spot-check if product wants it on record), and any **real** i18n gaps if found. See `front/public/i18n/` and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and spot-check `/feedback/{tenant}` with and without token across several locales (picker + `Accept-Language`).
- If anything still fails in prod/staging, fix i18n or loading order; otherwise document verification for closer.
- Coordinate **close #67** when product accepts: verification comment on the issue and labels per `docs/agent-loop.md` (automation here may lack **Issues** write on `gh` — human can mirror the task outcome on GitHub).

---

## Coder verification (2026-03-24 UTC)

- **Locales:** Compared `FEEDBACK` key set in `en.json` with `de`, `es`, `fr`, `ca`, `zh-CN`, `hi` — all keys present (parity with English).
- **UI / title:** `feedback-public.component` uses `translate` pipe / `TranslateService` for all guest-visible strings; `Title` updates via `translate.get()` on lang change and loading/error/thank-you states (issue #67 pattern).
- **Automated:** `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs` — **PASS** (es `Accept-Language` stub on first load, picker de/fr/es/ca/zh-CN/hi, `?token=`, `/feedback/0` error states, document titles). Regression: `npm run test:landing-version --prefix front` — **PASS**.
- **Code change this round:** None required; implementation already matches goal.

---

## Testing instructions

1. Stack up (e.g. HAProxy on 4202). Run:
   `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`
   Expect exit **0** and four `>>> RESULT:` lines (no `FEEDBACK.` substring in body text).
2. Optional manual: open `/feedback/1`, switch language in picker, confirm tab title updates and no raw keys flash (hard refresh).
3. Optional prod: repeat spot-check on production URL if product wants GitHub #67 closed with a prod note.
4. Regression: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit **0**.

**Closer / product:** If tester **PASS**, add verification comment on **#67** and close when agreed; archive this task per `agents/tasks/README.md`.
