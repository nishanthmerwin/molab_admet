#!/usr/bin/env bash
# Start a marimo server inside the container, reachable from your Mac's browser.
# Usage: ./scripts/marimo.sh [notebook.py]
set -euo pipefail
NB="${1:-}"
ARGS=(edit ${NB:+$NB} --host 0.0.0.0 --headless -p 2718)
container exec -it admet uv run marimo "${ARGS[@]}"
