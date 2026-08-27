#!/usr/bin/env bash
# Stop and remove the sandbox container. /workspace contents (on host) are kept.
set -euo pipefail
container stop admet 2>/dev/null || true
container rm admet 2>/dev/null || true
