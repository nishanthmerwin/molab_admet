"""An interactive "instant screen vs pre-incubation" dose–response demo.

Shows why time-dependent inhibition (TDI) is missed by instantaneous reads:
measured straight away the dose-response looks clean, but after a 30-minute
pre-incubation with active CYP (+NADPH) the curve slides left across the hit
threshold. Pure inline SVG — no external assets.
"""

from __future__ import annotations

import pathlib

import anywidget

_WIDGET_DIR = pathlib.Path(__file__).resolve().parent


class ShiftScene(anywidget.AnyWidget):
    """Interactive 'instant vs pre-incubated read' dose–response slider."""

    _esm = str(_WIDGET_DIR / "shift_scene.js")
    _css = str(_WIDGET_DIR / "shift_scene.css")