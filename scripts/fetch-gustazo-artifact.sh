#!/usr/bin/env bash
# Back-compat wrapper: downloads 040_gustazo artifact into front/sites/gustazo/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export POS_REPO_ROOT="${POS_REPO_ROOT:-$ROOT}"
export TARGET_DIR="${TARGET_DIR:-front/sites/gustazo}"
export MARKETING_REPO="${GUSTAZO_REPO:-sakario/040_gustazo}"
export MARKETING_BRANCH="${GUSTAZO_BRANCH:-development}"
export MARKETING_ARTIFACT_NAME="${GUSTAZO_ARTIFACT_NAME:-dist}"
exec bash "$(dirname "$0")/fetch-marketing-artifact.sh"
