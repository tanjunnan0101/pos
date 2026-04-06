#!/usr/bin/env bash
# POS pi loop — same as pi-agent-loop.sh (GitHub issues + tasks).
# Run from repo root: ./agents/pi-pos-loop.sh [COMMAND]
set -euo pipefail
SCRIPTDIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPTDIR/pi-agent-loop.sh" "$@"
