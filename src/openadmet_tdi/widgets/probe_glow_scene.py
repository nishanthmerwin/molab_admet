"""An interactive "caged probe → glow" readout demo.

Shows what the assay physically measures: the CYP cleaves a dark, caged probe
into a fluorescent product; the glow (signal) is proportional to how much
enzyme is working. A compound-concentration slider dims the glow the same way
an inhibitor does — the dimming curve is where IC50/pIC50 come from.
"""

from __future__ import annotations

import pathlib

import anywidget
import traitlets

from openadmet_tdi.widgets.ddi_scene import get_icon_uris

_WIDGET_DIR = pathlib.Path(__file__).resolve().parent


class ProbeGlowScene(anywidget.AnyWidget):
    """Interactive 'caged probe → glowing product → signal' readout scene."""

    _esm = str(_WIDGET_DIR / "probe_glow_scene.js")
    _css = str(_WIDGET_DIR / "probe_glow_scene.css")

    icon_uris = traitlets.Dict(
        default_value=get_icon_uris(names=("enzyme_yellow",))
    ).tag(sync=True)