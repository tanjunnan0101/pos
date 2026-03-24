# docker buildx prune

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/73

## Problem / goal
The amvara9 build pipeline should run **`docker buildx prune`** so temporary BuildKit/buildx layers do not accumulate in the Docker cache and fill disk.

## High-level instructions for coder
- Inspect **`scripts/deploy-amvara9.sh`** and any related deploy/CI docs (**`docs/`** e.g. amvara9 CD) to find the right place **after** image builds complete successfully.
- Add a non-interactive prune (e.g. **`docker buildx prune -f`**, with filters the team accepts) so SSH/deploy scripts never hang on prompts; document behaviour briefly if behaviour is non-obvious.
- Balance **disk recovery** vs **next-build cold-cache** cost; note in commit or doc if specific flags were chosen for retention.
- Ensure the step does not break concurrent builds on the same host if that is a realistic scenario.

## Coder notes (implementation)

- **`scripts/deploy-amvara9.sh`:** After successful **`docker compose build`** for **back** and **front**, runs **`docker buildx prune -f`** (unused BuildKit cache only; non-interactive). **`SKIP_BUILDX_PRUNE=1`** skips the step. Prune failure logs a warning and does not exit deploy (**`set -e`** avoided via `if`).
- **Retention:** No **`--filter until=`** — full unused-cache prune for maximum disk recovery on amvara9; production front build is already **`--no-cache`**, so deploy does not depend on warm BuildKit cache for the prior layer set.
- **Concurrency:** **`.github/workflows/deploy-amvara9.yml`** uses a **`deploy-amvara9`** concurrency group so CI deploys do not overlap on the server; prune only removes cache not referenced by active builds.
- **`docs/0001-ci-cd-amvara9.md`:** Deploy behaviour bullet documents prune, opt-out, and non-fatal failures.

## Testing instructions

### What to verify

- After both image builds, the script prints prune messages and **`docker buildx prune -f`** succeeds on a host with buildx, or emits a clear warning without aborting deploy if prune fails.
- **`SKIP_BUILDX_PRUNE=1`** skips pruning.

### How to test

- **Syntax:** From repo root: `bash -n scripts/deploy-amvara9.sh` (expect exit 0).
- **Dry behaviour (optional, on a machine with Docker):** Run only the build+prune segment by copying the two `docker compose … build` lines and the new prune block into a throwaway shell after **`cd`** to a checkout with **`config.env`**, or run a full deploy on a staging host if available.
- **Manual check:** Inspect **`scripts/deploy-amvara9.sh`** after the front build for the **`docker buildx prune -f`** block and header comment **`SKIP_BUILDX_PRUNE`**.

### Pass / fail criteria

- **Pass:** Script remains **`set -e`**-safe; prune runs after successful **back** + **front** builds; **`SKIP_BUILDX_PRUNE=1`** skips; doc in **`docs/0001-ci-cd-amvara9.md`** matches behaviour.
- **Fail:** Deploy aborts on prune failure without intentional design, or prune runs before builds complete.
