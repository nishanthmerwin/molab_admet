#!/usr/bin/env bash
# Start a marimo server inside the container, reachable from your Mac's browser.
# Usage: ./scripts/marimo.sh [notebook.py]  (defaults to notebooks/tdi_dataset_explorer.py)
#
# Hot-reload setup:
#   - --watch            marimo reloads the notebook file itself on external edits
#   - ANYWIDGET_HMR=1    anywidget pushes .js/.css edits to open widgets live
#                        (src/openadmet_tdi/widgets/*), no cell re-run needed
#   - auto_reload=autorun (pyproject [tool.marimo.runtime]) re-imports changed
#                        Python modules and re-runs dependent cells automatically
set -euo pipefail
NB="${1:-notebooks/tdi_dataset_explorer.py}"
ARGS=(edit ${NB:+$NB} --host 0.0.0.0 --headless -p 2718 --watch)
container exec -it admet env ANYWIDGET_HMR=1 uv run marimo "${ARGS[@]}"
