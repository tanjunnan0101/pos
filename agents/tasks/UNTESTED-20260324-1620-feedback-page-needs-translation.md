# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public guest feedback (`/feedback/{tenant}`, e.g. with `?token=…` on production-style URLs) must show **fully translated** UI: every part of the form and related states in the selected language, with **no raw `FEEDBACK.*` keys** in visible copy or document title. Prior agent archives under `agents/tasks/done/` record repeated **PASS** on local Docker; the GitHub issue remains **open**—align **production** behaviour, capture evidence, and close the loop on the issue when product agrees (`docs/agent-loop.md`).

## High-level instructions for coder

- Re-verify on local stack: `FeedbackPublicComponent` (`front/src/app/feedback-public/`), locale files under `front/public/i18n/`, and automated check `npm run test:feedback-public-i18n --prefix front` (or `node front/scripts/test-feedback-public-i18n.mjs` with `BASE_URL`).
- Spot-check **production** (`https://satisfecho.de/feedback/…` or tenant under test) for the same acceptance bar; fix any real gaps (missing keys, title flicker, wrong locale) rather than re-litigating already-green dev-only paths.
- If behaviour matches acceptance, post a short verification summary on **#67** (or hand to closer with `issues:write`) and support closing the issue when product accepts.

## Testing instructions

**What to verify**

- Public `/feedback/{tenant}`: no raw `FEEDBACK.*` in visible copy or document title; browser tab title follows the active locale (not stuck on the default `POS - Point of Sale` from `index.html`), including first visit with browser language auto-detect (e.g. Spanish).

**How to test**

- Local (stack on HAProxy, e.g. port 4202):  
  `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`
- **Production** (after this build is deployed):  
  `BASE_URL=https://satisfecho.de node front/scripts/test-feedback-public-i18n.mjs`  
  Prior to deploy, production could pass the DOM checks but fail the **document title** assertion on first-load ES auto-detect; that gap is what the code change addresses.

**Pass / fail**

- **Pass:** Script exits 0; all `>>> RESULT:` lines print; no assertion errors.
- **Fail:** Any raw `FEEDBACK.` in body/title, or missing localized substring in `document.title` where the script expects it (see script comments for #67).
