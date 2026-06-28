#!/bin/sh
set -e

# Get API and WS URLs from environment variables, with defaults
API_URL="${API_URL:-http://localhost:8020}"
WS_URL="${WS_URL:-ws://localhost:8021}"

# Replace placeholders in index.html with actual values
# Use # as delimiter to avoid conflicts with URLs and || operator
# Escape special characters for sed (slashes, ampersands, etc.)
API_URL_ESCAPED=$(echo "$API_URL" | sed 's/[\/&]/\\&/g')
WS_URL_ESCAPED=$(echo "$WS_URL" | sed 's/[\/&]/\\&/g')

# Replace the default values in the JavaScript code
# Only replace if environment variables are explicitly set (not using relative URLs)
if [ -n "$API_URL" ] && [ "$API_URL" != "" ]; then
    sed -i "s#window.__API_URL__ || '[^']*'#window.__API_URL__ || '${API_URL_ESCAPED}'#g" /app/src/index.html
fi
if [ -n "$WS_URL" ] && [ "$WS_URL" != "" ]; then
    sed -i "s#window.__WS_URL__ || '[^']*'#window.__WS_URL__ || '${WS_URL_ESCAPED}'#g" /app/src/index.html
fi
# Sync version in commit-hash.ts from package.json (preserve existing git hash if .git is missing, e.g. Docker bind-mount of ./front only)
if [ -f /app/scripts/get-commit-hash.js ]; then
  node /app/scripts/get-commit-hash.js || true
fi

# Optional: populate front/sites/<slug>/ and front/marketing-flat/ (docker-compose.dev mounts ./scripts → /pos-scripts)
if [ -f /pos-scripts/sync-all-marketing-sites.sh ] && [ "${SYNC_MARKETING_ON_START:-${SYNC_GUSTAZO_ON_START:-1}}" != "0" ]; then
  /bin/bash /pos-scripts/sync-all-marketing-sites.sh || true
fi

# Execute the original command
exec "$@"
