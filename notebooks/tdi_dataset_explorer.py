import marimo

__generated_with = "0.24.0"
app = marimo.App(app_title="OpenADMET CYP TDI Dataset Explorer")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    # Shared look & size for the builtin mo.mermaid diagrams (bundled, no CDN).
    # fontSize drives the diagram size; colors mirror mermaid's classic "default".
    MMD_THEME = {
        "primaryColor": "#ECECFF",
        "primaryBorderColor": "#9370DB",
        "primaryTextColor": "#333333",
        "lineColor": "#333333",
        "fontSize": "21px",
    }
    return (MMD_THEME,)


@app.cell
def _():
    import os

    import altair as alt
    import pandas as pd

    DATA_DIR = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "openadmet_cyp_challenge"
    )
    return DATA_DIR, alt, os, pd


@app.cell
def _(DATA_DIR, os, pd):
    _base = os.path.join(DATA_DIR, "{name}")

    def _p(name):
        return _base.format(name=name)

    RAW = {
        "inhibition": _p("cyp-challenge-TRAIN_inhibition.csv"),
        "tdi": _p("cyp-challenge-TRAIN_TDI.csv"),
        "emax": _p("cyp-challenge-TRAIN_Emax.csv"),
        "single_concentration": _p("cyp-challenge-single-concentration-TRAIN.csv"),
        "test": _p("cyp-challenge-TEST-BLINDED.csv"),
    }

    D = {k: pd.read_csv(p) for k, p in RAW.items()}
    return (D,)


@app.cell
def _(D):
    df_tdi = D["tdi"]
    ISO = ["CYP1A2", "CYP2C9", "CYP2D6", "CYP3A4"]
    return ISO, df_tdi


@app.cell
def _():
    ISO_ABBREV = {
        "CYP1A2": "1A2",
        "CYP2C9": "2C9",
        "CYP2D6": "2D6",
        "CYP3A4": "3A4",
    }

    def classify_batch(df, iso):
        dcol = f"{iso}_pIC50_direct_inhibition"
        tcol = f"{iso}_pIC50_TDI_condition"
        out = df[dcol].notna() & df[tcol].notna()
        direct = df.loc[out, dcol]
        tdi = df.loc[out, tcol]
        shift = tdi - direct
        rule = (direct > 4) & (shift > 0.301) | (direct <= 4) & (tdi > 4.3)
        return out, rule, direct, tdi, shift

    return (classify_batch,)


@app.cell
def _(alt):
    _base_axis = dict(
        labelFont="Inter, sans-serif",
        labelFontSize=13,
        titleFont="Inter, sans-serif",
        titleFontSize=13,
        gridColor="#e5e7eb",
        gridWidth=0.6,
    )

    @alt.theme.register("Default", enable=True)
    def _default():
        return {}

    @alt.theme.register("Clean", enable=True)
    def _clean():
        return {
            "background": "#ffffff",
            "font": "Inter, sans-serif",
            "view": {"stroke": "transparent"},
            "axis": {**_base_axis, "grid": True},
            "axisX": {"domain": True, "domainColor": "#cbd5e1", "domainWidth": 1.2},
            "axisY": {"domain": False},
            "legend": {"titleFontSize": 13, "labelFontSize": 12, "labelLimit": 260},
        }

    @alt.theme.register("Paper", enable=True)
    def _paper():
        return {
            "background": "#faf9f6",
            "font": "Georgia, serif",
            "title": {"font": "Georgia, serif", "fontSize": 17, "color": "#1f2937"},
            "view": {"stroke": "#d1d5db", "strokeWidth": 1},
            "axis": {
                **_base_axis,
                "labelFont": "Georgia, serif",
                "titleFont": "Georgia, serif",
                "grid": True,
                "gridColor": "#e7e5e4",
            },
            "axisX": {"domain": True, "tickColor": "#d1d5db"},
            "legend": {"labelFont": "Georgia, serif", "titleFont": "Georgia, serif"},
        }

    @alt.theme.register("Ink (dark)", enable=True)
    def _ink():
        return {
            "background": "#0f1115",
            "font": "Inter, sans-serif",
            "title": {"color": "#f9fafb"},
            "view": {"stroke": "transparent"},
            "axis": {
                **_base_axis,
                "labelColor": "#d1d5db",
                "titleColor": "#e5e7eb",
                "grid": True,
                "gridColor": "#1f2937",
                "gridDash": [2, 2],
            },
            "axisX": {"domain": True, "domainColor": "#374151", "tickColor": "#374151"},
            "legend": {
                "labelColor": "#d1d5db",
                "titleColor": "#e5e7eb",
                "labelFontSize": 12,
            },
        }

    return


@app.cell
def _(mo):
    mo.md(r"""
    # OpenADMET CYP Time‑Dependent Inhibition (TDI) Dataset Explorer

    **Source:** [`openadmet/cyp-challenge-train-test`](https://huggingface.co/datasets/openadmet/cyp-challenge-train-test)
    · Challenge: OpenADMET CYP Inhibition Blind Challenge · **License:** Apache‑2.0

    This notebook is a **deep‑dive into the raw data** — anchored by an
    interactive decision‑boundary explorer (§1) with on‑demand chemical
    structures.

    **Epistemic legend:** 🔵 OBSERVED (measured experiment) · 🟠 PREDICTED
    (derived rule / model) · 🟢 PROPOSED (what we could do next).
    """)
    return


@app.cell
def _(mo):
    theme_sel = mo.ui.radio(
        options=["Default", "Clean", "Paper", "Ink (dark)"],
        value="Clean",
        label="Chart style — switch to re-render every chart",
        inline=True,
    )
    return (theme_sel,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 0 · How the assay works (a primer)

    Flip the toggle in the interactive panel below — the whole story, in one
    picture.
    """)
    return


@app.cell
def _():
    from openadmet_tdi.widgets import DDIScene, ProbeGlowScene, ShiftScene

    return DDIScene, ProbeGlowScene, ShiftScene


@app.cell
def _(DDIScene, mo):
    _desc = mo.md(
        "**Cytochromes P450 (CYPs)** are the liver enzymes that break down most "
        "drugs. When we test a compound, we want to know: *does it stop a CYP "
        "from doing its job?* If it does, co‑administered drugs that rely on "
        'that CYP (the **"victim" drug**) clear more slowly, which can push '
        "them into toxic territory — a **drug–drug interaction (DDI)**."
        "\n\n"
        "The dataset covers the four isoforms that do most of the work: "
        "**CYP3A4, CYP2D6, CYP2C9, CYP1A2** — each assayed separately on human "
        "CYP 'Supersomes', so every number is unambiguously about one enzyme."
    )
    _credits = mo.Html(
        '<p style="font-size:0.78em;color:#64748b;line-height:1.45;'
        "margin:8px 0 0;\"><b>Panel icons:</b> liver, enzymes &amp; "
        "drug‑tablet by <b>Servier Medical Art</b> (CC‑BY 3.0); pills, drugs, "
        "metabolites &amp; toxic by Marcel Tisch, Fang‑fang‑yang &amp; David "
        "Eccles (CC0) — via <a href='https://bioicons.com' target='_blank'>"
        "bioicons.com</a>.</p>"
    )
    _widget = mo.ui.anywidget(DDIScene())
    mo.vstack([_desc, _widget, _credits])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### What the assay *measures* (the readout)

    The trick is to give the CYP a **"caged" probe** — a molecule that only
    glows (or is only detectable) after the CYP has modified it. A CYP
    "working" cleaves the probe into a **product** we can see:

    - **Fluorescence:** the probe (e.g. BOMF, EOMCC, DBOMF) is non‑fluorescent;
      the CYP's product **fluoresces**, so fluorescence = amount of product made.
    - **Mass‑spec (CYP2D6 only):** dextromethorphan → dextrorphan (a mass shift
      the instrument counts).

    So the raw signal is simply **"how much product did the enzyme make?"** A
    compound that *inhibits* the CYP makes less product → a weaker signal than
    a plate with no compound. We measure this across many compound
    concentrations to trace a dose‑response curve, from which we read off the
    **IC50** (concentration that halves the enzyme's product output) → **pIC50**
    = −log10(IC50).
    """)
    return


@app.cell
def _(ProbeGlowScene, mo):
    mo.vstack([mo.ui.anywidget(ProbeGlowScene())])
    return


@app.cell
def _(MMD_THEME, mo):
    _writeup = mo.md(r"""
    ### Experimental Design

    For every compound, the assay runs **two pre‑incubations in parallel** —
    one with the CYP switched **off** (−NADPH), one switched **on** (+NADPH) —
    then traces a 12‑point dose–response in each arm. Because only the +NADPH
    arm lets the enzyme metabolise the compound, a *time‑dependent inhibitor*
    reveals itself as a leftward slide of the dose–response: a lower IC50
    (higher pIC50) after active pre‑incubation. That **shift** between arms is
    the dataset's TDI readout, with `is_TDI = True` called at a ≥2‑fold
    potency gain.
    """)
    _diagram = mo.center(
        mo.mermaid(
            """flowchart TD
    C["Compound"] --> A["Incubate compound + CYP<br/>two arms, same plate, 30 min"]
    A --> D1["<b>DIRECT arm</b> ( –NADPH )<br/>CYP <b>switched off</b><br/>no metabolism<br/>&rarr; reversible<br/>binding only"]
    A --> T1["<b>TDI arm</b> ( +NADPH )<br/>CYP <b>switched on</b><br/>metabolises compound<br/>&rarr; reactive<br/>species may disable CYP"]
    D1 --> D2["12-pt dose-response<br/>&rarr; pIC50 direct"]
    T1 --> T2["12-point dose-response<br/>&rarr; pIC50 TDI"]
    D2 --> S{"shift = pIC50 TDI<br/>&minus; pIC50 direct"}
    T2 --> S
    S -->|"&ge; 2-fold (shift &ge; 0.301)"| P["is_TDI = True"]
    S -->|"no shift"| N["is_TDI = False"]
    """,
            theme="base",
            theme_variables=MMD_THEME,
        ),
    )
    mo.vstack([_writeup, _diagram])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### NADPH is the enzyme's "on switch" — this is what splits the two arms

    A CYP only works when it has an electron donor to power the reaction. That
    donor is **NADPH**. So the experiment takes each compound into **two arms**
    that differ *only* in whether NADPH is present during a 30‑minute
    pre‑incubation:

    - **Direct arm (−NADPH):** no NADPH → the enzyme is **"off"** → the compound
      will not be metabolised. You only see the compound *itself* reversibly
      binding and blocking the enzyme. This is plain, reversible inhibition.
    - **TDI arm (+NADPH):** NADPH present → the enzyme is **"on"** and actively
      metabolising. If the compound is a *time‑dependent inhibitor*, its
      metabolism creates a **reactive species that progressively disables the
      CYP** — so over the 30‑minute pre‑incubation it becomes a stronger
      inhibitor.

    After pre‑incubation, the substrate probe and NADPH are added to *both* arms
    and product is measured, tracing a dose‑response for each. The tell‑tale
    sign of TDI is that the dose‑response **slides left** (lower IC50 = higher
    pIC50) in the +NADPH arm:

    ```
    shift = pIC50_TDI(+NADPH) − pIC50_direct(−NADPH)
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Instant screens miss TDI — the pre‑incubation is the point

    A conventional, **instantaneous** screen (mix compound and enzyme, measure
    straight away) can rank a time‑dependent inhibitor as **clean**: at the
    moment of measurement, little enzyme has been disabled yet. The loss of
    activity **builds while the compound pre‑incubates with active CYP
    (+NADPH)** — so the dose–response you measure *afterwards* has slid left.
    Flip the toggle and watch one compound go from "sails through" to
    "flagged".
    """)
    return


@app.cell
def _(ShiftScene, mo):
    mo.vstack([mo.ui.anywidget(ShiftScene())])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1 · Explore the dataset: the decision boundary

    The core explorer. Every point is a compound measured in **both arms**; the
    dashed green line is the **2‑fold shift boundary** (`y = x + 0.301`), purple
    and blue mark the direct‑arm (`4`) and TDI‑arm (`4.3`) detection floors. Pick
    an isoform, choose a cursor mode, then **hover a point for its structure** —
    structures also render in the table's first column.
    """)
    return


@app.cell
def _():
    IMG_CACHE = {}
    return (IMG_CACHE,)


@app.cell
def _(IMG_CACHE, mo):
    import useful_rdkit_utils as uru

    def structure_uri(smiles, width=300, height=150):
        """PNG data-URI for chart tooltips (cached per SMILES).

        Drawn at 2x so the tooltip shows a crisp image on HiDPI screens.
        """
        key = ("uri", width, height, smiles)
        if key not in IMG_CACHE:
            IMG_CACHE[key] = uru.smi_to_base64_image(
                smiles, target="altair", width=width * 2, height=height * 2
            )
        return IMG_CACHE[key]

    def structure_html(smiles, width=240, height=120):
        """HTML <img> for table cells (cached per SMILES).

        Drawn at 2x and displayed at width x height so it stays crisp on
        HiDPI screens; explicit dimensions + max-*:none keep the table's CSS
        from shrinking it.
        """
        key = ("html", width, height, smiles)
        if key not in IMG_CACHE:
            IMG_CACHE[key] = uru.smi_to_base64_image(
                smiles, target="html", width=width * 2, height=height * 2
            )
        img = IMG_CACHE[key].replace(
            "<img ",
            "<img style='width:%dpx;height:%dpx;max-width:none;"
            "max-height:none;display:block' " % (width, height),
            1,
        )
        return mo.Html(img)

    return structure_html, structure_uri


@app.cell
def _(ISO, mo):
    iso_sel = mo.ui.dropdown(options=ISO, value="CYP3A4", label="Isoform")
    only_pos = mo.ui.checkbox(value=True, label="Only TDI-positive")
    cursor_sel = mo.ui.radio(
        options=["brush", "click", "pan"],
        value="brush",
        label="Cursor",
        inline=True,
    )
    return cursor_sel, iso_sel, only_pos


@app.cell
def _(
    alt,
    classify_batch,
    cursor_sel,
    df_tdi,
    iso_sel,
    mo,
    only_pos,
    pd,
    structure_uri,
    theme_sel,
):
    alt.theme.enable(theme_sel.value)
    _iso = iso_sel.value
    _out, _rule, _direct, _tdi, _shift = classify_batch(df_tdi, _iso)
    _lab = f"{_iso}_is_TDI"
    _has_labels = _lab in df_tdi.columns
    _f = df_tdi.loc[_out, ["Molecule_Name", "SMILES"]].copy()
    _f["direct"] = _direct
    _f["tdi_condition"] = _tdi
    _f["shift"] = _shift
    _f["is_TDI"] = (
        df_tdi.loc[_out, _lab].astype(bool) if _has_labels else _rule
    )
    if only_pos.value:
        _f = _f[_f["is_TDI"]]
    _f["image"] = [structure_uri(s) for s in _f["SMILES"]]
    _pts = (
        alt.Chart(_f)
        .mark_point(opacity=0.6, filled=True, size=30)
        .encode(
            x=alt.X(
                "direct:Q",
                title="pIC50 direct (–NADPH)",
                scale=alt.Scale(domain=[1, 8]),
            ),
            y=alt.Y(
                "tdi_condition:Q",
                title="pIC50 TDI (+NADPH)",
                scale=alt.Scale(domain=[1, 8]),
            ),
            color=alt.Color(
                "is_TDI:N",
                scale=alt.Scale(
                    domain=[False, True], range=["#7f7f7f", "#d62728"]
                ),
                title="is_TDI",
            ),
            tooltip=[
                "image",
                "Molecule_Name",
                "direct",
                "tdi_condition",
                "shift",
            ],
        )
        .properties(width=560, height=460)
    )
    _diag = (
        alt.Chart(pd.DataFrame({"x": [1, 7.7], "y": [1.301, 8.0]}))
        .mark_line(color="#2ca02c", strokeDash=[4, 3])
        .encode(x="x:Q", y="y:Q")
    )
    _vline = (
        alt.Chart(pd.DataFrame({"x": [4]}))
        .mark_rule(color="#9467bd", strokeDash=[4, 3])
        .encode(x="x:Q")
    )
    _hline = (
        alt.Chart(pd.DataFrame({"y": [4.3]}))
        .mark_rule(color="#1f77b4", strokeDash=[4, 3])
        .encode(y="y:Q")
    )
    _title = (
        f"{_iso} — "
        + "shipped is_TDI labels"
        if _has_labels
        else f"{_iso} — coloured by the classification rule (no shipped labels)"
    )
    _layered = _pts + _diag + _vline + _hline
    if cursor_sel.value == "brush":
        _layered = _layered.add_params(
            alt.selection_interval(encodings=["x", "y"])
        )
        scat = mo.ui.altair_chart(
            _layered.properties(title=_title),
            chart_selection=False,
            legend_selection=False,
        )
    elif cursor_sel.value == "click":
        _layered = _layered.add_params(alt.selection_point(on="click"))
        scat = mo.ui.altair_chart(
            _layered.properties(title=_title),
            chart_selection=False,
            legend_selection=False,
        )
    else:
        scat = mo.ui.altair_chart(
            _layered.properties(title=_title).interactive(),
            chart_selection=False,
            legend_selection=False,
        )
    scatter_points = _f
    mo.vstack([mo.hstack([iso_sel, only_pos, cursor_sel]), scat])
    return scat, scatter_points


@app.cell
def _(mo, scat, scatter_points, structure_html):
    _selection = scat.selections
    _selected = (
        scat.apply_selection(scatter_points) if _selection else scatter_points
    )
    _hint = (
        ""
        if _selection
        else " — brush‑select points to isolate yours"
    )
    _shown = _selected.sort_values("shift", ascending=False)
    _table = _shown[
        ["Molecule_Name", "SMILES", "direct", "tdi_condition", "shift", "is_TDI"]
    ].copy().reset_index(drop=True)
    _table.insert(0, "structure", [structure_html(s) for s in _shown["SMILES"]])
    mo.vstack(
        [
            mo.md(f"**{len(_selected):,} compounds** selected{_hint}"),
            mo.ui.table(_table, selection=None, page_size=10),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
