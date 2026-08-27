#!/usr/bin/env bash
set -e

cd /workspace

# One-time (or as-needed) project env setup: creates .venv from pyproject.toml.
if [ -f pyproject.toml ] && [ ! -d .venv ]; then
  uv sync || true
fi

exec "$@"
