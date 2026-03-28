# Bump Version

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/70
- **Related (same topic, dedupe — no separate FEAT-):** https://github.com/satisfecho/pos/issues/77

## Problem / goal

The reporter notes many unmerged commits on `development` and asks to bump the version and merge into `master`/`main`. Version and changelog live in this repo per `front/package.json` / `CHANGELOG.md` and team rules in `.cursor/rules/commit-changelog-version.mdc`. Promotion of `development` → `master` is governed by `.cursor/rules/git-development-branch-workflow.mdc` and `docs/agent-loop.md` (not every bump requires an immediate production merge unless criteria there are met).

## High-level instructions for coder

- Review `CHANGELOG.md` `[Unreleased]` and align with what would ship; cut a new `## [X.Y.Z] - YYYY-MM-DD` section when appropriate and bump `front/package.json` / `front/package-lock.json` per project convention.
- Confirm branch state: routine commits stay on `development`; merging to `master` only when the workflow allows (batch cadence, production-urgent, or explicit product request).
- If the issue author expects an immediate production release, capture that explicitly in the issue or verify with the maintainer before merging `master`.
- After changes, run the usual smoke checks from `AGENTS.md` / `docs/testing.md` for anything that touches the built app.

## Implementation (feature coder)

- **Release metadata:** Repo is already at **`2.0.64`** in `front/package.json` / lockfile with **`## [2.0.64] - 2026-03-27`** in `CHANGELOG.md`; further items remain under **`[Unreleased]`** for a future cut.
- **`commit-hash.ts`:** Regenerated with **`node front/scripts/get-commit-hash.js`** so footer semver/hash match the current checkout (avoids stale `version` in the landing bar after a bump).
- **`test:landing-version`:** On **localhost** (`127.0.0.1` / `localhost` / `::1`), the first semver in the landing footer must equal **`front/package.json`** `version`. Mismatch fails fast (with hint to run `get-commit-hash.js`). Remote `BASE_URL` unchanged unless `SKIP_LANDING_PACKAGE_VERSION_CHECK=1`.
- **No `development` → `master` merge** in this task: promotion follows `.cursor/rules/git-development-branch-workflow.mdc`.

## Testing instructions

- **What to verify:** Landing footer semver matches **`front/package.json`** on localhost; `commit-hash.ts` updated when regenerating; Puppeteer smoke still passes.
- **How to test:**
  1. `grep '"version"' front/package.json` — note version (e.g. **2.0.64**).
  2. From repo root: `node front/scripts/get-commit-hash.js` — should write `front/src/environments/commit-hash.ts` with the same `version` and current short git hash when `.git` is available.
  3. With stack up (`docker-compose.yml` + `docker-compose.dev.yml`, HAProxy e.g. **4202**):  
     `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit **0**; log line `Version element text:` must start with the package version.
  4. Optional: `npm run test:changelog --prefix front` — changelog modal still loads.
  5. Against a **remote** host with a different deployed version:  
     `SKIP_LANDING_PACKAGE_VERSION_CHECK=1 BASE_URL=https://… npm run test:landing-version --prefix front`
- **Pass/fail:** Step 3 exit **0** and footer semver equals package.json on localhost; step 2 produces consistent `commit-hash.ts`; step 4 optional **0** or skip.

## Coder completion notes (2026-03-28 UTC)

- Regenerated `commit-hash.ts` (version **2.0.64**, hash **7c920cd** at time of run).
- `test:landing-version` extended with localhost package-version assertion; full smoke run passed against **4202**.
