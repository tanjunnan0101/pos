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
