#!/usr/bin/env bash
# Download the latest successful GitHub Actions artifact from satisfecho/040_gustazo (or GUSTAZO_REPO)
# into front/gustazo/ for embedding in the production nginx image. Uses curl + jq only (no third-party Actions).
#
# Required when not skipping: GH_TOKEN with permission to read Actions artifacts on the Gustazo repo
# (fine-grained PAT: Actions: Read + Contents: Read on 040_gustazo).
#
# Env:
#   GH_TOKEN                    — PAT (set GUSTAZO_ARTIFACT_TOKEN in CI → GH_TOKEN in step)
#   GUSTAZO_REPO                — default satisfecho/040_gustazo
#   GUSTAZO_BRANCH              — branch to take latest successful run from (default: development)
#   GUSTAZO_ARTIFACT_NAME       — artifact name from Gustazo workflow (default: dist)
#   GUSTAZO_SKIP=1              — skip download (leave front/gustazo as in checkout; gitkeep.txt placeholder)
#   TARGET_DIR                  — default front/gustazo (relative to repo root)

set -euo pipefail

ROOT="${POS_REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$ROOT"

TARGET_DIR="${TARGET_DIR:-front/gustazo}"
REPO="${GUSTAZO_REPO:-satisfecho/040_gustazo}"
BRANCH="${GUSTAZO_BRANCH:-development}"
[[ -n "$BRANCH" ]] || BRANCH="development"
ARTIFACT_NAME="${GUSTAZO_ARTIFACT_NAME:-dist}"
[[ -n "$ARTIFACT_NAME" ]] || ARTIFACT_NAME="dist"
TOKEN="${GH_TOKEN:-}"

if [[ "${GUSTAZO_SKIP:-0}" == "1" ]]; then
  echo "GUSTAZO_SKIP=1: skipping Gustazo artifact fetch."
  exit 0
fi

if [[ -z "$TOKEN" ]]; then
  echo "::warning::GH_TOKEN not set — skipping Gustazo artifact fetch (/gustazo may be empty until configured)."
  exit 0
fi

API="https://api.github.com"
AUTH_HDR=(-H "Authorization: Bearer ${TOKEN}" -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28")

echo "Fetching latest successful Actions run for ${REPO} branch=${BRANCH}..."
RUNS_JSON="$(curl -sf "${AUTH_HDR[@]}" "${API}/repos/${REPO}/actions/runs?branch=${BRANCH}&status=completed&per_page=20")" || {
  echo "::error::GitHub API request failed (runs list). Check token and repo access."
  exit 1
}

RUN_ID="$(echo "$RUNS_JSON" | jq -r '.workflow_runs[] | select(.conclusion == "success") | .id' | head -1)"
if [[ -z "$RUN_ID" || "$RUN_ID" == "null" ]]; then
  echo "::error::No successful workflow run found for ${REPO}@${BRANCH}."
  exit 1
fi
echo "Using workflow run id=${RUN_ID}"

echo "Listing artifacts..."
ARTIFACTS_JSON="$(curl -sf "${AUTH_HDR[@]}" "${API}/repos/${REPO}/actions/runs/${RUN_ID}/artifacts")" || {
  echo "::error::GitHub API request failed (artifacts list)."
  exit 1
}

ZIP_URL="$(echo "$ARTIFACTS_JSON" | jq -r --arg name "$ARTIFACT_NAME" '.artifacts[] | select(.name == $name) | .archive_download_url' | head -1)"
if [[ -z "$ZIP_URL" || "$ZIP_URL" == "null" ]]; then
  NAMES="$(echo "$ARTIFACTS_JSON" | jq -r '.artifacts[].name' | paste -sd, -)"
  echo "::error::No artifact named '${ARTIFACT_NAME}'. Available: ${NAMES:-none}"
  exit 1
fi

TMP_ZIP="$(mktemp)"
TMP_EX="$(mktemp -d)"
cleanup() { rm -f "$TMP_ZIP"; rm -rf "$TMP_EX"; }
trap cleanup EXIT

echo "Downloading artifact zip..."
curl -sfL "${AUTH_HDR[@]}" -o "$TMP_ZIP" "$ZIP_URL" || {
  echo "::error::Artifact download failed."
  exit 1
}

mkdir -p "$TMP_EX"
unzip -q -o "$TMP_ZIP" -d "$TMP_EX"

# Normalize extracted layout into TARGET_DIR (keep tracked placeholder gitkeep.txt if present)
mkdir -p "${TARGET_DIR}"
find "${TARGET_DIR}" -mindepth 1 -maxdepth 1 ! -name 'gitkeep.txt' -exec rm -rf {} +

shopt -s dotglob nullglob
TOP=( "$TMP_EX"/* )
if [[ ${#TOP[@]} -eq 1 && -d "${TOP[0]}" ]]; then
  mv "${TOP[0]}"/* "${TARGET_DIR}/" 2>/dev/null || true
else
  mv "$TMP_EX"/* "${TARGET_DIR}/" 2>/dev/null || true
fi
shopt -u dotglob nullglob

# Angular often uploads dist/.../browser — hoist browser/ if index.html not at root yet
if [[ -d "${TARGET_DIR}/browser" && ! -f "${TARGET_DIR}/index.html" ]]; then
  echo "Hoisting browser/ contents to ${TARGET_DIR}/"
  mv "${TARGET_DIR}/browser"/* "${TARGET_DIR}/" || true
  rmdir "${TARGET_DIR}/browser" 2>/dev/null || true
fi

if [[ ! -f "${TARGET_DIR}/index.html" ]]; then
  echo "::warning::No index.html under ${TARGET_DIR} after extract — check Gustazo artifact layout and GUSTAZO_ARTIFACT_NAME."
fi

echo "Gustazo static files ready under ${TARGET_DIR} ($(find "${TARGET_DIR}" -type f | wc -l | tr -d ' ') files)."
exit 0
