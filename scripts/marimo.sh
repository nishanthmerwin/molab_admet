#!/usr/bin/env bash
# Start a marimo server inside the container, reachable from your Mac's browser.
# Usage: ./scripts/marimo.sh [notebook.py]  (defaults to notebooks/tdi_investigator.py)
set -euo pipefail
NB="${1:-notebooks/tdi_investigator.py}"
ARGS=(edit ${NB:+$NB} --host 0.0.0.0 --headless -p 2718 --watch)
container exec -it admet uv run marimo "${ARGS[@]}"
