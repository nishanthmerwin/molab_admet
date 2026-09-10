# OpenCode agent guidance for this repo.

## Environment
- This is the mounted workspace; container root FS is disposable.
- Python: always use `uv` (`uv add <pkg>`, `uv run python ...`, `uv run marimo edit`).
  Never pip-install into system python.
- marimo notebooks are `.py` files; edit them directly or via `uv run marimo edit --host 0.0.0.0`.
- GitHub: `gh` CLI and SSH are available; SSH agent is forwarded from the host.

## Conventions
- Keep new dependencies in pyproject.toml via `uv add`, not requirements files.
- Notebooks must stay valid marimo format (run `marimo check .` after edits).

## Pasted screenshots
- Cmd+V images from cmux are auto-materialized by `.opencode/plugins/paste-materializer.js`
  into `.opencode-data/pastes/<timestamp>.<ext>` (gitignored, ephemeral working material).
- The saved worktree-relative path is injected into the message as a text part;
  prefer that path with file tools instead of the transient `clipboard-*.png` temp file.
