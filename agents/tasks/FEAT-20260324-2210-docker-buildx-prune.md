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
