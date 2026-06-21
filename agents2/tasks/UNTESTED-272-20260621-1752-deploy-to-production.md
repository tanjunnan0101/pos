# Deploy to production

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/272
- **272**

## Problem / goal

Promote tested work from **`development`** to **`master`** and deploy to **amvara9** (production / **satisfecho.de**). The issue author requests shipping the latest changes to production.

Follow **`.cursor/rules/git-development-branch-workflow.mdc`** — this is an explicit production-promotion request (issue opened 2026-06-21).

**Context (2026-06-21):** After sync, **`origin/development`** is ahead of **`origin/master`** (last **`master`** tip **`632de10d`**, 2026-06-17). Notable product commits on **`development`** not yet on **`master`** include **#271** (schedule write authorization for non-owner staff), **#270** (courier role / delivery driver portal), and **#269** (pricing helper garnish costs). Local dev stack responds **200** on port 4202; no Angular compile errors in **`pos-front`** logs in the last 7 days.

## High-level instructions for coder

- Confirm **`development`** is green locally: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4202/` → 200; run relevant Puppeteer smoke tests for recently merged features (#269 pricing helper, #270 courier portal, #271 schedule auth) if credentials are available.
- Review **`CHANGELOG.md`** / version in **`front/package.json`** — bump and release notes if user-visible changes warrant it (see **`.cursor/rules/commit-changelog-version.mdc`**).
- Merge **`development` → `master`** (merge commit or team-preferred fast-forward), push **`origin/master`**.
- Watch **Deploy to amvara9** GitHub Actions for the pushed **`master`** commit; document run URL and conclusion in the task file.
- Verify production: `curl -sf https://www.satisfecho.de/api/health`; optional `LANDING_VERSION_ONLY=1 BASE_URL=https://www.satisfecho.de npm run test:landing-version` from `front/`.
- If deploy fails, check Actions logs and **`docs/0001-ci-cd-amvara9.md`** (migrations, dirty tree, marketing artifacts) before retrying.
- Append **Testing instructions** when ready for tester; follow **wip → untested** flow per **`TASKS-README.md`**.

## Coder notes (2026-06-21)

- **Pre-deploy local:** `curl` → **200** on `http://127.0.0.1:4202/`. Landing Puppeteer with `.env` credentials failed login (401) — local DB credentials may differ; version footer showed **2.1.5** before deploy.
- **Changelog:** Cut **`## [2.1.5] - 2026-06-21`** with #269, #270, #271 and release note (#272).
- **Merge:** Fast-forward **`development` → `master`** at **`7405465c`**; pushed **`origin/master`** and **`origin/development`**.
- **Deploy:** **Deploy to amvara9** run **success** — https://github.com/satisfecho/pos/actions/runs/27912680055 (3m21s, push on `master`).
- **Production verify:** `curl -sf https://www.satisfecho.de/api/health` → `{"status":"ok"}`. Landing test `LANDING_VERSION_ONLY=1 BASE_URL=https://www.satisfecho.de` → **2.1.5 7405465c**.

## Testing instructions

1. **Production health:** `curl -sf https://www.satisfecho.de/api/health` → `{"status":"ok"}`.
2. **Landing version:** From `front/`, `LANDING_VERSION_ONLY=1 BASE_URL=https://www.satisfecho.de npm run test:landing-version` → footer shows **2.1.5** and commit **`7405465c`**.
3. **Pricing helper (#269):** Log in as owner/admin → **Products → Pricing helper** → confirm **Garnishes** section with ice/lemon/other costs; verify pour-cost math includes garnish amounts.
4. **Courier portal (#270):** In **Users**, assign **Courier** role to a test user → sign in at **`/courier/login`** → lands on **`/courier`** placeholder; staff routes blocked for courier; courier routes blocked for staff.
5. **Schedule auth (#271):** Log in as staff with `schedule:write` (not owner/admin) → **Working plan** → can edit own shifts only; API returns 403 for other users' shifts; edit/delete hidden for others' rows in UI.
6. **Regression:** `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4202/` → **200** on local dev if stack is up.
