#!/usr/bin/env bash
# Populate front/gustazo for local dev: (1) latest CI artifact if token set, else (2) ng build from a Gustazo checkout.
# Intended for pos-front Docker entrypoint and optional host runs from repo root.
#
# Env (see config.env.example):
#   GUSTAZO_ARTIFACT_TOKEN / GH_TOKEN — PAT with Actions read on satisfecho/040_gustazo (artifact download)
#   GUSTAZO_LOCAL_REPO — path to 040_gustazo clone (container: e.g. /gustazo-src from a bind mount)
#   SYNC_GUSTAZO_ON_START — default 1; set 0 to disable
#   GUSTAZO_REFRESH_EVERY_START — default 0; set 1 to always re-fetch/re-build (skip placeholder shortcut)
#   GUSTAZO_SYNC_FORCE — default 0; set 1 same as refresh for this run
#   GUSTAZO_NG_CONFIGURATION — passed to ng build (default production)

set -euo pipefail

ROOT="${POS_REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
TARGET="$ROOT/front/gustazo"
PLACEHOLDER_SIG='bundle not loaded'

log() { echo "[gustazo-sync] $*"; }

if [[ "${SYNC_GUSTAZO_ON_START:-1}" != "1" ]]; then
  log "SYNC_GUSTAZO_ON_START is not 1 — skipping."
  exit 0
fi

needs_sync() {
  if [[ "${GUSTAZO_SYNC_FORCE:-0}" == "1" ]] || [[ "${GUSTAZO_REFRESH_EVERY_START:-0}" == "1" ]]; then
    return 0
  fi
  if [[ ! -f "${TARGET}/index.html" ]]; then
    return 0
  fi
  if grep -q "${PLACEHOLDER_SIG}" "${TARGET}/index.html" 2>/dev/null; then
    return 0
  fi
  log "Existing Gustazo bundle (non-placeholder). Set GUSTAZO_REFRESH_EVERY_START=1 or GUSTAZO_SYNC_FORCE=1 to replace."
  return 1
}

if ! needs_sync; then
  exit 0
fi

TOKEN="${GUSTAZO_ARTIFACT_TOKEN:-${GH_TOKEN:-}}"
if [[ -n "$TOKEN" ]]; then
  export GH_TOKEN="$TOKEN"
  if bash "$ROOT/scripts/fetch-gustazo-artifact.sh"; then
    log "Installed from GitHub Actions artifact."
    exit 0
  fi
  log "Artifact download failed — trying local Gustazo build if configured."
fi

resolve_local() {
  if [[ -n "${GUSTAZO_LOCAL_REPO:-}" ]] && [[ -d "${GUSTAZO_LOCAL_REPO}" ]]; then
    echo "${GUSTAZO_LOCAL_REPO}"
    return 0
  fi
  if [[ -d "/gustazo-src" ]] && [[ -f "/gustazo-src/package.json" ]]; then
    echo "/gustazo-src"
    return 0
  fi
  local sibling="${ROOT}/../040_gustazo"
  if [[ -d "$sibling" ]] && [[ -f "$sibling/package.json" ]]; then
    echo "$sibling"
    return 0
  fi
  echo ""
}

LOCAL="$(resolve_local)"
if [[ -z "$LOCAL" ]]; then
  log "No token (or fetch failed) and no local repo — leaving placeholder under ${TARGET}."
  exit 0
fi

log "Building Gustazo from ${LOCAL} ..."
WORK="$(mktemp -d)"
cleanup() { rm -rf "${WORK}"; }
trap cleanup EXIT
cp -a "${LOCAL}/." "${WORK}/"
cd "${WORK}"

if [[ ! -f package.json ]]; then
  log "No package.json in ${LOCAL}"
  exit 0
fi

npm ci --ignore-scripts
CFG="${GUSTAZO_NG_CONFIGURATION:-production}"
set +e
npx ng build --configuration "${CFG}" --base-href /gustazo/
BUILD_OK=$?
set -e
if [[ "${BUILD_OK}" -ne 0 ]]; then
  log "ng build failed (configuration=${CFG}). Set GUSTAZO_NG_CONFIGURATION if needed."
  exit 0
fi

BROWSER="$(find "${WORK}/dist" -type d -name browser 2>/dev/null | head -1)"
if [[ -z "${BROWSER}" ]] || [[ ! -f "${BROWSER}/index.html" ]]; then
  log "No dist/.../browser after build — check Gustazo output layout."
  exit 0
fi

mkdir -p "${TARGET}"
find "${TARGET}" -mindepth 1 -maxdepth 1 ! -name 'gitkeep.txt' -exec rm -rf {} +
cp -a "${BROWSER}/." "${TARGET}/"
log "Installed from local build (${BROWSER})."
exit 0
