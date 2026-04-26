# Push to Master

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/195
- **195**

## Problem / goal
Promote tested work from **`development`** to **`master`** so production (e.g. **amvara9**) can run current code. After deploy, confirm the **GitHub Actions** deployment workflow completed successfully (per issue text).

Follow repo branching rules: routine promotion timing vs urgent production fixes — see **`.cursor/rules/git-development-branch-workflow.mdc`**.

## High-level instructions for coder
- Confirm **`development`** is synced with **`origin/development`** and reflects the intended release scope (no accidental WIP).
- Merge **`development` → `master`** only when allowed by team rules (cadence, production-impacting trigger, or explicit urgent/production request on the issue). Align with **`docs/agent-loop.md`**.
- Push **`master`** to **`origin`** when merging for production.
- Deploy to **amvara9** using the documented path (see **`docs/0001-ci-cd-amvara9.md`**, **`scripts/deploy-amvara9.sh`** as referenced in **`README.md`** / **`AGENTS.md`**).
- For “review the success status of the deployment action on GitHub”: open the repo’s **Actions** tab for the relevant workflow run and verify success; capture any failure logs for follow-up without pasting secrets.
- Post a short summary on the issue when promotion/deploy is done (what was merged, whether CI/deploy is green).

## Implementation summary (feature coder)
- **`development`** was synced with **`origin/development`** (already up to date).
- **`master`** was fast-forwarded to **`7a2c2bd`** (same tip as **`development`** after promotion) and pushed to **`origin/master`** (issue explicitly requested production promotion).
- **GitHub Actions — Deploy to amvara9** run **`24773000757`** (triggered by **`master`** push) **failed** at step **Fetch marketing site artifacts**: sync script reported **no `MARKETING_ARTIFACT_TOKEN` / `GH_TOKEN`** in that job’s environment, could not download marketing bundles, and **`MARKETING_VERIFY_NO_PLACEHOLDERS=1`** failed with placeholder bundles for slugs **antillana**, **dilruba**, **flamanapolitana**, **gustazo**, **hakone**. Server deploy steps did not run.
- **Follow-up (repo settings):** ensure Actions secrets include a PAT with **Actions read** on every repo listed in **`config/marketing-sites.json`** (see error text in workflow logs), then re-run the failed workflow or redeploy.

## Previous verification (2026-04-26) — FAIL (for context)

1. **Date/time (UTC) and log window**  
   - 2026-04-26T (approximately) single verification pass; `gh run view` / `git` commands run on host (no `docker logs` for this task — no local stack test required in instructions).

2. **Environment**  
   - **Branch:** local `development` synced (already up to date with `origin/development` before edits).  
   - **Remotes:** `git fetch origin` from `/Users/raro42/projects/pos2`.  
   - **`BASE_URL` / browser:** N/A — no optional live check (deploy not green).  
   - **Evidence:** `gh` CLI to `satisfecho/pos` Actions (authenticated).

3. **What was tested (from Testing instructions)**  
   - (1) `origin/master` vs `origin/development` with `rev-parse`  
   - (2) GitHub Actions run `24773000757` and latest `Deploy to amvara9` on `master`  
   - (3) Optional `https://satisfecho.de/` — **skipped** (no green deploy)  
   - (4) Manual server deploy — not executed

4. **Results**

   | Criterion | Result | Evidence |
   |---|---|---|
   | 1. Git: refs aligned | **FAIL** | `git rev-parse origin/master origin/development` → `7a2c2bd59b2cfb6cbc6a55ac407993494b17256f` then `c609795496451ac7ec1b095dc5b7620f51d5dfc8` (two different SHAs). `7a2c2bd` is an ancestor of `c6097954` on `development`; `origin/master` is still the promoted commit `7a2c2bd` while `origin/development` has advanced (e.g. follow-up work after promotion). |
   | 2. GitHub Actions: deploy green for relevant run | **FAIL** | `gh run view 24773000757 --repo satisfecho/pos` → run **X failed** at **Fetch marketing site artifacts**; subsequent jobs (SSH, stack, smoke) **not run**. `gh run list --workflow "Deploy to amvara9" --limit 5` on `master`: latest push deploy is still the failed `24773000757` (2026-04-22); no newer **success** after that for `master` deploy. |
   | 3. Optional production URL / health after green | **N/A** | No green deploy; optional step not applicable. |
   | 4. Manual fallback on server | **N/A** | Not run (out of scope for this verification pass). |

5. **Overall: FAIL**  
   - Failed: strict branch-tip match for instruction (1), and (2) deployment pipeline not successful — marketing artifact token/placeholder problem unchanged in recorded run. **Follow-up:** add/configure `MARKETING_ARTIFACT_TOKEN` / `GH_TOKEN` in repo Actions secrets and re-run deploy (per implementation summary and workflow log); then re-test.

6. **Product owner feedback**  
   The merge to `master` at `7a2c2bd` is present on the remote, but `development` has since moved forward and the automated amvara9 deploy for that `master` push is still **red** in Actions (marketing bundles), so end-to-end “promote and deploy successfully” is not verified. Operators should treat production as not updated by that **green** pipeline until a successful workflow run is observed.

7. **URLs tested**  
   1. `https://github.com/satisfecho/pos/actions/runs/24773000757` (run metadata and status)  
   - **N/A** — no full browser product URLs (optional prod check skipped).

8. **Relevant log excerpts (CI — failed step)**  
   - From `gh run view 24773000757 --log-failed` (truncated):  
   - `MARKETING_ARTIFACT_TOKEN:` and `GH_TOKEN:` empty; `[marketing-sync] no token` for antillana, dilruba, flamanapolitana, gustazo, hakone; `::error::placeholder still present for slug=...`; `Process completed with exit code 1`.

## Testing instructions

1. **Git:** Confirm **`origin/master`** and **`origin/development`** are at the expected points for the promotion under test (e.g. after a new merge, re-check tips):  
   `git fetch origin && git rev-parse origin/master origin/development`
2. **GitHub Actions:** Open **Actions** → **Deploy to amvara9** → run **`24773000757`** (or latest **`master`** deploy). After secrets are fixed, either **Re-run failed jobs** or trigger a new deploy from **`master`** and expect **green** through **Fetch marketing site artifacts**, **Set up SSH**, **Build and restart stack on amvara9**, **Smoke test**.
3. **Optional live check:** After a **green** deploy, verify **`https://satisfecho.de/`** (or documented prod URL) and API health per **`docs/0001-ci-cd-amvara9.md`** / smoke step output.
4. **Manual fallback:** If CI cannot be fixed immediately, an operator may run **`scripts/deploy-amvara9.sh`** from the server checkout per **`README.md`** / **`AGENTS.md`** (still needs marketing bundles resolved for full parity with CI).

## Test report

1. **Date/time (UTC) and log window**  
   - **Verification:** 2026-04-26T16:32Z–16:38Z (approx.).  
   - **Evidence:** `git` / `gh` / `curl` on host; CI failed-step logs via `gh run view 24773000757 --log-failed` (not `docker logs` — task scope is git + GitHub deploy).

2. **Environment**  
   - **Branch:** `development` synced (already up to date with `origin/development` at run start, per `./scripts/git-sync-development.sh`).  
   - **Remotes (after `git fetch origin`):** `origin/master` = `7a2c2bd59b2cfb6cbc6a55ac407993494b17256f`, `origin/development` = `e3da5729b85529de0de417d17543ee65c899e1c7`.  
   - **Compose / local app:** N/A (not in Testing instructions for this task).

3. **What was tested (from “What to verify” / Testing instructions)**  
   - (1) `git rev-parse` for both remotes; whether lineage matches expected post-promotion state.  
   - (2) GitHub Actions **Deploy to amvara9** for latest **`master`** deploy (run **24773000757** and list for newer).  
   - (3) Optional: prod URLs after green — N/A to strict pass/fail (deploy not green); sanity **curl** to `https://satisfecho.de/api/health` and `/` for context.  
   - (4) Manual server deploy — N/A (not run).

4. **Results**

   | Criterion | Result | Evidence line |
   |---|---|---|
   | 1. Git: refs / lineage | **PASS** | `git rev-parse origin/master origin/development` (SHAs above); `git merge-base --is-ancestor origin/master origin/development` → exit **0** (all commits on `origin/master` are in `origin/development`’s history — expected after a promotion, with `development` having advanced). |
   | 2. GitHub Actions: deploy **green** for latest **`master`** deploy | **FAIL** | `gh run list --workflow "Deploy to amvara9" --limit 8`: latest on **`master`** is **24773000757** (2026-04-22T10:18:20Z) **failure**. `gh run view 24773000757` → **X** at **Fetch marketing site artifacts (curl + GitHub API)**; **Set up SSH** through **Smoke test** not run. No newer **success** on `master` after 24710137656 / 24773000757 in this list. |
   | 3. Optional live check after **green** | **N/A** | No green master deploy; optional step not applicable. |
   | 4. Manual fallback | **N/A** | Not run. |
   | Sanity (not replacing (2)) | **INFO** | `curl` → `https://satisfecho.de/api/health` **200**, `https://satisfecho.de/` **200**; does not prove a successful 24773000757 pipeline. |

5. **Overall: FAIL**  
   - Fails criterion **2** — automated amvara9 deploy for the **master** push in scope is not green (marketing token / placeholder bundles, unchanged from prior report). Criterion **1** passes. **Next:** add/configure **`MARKETING_ARTIFACT_TOKEN` / `GH_TOKEN`** in repo Actions (PAT with Actions read on all repos in **`config/marketing-sites.json`**) and **re-run** failed jobs or push a new **`master` deploy; then re-test per Testing instructions (optional prod check after green).

6. **Product owner feedback**  
   Production URLs respond with HTTP 200, but the **Deploy to amvara9** run tied to the **`master` push in question** still fails in CI before any SSH or smoke steps. Until a workflow run is **success** through marketing fetch and smoke, the issue’s “confirm deployment action succeeded on GitHub” is **not** satisfied. Operators must fix the secret/PAT and get a **green** run; branch lineage alone is not enough to close the loop.

7. **URLs tested (numbered list)**  
   1. `https://github.com/satisfecho/pos/actions/runs/24773000757` (run view / status)  
   2. `https://satisfecho.de/api/health` (200 — sanity)  
   3. `https://satisfecho.de/` (200 — sanity)

8. **Relevant log excerpts (last section — CI, failed step)**  
   - From `gh run view 24773000757 --log-failed` (excerpt):  
   - `MARKETING_ARTIFACT_TOKEN:` and `GH_TOKEN:` empty.  
   - `[marketing-sync] no token` / skip (antillana, dilruba, flamanapolitana, gustazo, hakone).  
   - `::error::placeholder still for slug=...` (missing artifact or PAT scope; token with Actions read on every repo in `config/marketing-sites.json`).  
   - `##[error]Process completed with exit code 1.`
