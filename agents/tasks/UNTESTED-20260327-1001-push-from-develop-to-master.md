# Push from develop to master

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/111

## Problem / goal

Promote tested work from **`development`** to **`master`** so production (p. ej. amvara9) can track the release branch. The issue text is minimal; interpret it as a **release / branch promotion** request, not as a product feature in `back/` or `front/` unless the assignee discovers blockers that require code.

See **`.cursor/rules/git-development-branch-workflow.mdc`** and **`AGENTS.md`**: merge **`development` → `master`** only when a promotion window applies (~2h batch, production-urgent, or explicit hotfix), then push **`origin master`** as appropriate.

## High-level instructions for coder

- Confirm **`development`** is synced with **`origin/development`** and that CI/smoke expectations for what is about to ship are met (or document known gaps in the issue).
- If promotion is allowed by team rules, perform **`development` → `master`** (fast-forward or merge per team habit), push **`origin master`**, and note commit range or tag in the GitHub issue.
- If promotion is **not** yet justified by policy, reply on the issue with **why** (which rule window is missing) and what remains (tests, sign-off, urgent label, etc.).
- Do **not** treat this as permission to bypass tenant/security rules or to ship untested breaking migrations without explicit production urgency.

## Implementation (feature coder 006, 2026-03-27 UTC)

- **Policy:** Promotion allowed because **GitHub #111** explicitly requests pushing **`development`** to **`master`** (explicit release / branch promotion), per **`git-development-branch-workflow.mdc`**.
- **Pre-sync:** `./scripts/git-sync-development.sh` — `development` matched **`origin/development`** at **`3a29d70`**.
- **Merge:** On **`master`**, merged **`origin/development`** with merge commit message *Merge branch 'development' for production promotion (GitHub #111)* → tip **`bad16c9`**.
- **Range:** prior **`origin/master`** was **`445888a`** (*Merge branch 'development' for release 2.0.61*); included product work through app version **2.0.64** on the branch (changelog/features accumulated on `development`, e.g. legal URLs #110, working-plan colors #109, contract templates #106, security/upload hardening, migrations under `back/migrations/`).
- **Push:** **`git push origin master`** completed successfully (`445888a..bad16c9`).
- **Branch alignment:** Local **`development`** fast-forwarded to **`bad16c9`** so it matches **`master`** after promotion (ready to **`git push origin development`** when this task commit lands).

## Testing instructions

1. **Git remote:** On any clone, `git fetch origin && git rev-parse origin/master` should equal **`bad16c9`** (or newer if further commits were pushed).
2. **Production / amvara9:** If production deploy tracks **`master`**, run the usual deploy (e.g. **`scripts/deploy-amvara9.sh`**) so the server pulls the new tip; confirm **`python -m app.migrate`** (and **`--sync-idempotent`** if used) completes without error — new SQL migrations were part of the promoted range.
3. **Smoke:** After deploy, `curl -s -o /dev/null -w "%{http_code}" https://satisfecho.de/` (or dev HAProxy port) returns **200**; optional: `BASE_URL=… npm run test:landing-version` from **`front/`** against the target environment.
4. **Known gaps:** Full CI/pytest/Puppeteer suite was not re-run in this step; prior tester closures on included features are documented under **`agents/tasks/done/`**. If anything fails post-deploy, open a follow-up issue or **NEW-** task rather than reverting **`master`** without team agreement.
