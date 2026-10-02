"""An interactive "drug–drug interaction" visual essay panel (anywidget).

Renders two side-by-side scenes — a healthy CYP clearing a victim drug, and a
CYP blocked by an inhibitor letting the victim drug accumulate toward toxic
levels — using CC0/CC-BY icons from https://bioicons.com (see assets/bioicons).
"""

from __future__ import annotations

import base64
import pathlib
from functools import lru_cache

import anywidget
import traitlets

_WIDGET_DIR = pathlib.Path(__file__).resolve().parent
_ICON_DIR = _WIDGET_DIR.parent.parent.parent / "assets" / "bioicons"

_ICON_NAMES = [
    "liver",
    "enzyme_yellow",
    "drug_tablet",
    "pill_blue",
]


@lru_cache(maxsize=2)
def get_icon_uris(icon_dir: pathlib.Path | None = None, names: tuple[str, ...] | None = None):
    """Return ``{name: data-URI}`` for the bundled bioicons SVGs.

    ``names`` selects a subset (defaults to all bundled icons).
    """
    d = pathlib.Path(icon_dir) if icon_dir is not None else _ICON_DIR
    uris: dict[str, str] = {}
    for name in names if names is not None else _ICON_NAMES:
        p = d / f"{name}.svg"
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode("ascii")
            uris[name] = f"data:image/svg+xml;base64,{b64}"
    return uris


class DDIScene(anywidget.AnyWidget):
    """Interactive 'drug–drug interaction' scene built from bioicons."""

    _esm = str(_WIDGET_DIR / "ddi_scene.js")
    _css = str(_WIDGET_DIR / "ddi_scene.css")

    icon_uris = traitlets.Dict(default_value=get_icon_uris()).tag(sync=True)