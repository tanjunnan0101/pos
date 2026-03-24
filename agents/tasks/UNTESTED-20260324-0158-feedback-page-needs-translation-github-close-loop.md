# Feedback page needs translation

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal

Public feedback URLs (e.g. `/feedback/{tenant}` with token) must show the full form in the user’s selected language. Reporter noted untranslated strings when opening the page with a language selected.

Delivery and tester **PASS** are already archived:

- `agents/tasks/done/2026/03/23/CLOSED-20260323-2214-feedback-page-needs-translation.md`
- `agents/tasks/done/2026/03/24/CLOSED-20260324-0133-feedback-page-needs-translation-close-loop.md`
- `agents/tasks/done/2026/03/24/CLOSED-20260324-0145-feedback-page-needs-translation-github-housekeeping.md` (includes `de.json` fix)

Issue **#67** is still **OPEN** on GitHub; primary remaining work is **process/GitHub alignment** (comment, labels, close when product agrees). Only implement further i18n if QA finds real gaps.

## High-level instructions for coder

- Re-read the three **CLOSED** archives above; treat them as the baseline unless new regressions appear.
- Optional quick smoke: public feedback route with language picker (locales already exercised in archives); confirm no missing keys or invalid locale JSON.
- Use **`gh`** (or a human with **Issues** write) on **#67**: post a short verification / closing comment, adjust labels per `docs/agent-loop.md`, and **close** the issue when product accepts. If automation token cannot comment (known `addComment` / `addLabelsToLabelable` restriction), document the handoff and stop after code/QA is confirmed.
- Do not duplicate large i18n implementation unless the issue scope is explicitly expanded on GitHub.

---

## Coder implementation (2026-03-24 UTC, feature coder)

### Baseline
- Re-read archived **CLOSED** tasks above; no new i18n code required.
- Public template `feedback-public.component.html` already pipes **`FEEDBACK.*`** through `translate`.

### Verification (this run)
- **`de.json`:** `node -e "JSON.parse(require('fs').readFileSync('front/public/i18n/de.json','utf8'))"` → OK.
- **Smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` → exit **0** (2026-03-24).
- **Docker `front` logs:** bundle generation complete, no TS/build errors in tail.

### GitHub **#67** (automation)
- **`gh issue comment 67 --repo satisfecho/pos`** → **`GraphQL: Resource not accessible by personal access token (addComment)`** (same as prior archives).
- **Hand off:** Human with **Issues** write should post the comment below, adjust labels per **`docs/agent-loop.md`** (remove **`agent:wip`** / **`agent:testing`** if present; close when product agrees), and **`gh issue close 67`**.

**Suggested closing comment for #67:**

> Verification (2026-03-24, dev on :4202, task `UNTESTED-20260324-0158-…`):
>
> - **Fix already on `development`:** `front/public/i18n/de.json` invalid JSON (missing comma) blocked German app-wide; fixed in archive **CLOSED-20260324-0145-…**. Current tree: `de.json` parses.
> - **Public `/feedback/{tenant}`:** Form uses `FEEDBACK.*` translations; DE/ES intros verified in prior tester PASS (archived).
> - **Smoke:** `npm run test:landing-version` with `BASE_URL=http://127.0.0.1:4202` passed.
>
> Closing; reopen if a locale shows missing keys.

---

## Testing instructions (tester)

1. **`de.json`:** From repo root:  
   `node -e "JSON.parse(require('fs').readFileSync('front/public/i18n/de.json','utf8')); console.log('OK')"` — must exit 0.
2. **Public feedback DE/ES:** With stack on **:4202**, open `/feedback/1` (no login). Language picker → **Deutsch** then **Español**; `.feedback-intro` should match German / Spanish copy (not English).
3. **Smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit 0.
4. **GitHub:** If product accepts, close **#67** with the suggested comment (automation token cannot comment).
