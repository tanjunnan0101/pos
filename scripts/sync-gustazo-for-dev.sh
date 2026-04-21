#!/usr/bin/env bash
# Back-compat: full marketing sync (all sites from manifest + discovery).
exec "$(cd "$(dirname "$0")" && pwd)/sync-all-marketing-sites.sh"
