# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `/feedback/{tenant}` with optional `?token=…`) must show **every part of the form** in the user’s selected language—no untranslated or mixed-language UI. Reporter example: production-style URL on satisfecho.de.

Multiple **`agents/tasks/done/`** archives document repeated implementation and tester **PASS** on local Docker for this theme; **#67** remains **open** on GitHub. Remaining work is typically **product verification** (especially production), any **real i18n gaps** discovered there, and **GitHub alignment** (verification comment, labels, close when product accepts). See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys in UI or document title.
- Run automated coverage where available (e.g. `npm run test:feedback-public-i18n --prefix front` with `BASE_URL` pointing at the dev stack) and fix any failures or gaps.
- If dev/staging already match acceptance, optional production spot-check on **satisfecho.de**; if product agrees, support closing **#67** with a short verification comment (human may post if automation lacks Issues write).
- Do not duplicate main-coder **NEW-** tasks for this issue—GitHub-driven work stays in this **FEAT-** queue.

---

## Coder verification (2026-03-24 UTC)

- **Code review:** `front/src/app/feedback-public/feedback-public.component.html` uses `translate` for all user-visible copy; `feedback-public.component.ts` sets the tab title via `translate.get()` and subscribes to `onLangChange` / `onTranslationChange` so titles stay localized after load (GitHub **#67**).
- **Locales:** `FEEDBACK` block in `en`, `de`, `es`, `fr`, `ca`, `zh-CN`, `hi` has the same keys as `en.json` (no missing public-form strings).
- **Automated:** `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front` — **PASS** (exit 0; five `>>> RESULT:` lines, no `FEEDBACK.` leaks in asserted checks). `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — **PASS**.
- **Product / GitHub:** No further app code changes required on current `development`; optional prod spot-check on **satisfecho.de** and human verification comment on **#67** when product accepts.

---

## Testing instructions

1. Stack up (e.g. `docker-compose.yml` + `docker-compose.dev.yml`, HAProxy on **4202**). Run:
   `BASE_URL=http://127.0.0.1:4202 npm run test:feedback-public-i18n --prefix front`  
   Expect exit **0** and **five** `>>> RESULT:` lines (es first-load stub, locale loop, `?token=`, post-submit thank-you `de`, `/feedback/0`); no raw `FEEDBACK.` substring in body or title checks asserted by the script.
2. Regression: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit **0**.
3. Optional manual: `/feedback/1` with and without `?token=…`, switch locale in the picker — no raw keys; tab title matches locale.
4. Optional prod: spot-check **satisfecho.de** if product wants **#67** closed with a prod-specific note.

**Closer / product:** On tester **PASS**, mirror verification on GitHub **#67** when agreed; archive per `agents/tasks/README.md`.
