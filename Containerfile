FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates ripgrep procps less unzip openssh-client \
    && rm -rf /var/lib/apt/lists/*

# GitHub CLI
RUN curl -fsSL https://github.com/cli/cli/releases/download/v2.83.1/gh_2.83.1_linux_arm64.tar.gz \
    | tar -xz -C /opt && mv /opt/gh_2.83.1_linux_arm64/bin/gh /usr/local/bin/gh

# uv (project deps are added at runtime with `uv add`, never require a rebuild)
RUN pip install --no-cache-dir uv

# marimo + optional deps it likes to have
RUN pip install --no-cache-dir "marimo[recommended]" ruff

# OpenCode agent CLI
RUN curl -fsSL https://opencode.ai/install | bash

WORKDIR /workspace
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"]
