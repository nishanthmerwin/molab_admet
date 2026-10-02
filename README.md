# molab_admet

Sandboxed Linux dev environment for agentic marimo notebook development, running
via [apple/container](https://github.com/apple/container) microVMs on macOS.
The agent (OpenCode) runs *inside* the container; you interact from your
terminal and browser.

## Quickstart

```bash
./scripts/build.sh    # only needed after changing the Containerfile
./scripts/up.sh       # start container (idempotent-ish; down.sh to recreate)
./scripts/shell.sh    # shell inside the container
./scripts/marimo.sh   # open notebooks/tdi_dataset_explorer.py in marimo (pass a path to override) -> open http://localhost:2718 (see printed URL)
```

Inside the container:

```bash
opencode   # launch the agent (resume a past session with ctrl+x then l; new session: ctrl+x n)
uv run python ...      # run things against the project venv
```

## Adding Python dependencies (no rebuild!)

Deps are managed by **uv** from `pyproject.toml`, resolved at runtime into
`/workspace/.venv` (which lives on your Mac via the bind mount):

```bash
uv add polars        # updates pyproject.toml + installs instantly
uv sync              # after pulling someone else's pyproject changes
```

Rebuild the image (`./scripts/build.sh`) *only* to change system-level tooling
(new apt packages, different Python version, agent CLI upgrades).

## What persists vs. what doesn't

- **Persists** (host): all code under this directory, `.venv`, notebooks,
  `uv.lock` — even if you `./scripts/down.sh`.
- **Disposable**: container root FS. Anything installed outside /workspace
  (apt packages, global pip) vanishes on recreate. Prefer `uv add`.

## API keys

`scripts/up.sh` passes these through from your **host** environment if set:
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`,
`GEMINI_API_KEY`, `GITHUB_TOKEN`. Export what you need before `./scripts/up.sh`.
Keys are never stored in files committed to git.

## GitHub auth

SSH agent forwarding is enabled (`--ssh`), so your host's `ssh-add` identities
work for `git push` over SSH inside the container. For `gh` CLI:

```bash
gh auth login           # web flow, once, inside the container
git remote add origin git@github.com:<you>/<repo>.git && git push -u origin main
```

## Ports

- `2718` → marimo editor (bind 0.0.0.0 in-container; open
  `http://localhost:2718/?access_token=...` using the URL marimo prints).
