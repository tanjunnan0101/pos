# Push to master

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/175

## Problem / goal
Promote tested work from **`development`** to **`master`** and deploy to production when appropriate. If deploying to amvara9, confirm the deployment pipeline succeeded (e.g. GitHub Actions or documented deploy script status).

## High-level instructions for coder / operator
- Follow **`.cursor/rules/git-development-branch-workflow.mdc`** and **`AGENTS.md`**: routine feature work stays on **`development`**; merge **`development` → `master`** only per team rules (~2-hour batch, production-urgent, or explicit production/hotfix request).
- Ensure **`development`** is green and reviewed for what should go live; reconcile with changelog/version policy if cutting a release.
- After promotion, verify deploy: **`scripts/deploy-amvara9.sh`** / server steps in **`docs/`** as applicable; check GitHub deployment or CI success for the environment referenced in the issue.
- Update the issue with what was merged and verification outcome (no secrets in comments).

## Implementation notes (feature coder)
- **2026-04-07 (UTC):** Fast-forward merged `origin/development` into `master` at **`00e7f62`** (`feat(tables): grouped list and tiles for joined groups, sibling activity warnings (#174)` and full `development` history to that tip). Pushed **`origin master`**.
- **Deploy:** GitHub Actions workflow **Deploy to amvara9** run **`24084369755`** completed **success** (~2m29s). Jobs **Deploy on amvara9** and **Smoke test (landing, version, API health)** passed.

## Testing instructions
- **What to verify:** `master` on GitHub matches the promoted tip; production deploy for that push succeeded; optional spot-check production URLs.
- **How to test:** `gh run view 24084369755 --repo satisfecho/pos` (expect **success**). Optional: `curl -s -o /dev/null -w "%{http_code}\n" https://satisfecho.de/` (expect **200**).
- **Pass/fail:** Pass if the workflow run is **success** and optional curl returns **200**. Fail if the run failed or production health checks fail.
