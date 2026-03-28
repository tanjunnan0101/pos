#!/usr/bin/env bash
# Optional pre-001 filter: local Ollama decides if Docker log heuristics are noise.
# Used when AGENT_001_OLLAMA_LOG_TRIAGE=1 in pos-agent-loop.sh (issues untouched).
#
# Usage: scripts/agent-ollama-log-triage.sh /path/to/001-latest-context.txt
# Env:   OLLAMA_MODEL (default qwen2.5:1.5b), OLLAMA_HOST if daemon is remote
#
# Exit: 0 = ESCALATE (keep log incident flag for 001)
#       1 = SKIP    (clear log flag; do not call cursor for logs-only triage)
#       2 = error   (ollama missing/failed; caller keeps heuristic flag)

set -euo pipefail

ctx="${1:?usage: $0 /path/to/001-latest-context.txt}"
model="${OLLAMA_MODEL:-qwen2.5:1.5b}"

if ! command -v ollama >/dev/null 2>&1; then
  echo "agent-ollama-log-triage: ollama not on PATH" >&2
  exit 2
fi

if [[ ! -f "$ctx" ]]; then
  echo "agent-ollama-log-triage: missing context file: $ctx" >&2
  exit 2
fi

body=$(sed -n '/=== Docker log incident/,/=== Preflight summary ===/p' "$ctx" | head -c 16000)
_body_compact=$(printf '%s' "$body" | tr -d ' \t\n\r')
if [[ -z "$_body_compact" ]]; then
  echo "agent-ollama-log-triage: no Docker section in context" >&2
  exit 2
fi
unset _body_compact

prompt="You triage devops log excerpts. Answer briefly. First decide, then one word on its own line: either ESCALATE or SKIP.

ESCALATE = a developer should file follow-up (standing error, repeating 5xx, build still broken, DB FATAL).
SKIP = transient (e.g. one-off TS then compile ok), noise, or clearly self-recovered.

Log excerpt:
${body}"

out=$(printf '%s' "$prompt" | ollama run "$model" 2>/dev/null | tr -d '\r' || true)
head_lines=$(printf '%s\n' "$out" | head -n 20)

if [[ -z "$head_lines" ]]; then
  echo "agent-ollama-log-triage: empty model output" >&2
  exit 2
fi

if printf '%s\n' "$head_lines" | grep -qiE '\bescalate\b'; then
  exit 0
fi
if printf '%s\n' "$head_lines" | grep -qiE '\bskip\b'; then
  exit 1
fi

echo "agent-ollama-log-triage: no ESCALATE/SKIP token in model reply, escalating" >&2
exit 0
