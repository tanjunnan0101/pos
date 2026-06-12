# Remove diagnostics zip from repository

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/267
- **267**

## Problem / goal

Remove **`diagnostics_20260408_4.zip`** from the repository. The file is tracked at the repo root (~171 KB), appears to be a one-off diagnostics dump, and should not live in version control.

## High-level instructions for coder

- Delete **`diagnostics_20260408_4.zip`** from the repo root and commit the removal on **`development`**.
- Confirm nothing in the codebase references this filename (grep the repo).
- Optionally add a **`.gitignore`** rule for `diagnostics_*.zip` (or similar) if diagnostics archives are generated locally and must not be re-committed — only if consistent with existing ignore patterns.
- Do **not** remove unrelated files; scope is this zip only.
- Append **Testing instructions** when ready; follow **wip → untested** per **`agents2/TASKS-README.md`**.

## Implementation notes

- Deleted **`diagnostics_20260408_4.zip`** from repo root.
- Grep across the repo: no code, docs, or config references to this filename (only this task file).
- Added **`diagnostics_*.zip`** to **`.gitignore`** (alongside other local scratch patterns like **`tmp/*`**) to prevent accidental re-commit of future diagnostics archives.

## Testing instructions

1. **File removed:** From repo root, confirm the zip is gone:
   ```bash
   test ! -f diagnostics_20260408_4.zip && echo OK
   ```
2. **Git no longer tracks it:** After commit, `git ls-files | grep diagnostics` should return nothing.
3. **No references:** `rg -i 'diagnostics_20260408_4|diagnostics_.*\.zip' --glob '!agents2/tasks/*'` should find only **`.gitignore`** (the ignore rule), not product code or docs.
4. **Ignore rule:** Create a dummy `diagnostics_test.zip` at repo root; `git status` should not list it as untracked. Remove the dummy file afterward.
5. **Smoke:** No app/runtime impact expected; optional `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4202/` should still return **200** if the stack is up.

## Test report

1. **Date/time (UTC):** Start 2026-06-11 09:02:00 UTC — End 2026-06-11 09:03:15 UTC. Log window: N/A (no container log review required for this repo-hygiene change).

2. **Environment:** Branch `development` @ `db8bf224`; local Docker dev stack; `BASE_URL=http://127.0.0.1:4202`; compose files `docker-compose.yml` + `docker-compose.dev.yml`.

3. **What was tested:** File removal, git tracking, reference grep, `.gitignore` rule for `diagnostics_*.zip`, optional landing smoke.

4. **Results:**
   - **File removed:** **PASS** — `test ! -f diagnostics_20260408_4.zip && echo OK` → `OK: file removed`.
   - **Git no longer tracks it:** **FAIL** — `git ls-files | grep diagnostics` still returns `diagnostics_20260408_4.zip`. Working tree shows `deleted: diagnostics_20260408_4.zip` and `modified: .gitignore` with **no commit** on `development`.
   - **No references:** **PASS** — `rg` (excluding `agents2/tasks/*`) finds only `.gitignore` line `diagnostics_*.zip`; no product code or docs references.
   - **Ignore rule:** **PASS** — Created `diagnostics_test.zip`; `git status --porcelain diagnostics_test.zip` empty; dummy removed.
   - **Smoke:** **PASS** — `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4202/` → `200`.

5. **Overall:** **FAIL** — Git still tracks the zip until deletion and `.gitignore` are committed on `development` (criterion 2).

6. **Product owner feedback:** The filesystem cleanup and ignore rule are correct, but the repository still lists the zip in the index. The coder should stage and commit the deletion plus `.gitignore` on `development`, then return the task to **UNTESTED-** for re-verification.

7. **URLs tested:** N/A — no browser (optional curl smoke only).

8. **Relevant log excerpts:** N/A — repo/git checks only; no container logs collected.
