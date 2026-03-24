# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public feedback flows (`/feedback/{tenant}`, tokenized links) must be fully localized: no raw `FEEDBACK.*` keys, validation and error copy respecting `Accept-Language` / locale picker. Implementation and repeated tester **PASS** are archived under `agents/tasks/done/` (e.g. `CLOSED-20260324-0345-feedback-page-needs-translation.md`). Issue **#67** remains **open** — treat as **final verification** (dev/staging/prod as needed), any **real i18n gaps**, and **GitHub alignment** (comment, labels, close when product accepts). See `docs/agent-loop.md` and `front/public/i18n/`.

## High-level instructions for coder

- Re-run smoke / Puppeteer paths for public feedback and landing if documented; confirm locales load on first paint and document titles are localized.
- If QA finds untranslated strings or API error text in the wrong language, trace `Accept-Language` / i18n keys in front and FastAPI validation messages; fix and add regression coverage where practical.
- When behaviour matches the issue everywhere tested: coordinate **close #67** on GitHub per `docs/agent-loop.md` (human with **Issues: write** if automation token cannot comment).

## Coder summary (2026-03-24 UTC)

- **`GET /public/tenants/{tenant_id}`:** Replaced hardcoded English **404** `detail` with `get_message("tenant_not_found", lang)` and `_get_requested_language`, matching `submit_public_guest_feedback` and other public endpoints (helps API clients and any UI that surfaces `detail`).
- **Tests:** `back/tests/test_guest_feedback.py` — `test_get_public_tenant_404_localized_de` asserts German copy when `Accept-Language: de`.
- **Smoke:** `front/scripts/test-feedback-public-i18n.mjs` — after **fr**, switches to **es**, asserts Spanish body copy (`Cómo fue`) and document title, still no `FEEDBACK.` substring in `document.body.innerText`.
- **FEEDBACK key parity:** Scripted diff across `front/public/i18n/*.json` — all locales match **en** (37 keys); no JSON edits this pass.

---

## Testing instructions

1. **Backend:** With DB up (e.g. dev compose):  
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back pytest /app/tests/test_guest_feedback.py -q`  
   Expect **6 passed** (includes `test_get_public_tenant_404_localized_de`).

2. **Public feedback i18n (Puppeteer):** With HAProxy reachable (e.g. **4202**):  
   `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`  
   Expect log line ending with **en + de + fr + es, no FEEDBACK.\* leaks** and exit **0**.

3. **Regression:**  
   `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit **0**.

4. **Front build:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no TS/NG errors after runs.

5. **Manual (optional):** `/feedback/1` — spot-check **ca**, **zh-CN**, **hi** in the language picker; confirm no raw keys.

6. **GitHub:** If tester **PASS** and product accepts, comment on **#67** and close per `docs/agent-loop.md` (PAT may lack `issues: write` for automated comments).
