# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback URLs (e.g. `https://satisfecho.de/feedback/1?token=…`) must show **the entire form and UI** in the selected language. The reporter still saw untranslated fragments on that flow.

Implementation and multiple tester **PASS** archives already exist under `agents/tasks/done/` for this theme; **#67** remains **open** on GitHub. Treat remaining work as **verification** (dev and, if product requires, production), any **real i18n gaps** found there, and **GitHub alignment** (short verification comment, labels, close when product accepts). See `front/public/i18n/`, `FeedbackPublicComponent`, and `docs/agent-loop.md`.

## High-level instructions for coder

- Re-read **#67** and verify `/feedback/{tenant}` with and without `?token=…` across supported locales (picker + `Accept-Language`); confirm no raw `FEEDBACK.*` keys in visible UI or document title.
- If dev/staging already match acceptance: optional production spot-check on **satisfecho.de**; if product agrees, post a verification comment on **#67** and support closing the issue (human may need to post if automation lacks **Issues** write on `gh`).
- Run or extend automated coverage if gaps appear (e.g. `front/scripts` feedback-public i18n tests when applicable).

## Coder notes (2026-03-24)

- **FEAT → WIP:** picked up for verification; **no `front/` or `back/` code changes** — public feedback flow already uses `FEEDBACK.*` for all visible copy and async document title updates (`FeedbackPublicComponent`).
- **Locale files:** `FEEDBACK` keys present and translated in `en`, `de`, `es`, `fr`, `ca`, `zh-CN`, `hi` under `front/public/i18n/`.
- **Automated:** `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs` — **PASS** (picker locales, `?token=`, submit → thank-you `de`, `/feedback/0` errors).
- **Regression smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — **PASS**.
- **Note (out of scope for public URL):** `SETTINGS.PUBLIC_GOOGLE_REVIEW_HINT` is still English in some non-`en` JSON files (staff settings hint only).
- **`gh issue comment`:** not posted from this environment (token lacks Issues write). Human can paste the summary from **Coder notes** + test commands into **#67** when closing the loop.

## Testing instructions

### What to verify

- Public `/feedback/{tenant}` shows **no raw `FEEDBACK.*` strings** in body or **document title**, with and without `?token=…`, for every language in the picker and for browser-default locale on first visit (no `pos_language`).
- Language switches update visible copy and tab title; submit flow reaches localized thank-you state.

### How to test

- Stack up (e.g. HAProxy dev): `docker compose -f docker-compose.yml -f docker-compose.dev.yml ps` — use host port from **haproxy** (often `4202`).
- From repo: `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`
- Optional manual: open `/feedback/1`, cycle languages, submit a rating; optional prod spot-check on `https://satisfecho.de/feedback/1` if product requires.

### Pass / fail criteria

- **Pass:** script exits 0; no `FEEDBACK.` substring in `document.body.innerText` or `document.title` during checks; thank-you and error states localized per selected language.
- **Fail:** any raw i18n key visible, wrong language after picker change, or script assertion failure — return task to **WIP** for coder.

### GitHub (#67)

- If tester and product accept: short verification comment on the issue; remove **agent:wip** / apply closure labels per `docs/agent-loop.md`; close **#67** when agreed.
