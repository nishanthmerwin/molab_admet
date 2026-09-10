#!/usr/bin/env bash
# Start (or restart) the long-lived sandbox container.
#
# - Project code lives HERE (bind-mounted at /workspace), so it survives
#   container recreation.
# - Python deps are managed by uv INSIDE /workspace/.venv at runtime:
#   `uv add <pkg>` never needs a rebuild.
# - API keys pass through from your host env if set (use export_env.example).
set -euo pipefail
cd "$(dirname "$0")/.."

NAME=admet

# Bootstrap opencode auth so it survives container recreation (reads host
# auth.json into the gitignored .opencode-data/, which entrypoint.sh copies
# into place inside the container at startup).
mkdir -p .opencode-data
if [ -f "$HOME/.local/share/opencode/auth.json" ]; then
  cp "$HOME/.local/share/opencode/auth.json" .opencode-data/auth.json
fi

if container ls | grep -q "$NAME"; then
  echo "Container '$NAME' already running. Use scripts/down.sh first to recreate."
  exit 1
fi

container run \
  --name "$NAME" \
  -d \
  -c 6 \
  -m 18g \
  -v "$(pwd)":/workspace \
  -p 2718:2718 \
  --ssh \
  -e ANTHROPIC_API_KEY \
  -e OPENAI_API_KEY \
  -e OPENROUTER_API_KEY \
  -e GEMINI_API_KEY \
  -e GITHUB_TOKEN \
  admet-sandbox:latest

echo "Started. Enter with: ./scripts/shell.sh"
