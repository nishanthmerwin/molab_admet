#!/usr/bin/env bash
# Build the sandbox image.
set -euo pipefail
cd "$(dirname "$0")/.."
container build -t admet-sandbox:latest .
