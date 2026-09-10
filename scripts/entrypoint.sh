#!/usr/bin/env bash
set -e

cd /workspace

# Keep opencode session data (SQLite DB: sessions, messages, todos, permissions)
# inside the project so it survives container recreation (root FS is disposable).
export OPENCODE_DB=/workspace/.opencode-data/opencode.db

# Restore opencode auth (bootstrapped from the host by scripts/up.sh).
if [ -f /workspace/.opencode-data/auth.json ]; then
  mkdir -p "$HOME/.local/share/opencode"
  cp /workspace/.opencode-data/auth.json "$HOME/.local/share/opencode/auth.json"
fi

# One-time (or as-needed) project env setup: creates .venv from pyproject.toml.
if [ -f pyproject.toml ] && [ ! -d .venv ]; then
  uv sync || true
fi

exec "$@"
