# Feedback page needs translation

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal
Public feedback URL (e.g. `/feedback/{tenant}` with token) should show the full form in the user’s selected language. Prior implementation and tester **PASS** are archived under `agents/tasks/done/2026/03/23/CLOSED-20260323-2214-feedback-page-needs-translation.md` and follow-up verification under `agents/tasks/done/2026/03/24/CLOSED-20260324-0133-feedback-page-needs-translation-close-loop.md`. Issue **#67** remains **open** on GitHub mainly for housekeeping: add a closing comment, apply labels per `docs/agent-loop.md`, and **close** when product agrees. Only reopen or extend scope if QA finds untranslated strings.

## High-level instructions for coder
- Re-verify on dev stack (language picker + key locales) that feedback UI strings still localize; fix any regressions if found.
- If behaviour matches the issue: use **`gh`** (or human with **Issues** write) to comment on **#67** with verification summary, adjust labels (**`agent-planned`** / **`agent:wip`** / **`agent:testing`** as appropriate), and **close** the issue.
- If **`gh`** fails with token scope errors, document outcome in the task and hand off to a human with repo permissions (same pattern as prior CLOSED archives).

---

## Coder implementation (2026-03-24 UTC)

### Regression fixed
- **`front/public/i18n/de.json`** was **invalid JSON**: missing comma after `SETTINGS.RESERVATION_REMINDER_2H_HINT` (before `STRIPE_SECRET_HINT`). Browsers/ngx-translate could not parse the file, so **German never loaded** app-wide—including `FEEDBACK.*` on the public feedback page. Locales such as **es** still worked (separate valid JSON files).
- **Change:** Inserted the missing comma. Validated with `JSON.parse` on the full file.

### Verification (coder)
- **Puppeteer:** Open `http://127.0.0.1:4202/feedback/1`, select **Deutsch** in the language picker; `.feedback-intro` contains German `FEEDBACK.INTRO` (e.g. “Wir freuen uns…”).
- **Regression smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` → exit 0.
- **Docker:** `docker compose … logs --tail=40 front` — bundle generation complete, no TS errors after reload.

### GitHub housekeeping (blocked)
- **`gh issue close 67`** with comment failed: `GraphQL: Resource not accessible by personal access token (addComment)`.
- **Hand off:** A human with **Issues** write (or a token with `issues` scope) should paste the closing comment below on **#67**, adjust labels per `docs/agent-loop.md`, and close the issue.

**Suggested closing comment for #67:**

> Verification (2026-03-24, dev stack on :4202):
>
> - **Regression found and fixed:** `front/public/i18n/de.json` was **invalid JSON** (missing comma after `SETTINGS.RESERVATION_REMINDER_2H_HINT`). The loader could not parse German, so the public feedback form and other DE strings stayed in English. Other locales (e.g. es) still switched correctly.
> - **Fix:** Added the missing comma; file validates. Confirmed German `FEEDBACK.INTRO` on `/feedback/1` after choosing Deutsch.
> - **Smoke:** `npm run test:landing-version` with `BASE_URL=http://127.0.0.1:4202` passed.
>
> Closing as feedback localization works and German locale loads again.

---

## Testing instructions (tester)

1. **JSON:** From repo root, `node -e "JSON.parse(require('fs').readFileSync('front/public/i18n/de.json','utf8'))"` — must exit 0 (no throw).
2. **Public feedback DE:** With stack up, open `/feedback/1` (no login). Use language picker → **Deutsch**. Confirm form labels and intro match German copy (not English). Submit flow optional.
3. **Public feedback ES (spot check):** Switch to **Español**; confirm intro differs from English (regression guard).
4. **Smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit 0.
5. **GitHub:** If all pass, ensure **#67** is commented/closed by someone with token access (see **GitHub housekeeping** above).
