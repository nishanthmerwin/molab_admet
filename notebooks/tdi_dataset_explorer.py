import marimo

__generated_with = "0.24.0"
app = marimo.App(app_title="OpenADMET CYP TDI Dataset Explorer")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    _STYLES = {
        "OBSERVED": ("#dbeafe", "#1e40af"),
        "PREDICTED": ("#fef3c7", "#92400e"),
        "HYPOTHESIS": ("#f3e8ff", "#6b21a8"),
        "PROPOSED": ("#dcfce7", "#166534"),
    }

    def badge(kind, text=""):
        _bg, _fg = _STYLES[kind]
        _label = f"{kind} · {text}" if text else kind
        return mo.Html(
            f'<span style="background:{_bg};color:{_fg};padding:2px 8px;'
            f'border-radius:999px;font-size:0.75em;font-weight:700;'
            f'letter-spacing:0.03em">{_label}</span>'
        )

    return (badge,)


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
    structures. The remaining sections (§A1–A7) form an appendix: how the
    dataset is shaped, how the labels are derived, and the supporting views.

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
    an isoform, toggle positives‑only, then **brush‑select points** — the
    selected compounds' chemical structures are drawn below the table.
    """)
    return


@app.cell
def _():
    from rdkit import Chem
    from rdkit.Chem import Draw

    def structures_grid(names, smiles, mols_per_row=4, sub_img=(200, 150)):
        """PIL grid of RDKit structures for (name, smiles) pairs; None if nothing draws."""
        pairs = []
        for name, smi in zip(names, smiles):
            mol = Chem.MolFromSmiles(smi or "")
            if mol is not None:
                pairs.append((mol, str(name)))
        if not pairs:
            return None
        return Draw.MolsToGridImage(
            [m for m, _ in pairs],
            molsPerRow=mols_per_row,
            subImgSize=sub_img,
            legends=[n for _, n in pairs],
        )

    return (structures_grid,)


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
                "Molecule_Name",
                "SMILES",
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
def _(mo, scat, scatter_points, structures_grid):
    _selection = scat.selections
    _selected = (
        scat.apply_selection(scatter_points) if _selection else scatter_points
    )
    _hint = (
        ""
        if _selection
        else " — showing the 8 strongest shifts; brush‑select points to isolate yours"
    )
    _cap = _selected.sort_values("shift", ascending=False).head(8)
    _img = structures_grid(_cap["Molecule_Name"], _cap["SMILES"])
    mo.vstack(
        [
            mo.md(f"**{len(_selected):,} compounds** selected{_hint}"),
            mo.ui.table(
                _selected.sort_values("shift", ascending=False),
                selection=None,
                page_size=10,
            ),
            mo.image(_img) if _img is not None else mo.md(""),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Appendix — supporting analyses

    The rest of the notebook: how the dataset is shaped, how the labels are
    derived and validated, and the remaining views (real‑data shift example,
    pipeline diagrams, shift distribution, flagship scanner). Nothing here is
    needed for the core explorer above.
    """)
    return


@app.cell
def _(D, alt, mo, pd, theme_sel):
    alt.theme.enable(theme_sel.value)
    _iso = "CYP3A4"
    _name = "OCNT-2315392"
    _t = D["tdi"]
    _row = _t[_t["Molecule_Name"] == _name].iloc[0]
    _rows = pd.DataFrame(
        {
            "arm": ["direct (−NADPH)", "TDI (+NADPH)"],
            "pIC50": [
                _row[f"{_iso}_pIC50_direct_inhibition"],
                _row[f"{_iso}_pIC50_TDI_condition"],
            ],
            "CI low": [
                _row[f"{_iso}_pIC50_direct_inhibition_conf_low"],
                _row[f"{_iso}_pIC50_TDI_condition_conf_low"],
            ],
            "CI high": [
                _row[f"{_iso}_pIC50_direct_inhibition_conf_high"],
                _row[f"{_iso}_pIC50_TDI_condition_conf_high"],
            ],
        }
    )
    _shift = float(_rows["pIC50"].iloc[1] - _rows["pIC50"].iloc[0])
    _pts = (
        alt.Chart(_rows)
        .mark_point(filled=True, size=120)
        .encode(
            x=alt.X(
                "pIC50:Q",
                title="pIC50 (higher = more potent, i.e. lower IC50)",
                scale=alt.Scale(domain=[4.5, 7.2]),
            ),
            y=alt.Y("arm:N", title=None),
            color=alt.Color(
                "arm:N",
                scale=alt.Scale(
                    domain=["direct (−NADPH)", "TDI (+NADPH)"],
                    range=["#4c78a8", "#e45756"],
                ),
                legend=None,
            ),
            tooltip=["arm", "pIC50", "CI low", "CI high"],
        )
    )
    _err = (
        alt.Chart(_rows)
        .mark_errorbar(extent="ci", thickness=3)
        .encode(
            x=alt.X("pIC50:Q", title=None),
            x2="CI high:Q",
            y="arm:N",
            color=alt.Color(
                "arm:N",
                scale=alt.Scale(
                    domain=["direct (−NADPH)", "TDI (+NADPH)"],
                    range=["#4c78a8", "#e45756"],
                ),
                legend=None,
            ),
            tooltip=["arm", "CI low", "CI high"],
        )
    )
    _gap = (
        alt.Chart(
            pd.DataFrame(
                {
                    "x0": [_rows["pIC50"].iloc[0]],
                    "x1": [_rows["pIC50"].iloc[1]],
                    "y": [0.225],
                }
            )
        )
        .mark_rule(color="#666", strokeDash=[5, 4])
        .encode(x="x0:Q", x2="x1:Q", y="y:Q")
    )
    _chart = (_err + _pts + _gap).properties(width=620, height=220)
    mo.vstack(
        [
            mo.md(
                "### Visualising the shift on real data: `%s` (CYP3A4)" % _name
            ),
            mo.md(
                "A **real** TDI-positive compound from this dataset, with its two "
                "measured potencies and 95% confidence intervals (CI). Its dose‑"
                "response is **more potent in the +NADPH (TDI) arm** than in the "
                "−NADPH (direct) arm — the measured pIC50 jumps from "
                f"**{_rows['pIC50'].iloc[0]:.2f} → {_rows['pIC50'].iloc[1]:.2f}**, "
                f"a shift of **+{_shift:.2f} log10** "
                f"(= {10**_shift:.1f}× more potent IC50) once the CYP was allowed "
                "to metabolise it. The CIs do not overlap, so this is a confident TDI "
                "call. This *is* the IC50 shift that the whole dataset's `is_TDI` "
                "labels are built from."
            ),
            mo.ui.altair_chart(_chart),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### The tiering funnel, the decision rule — the rest of the pipeline

    The remaining pieces of the pipeline, at a glance.
    """)
    return


@app.cell
def _(MMD_THEME, mo):
    _diagram = mo.mermaid(
        """flowchart LR
    L["<b>Library</b><br/>Enamine DDS10 (~10k)<br/>+ ~1k FDA drugs"] --> P["<b>Primary screen</b><br/>single conc 50 &micro;M<br/><b>TDI arm only</b><br/>all 4 isoforms"]
    P --> H["Hits promoted<br/>~1.5k each 1A2/2C9/2D6<br/>~2.25k for 3A4"]
    H --> DRC["<b>12-point dose-response</b><br/>both arms<br/>Bayesian fit &rarr; pIC50 &plusmn; 95% CI"]
    DRC --> LBL["<b>Call TDI</b><br/>from the IC50 shift"]
    """,
        theme="base",
        theme_variables=MMD_THEME,
    )
    mo.vstack([mo.md("### Tiering funnel — from library to labels"), _diagram])
    return


@app.cell
def _(MMD_THEME, mo):
    _diagram = mo.mermaid(
        """flowchart TD
    A["For each isoform<br/>pIC50 direct &amp; pIC50 TDI"] --> B{"direct &gt; 4?<br/>(measurable direct activity)"}
    B -->|"Yes"| C{"shift &gt; 0.301?<br/>(2-fold potency gain)"}
    C -->|"Yes"| T["is_TDI = True"]
    C -->|"No"| F["is_TDI = False"]
    B -->|"No (below-detection)"| D{"pIC50 TDI &gt; 4.3?<br/>(measurable in TDI arm)"}
    D -->|"Yes"| T
    D -->|"No"| F
    """,
        theme="base",
        theme_variables=MMD_THEME,
    )
    mo.vstack(
        [mo.md("### Labeling decision rule (Method 1, the shipped one)"), _diagram]
    )
    return


@app.cell
def _(MMD_THEME, mo):
    _diagram = mo.mermaid(
        """flowchart TD
    M["Dose-response<br/>(both arms, 4 isoforms)"] --> F["Bayesian fit"]
    F --> PIC["<b>pIC50</b> = potency<br/>(curve position)"]
    F --> EMAX["<b>Emax</b> = efficacy<br/>(curve max, EmaxVsPosCtrl)"]
    PIC --> TC["<b>TDI config</b><br/>labels 2D6 &amp; 3A4<br/>ships shift columns"]
    EMAX --> EC["<b>Emax config</b><br/>labels all 4 isoforms<br/>no shift columns"]
    """,
        theme="base",
        theme_variables=MMD_THEME,
    )
    mo.vstack(
        [mo.md("### pIC50 vs Emax — what each shipped config emphasises"), _diagram]
    )
    return


@app.cell
def _(D, mo, pd):
    shapes = pd.DataFrame(
        {
            "config": list(D.keys()),
            "rows": [len(D[k]) for k in D],
            "unique compounds": [D[k]["Molecule_Name"].nunique() for k in D],
            "content": [
                "Direct‑inhibition pIC50 (4 isoforms, train)",
                "TDI labels + TDI‑condition & direct pIC50 (CYP2D6/3A4)",
                "TDI/Emax labels for **all four** CYPs",
                "Single‑concentration primary screen (log2 fold‑change)",
                "750‑compound blinded test set (SMILES only)",
            ],
        }
    )
    _unique = len(set().union(*[set(D[k]["Molecule_Name"]) for k in D]))
    mo.vstack(
        [
            mo.md("### 1 · Dataset at a glance"),
            mo.md(
                "Five CSV files (the five configs of the HF dataset) were downloaded "
                f"into `data/raw/openadmet_cyp_challenge/`. **{_unique:,} unique** "
                "compounds across all configs."
            ),
            mo.ui.table(shapes, selection=None),
        ]
    )
    return


@app.cell
def _(D, mo, pd):
    df_tdi = D["tdi"]
    df_emax = D["emax"]
    ISO = ["CYP1A2", "CYP2C9", "CYP2D6", "CYP3A4"]
    iso_overview = pd.DataFrame(
        {
            "isoform": ISO,
            "labeled (TDI config)": [
                int(
                    df_tdi.get(f"{k}_is_TDI", pd.Series(dtype=bool))
                    .notna()
                    .sum()
                )
                for k in ISO
            ],
            "labeled (Emax config)": [
                int(df_emax[f"{k}_is_TDI"].notna().sum()) for k in ISO
            ],
        }
    )
    mo.vstack(
        [
            mo.md("### 2 · What labels does the dataset ship?"),
            mo.md(
                "The **Emax config** carries an explicit `is_TDI` boolean for **all four** "
                "isoforms; the **TDI config** ships labels for **CYP2D6 and CYP3A4 only** "
                "(plus pIC50 measurements for every isoform)."
            ),
            mo.ui.table(iso_overview, selection=None),
        ]
    )
    return ISO, df_emax, df_tdi


@app.cell
def _(mo):
    mo.md(r"""
    ### 3 · How frequent is TDI?

    The headline question. A compound counts as a **TDI positive** if it is labelled
    `True` for *any* isoform.

    **Key pattern:** nearly all positives come from one isoform — **CYP3A4**.
    CYP2D6 is a distant second. CYP1A2 and CYP2C9 are essentially non‑positive,
    which is why the challenge scores TDI only for CYP3A4/CYP2D6.
    """)
    return


@app.cell
def _(ISO, alt, df_emax, mo, pd, theme_sel):
    alt.theme.enable(theme_sel.value)
    pos_by_iso = pd.DataFrame(
        {
            "isoform": ISO,
            "positive": [
                int(df_emax[f"{k}_is_TDI"].fillna(False).sum()) for k in ISO
            ],
            "labeled": [
                int(df_emax[f"{k}_is_TDI"].notna().sum()) for k in ISO
            ],
        }
    )
    pos_by_iso["rate (labeled)"] = (
        pos_by_iso["positive"] / pos_by_iso["labeled"]
    )
    _chart = (
        alt.Chart(pos_by_iso)
        .mark_bar()
        .encode(
            x=alt.X("isoform:N", sort=ISO),
            y=alt.Y("positive:Q", title="TDI-positive compounds"),
            color=alt.Color(
                "isoform:N", scale=alt.Scale(scheme="set2"), legend=None
            ),
            tooltip=["isoform", "positive", "labeled", "rate (labeled)"],
        )
        .properties(width=520, height=360)
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(ISO, badge, df_emax, mo, pd):
    per_compound = pd.DataFrame(
        {
            "Molecule_Name": df_emax["Molecule_Name"],
            "n_positive_isoforms": df_emax[[f"{k}_is_TDI" for k in ISO]]
            .fillna(False)
            .sum(axis=1),
        }
    )
    per_compound["any_positive"] = per_compound["n_positive_isoforms"] > 0
    _ppos = per_compound[per_compound["any_positive"]]
    mo.vstack(
        [
            mo.md(
                "Across the **{}**-compound training set (Emax config, n={:,}):".format(
                    "6,145", len(df_emax)
                )
            ),
            mo.md(
                f"**{len(_ppos):,} compounds ({len(_ppos) / len(df_emax):.1%}) are "
                "TDI-positive for at least one isoform.**"
            ),
            mo.md(
                f"Multi-isoform TDI is rare: "
                f"**{int((per_compound['n_positive_isoforms'] >= 2).sum())} compounds** "
                f"are positive for ≥2 isoforms ({_ppos['n_positive_isoforms'].mean():.2f} "
                "positives per positive compound on average)."
            ),
            badge("OBSERVED", "counts from shipped is_TDI labels"),
        ]
    )
    return (per_compound,)


@app.cell
def _(alt, badge, mo, per_compound, theme_sel):
    alt.theme.enable(theme_sel.value)
    mo.vstack(
        [
            mo.md("### 3a · Distribution of # positive isoforms per compound"),
            badge("OBSERVED"),
            mo.ui.altair_chart(
                alt.Chart(per_compound)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "n_positive_isoforms:O", title="Positive isoforms"
                    ),
                    y=alt.Y("count()", title="compounds"),
                    color=alt.condition(
                        "datum.n_positive_isoforms > 0",
                        alt.value("#8b0000"),
                        alt.value("#999"),
                    ),
                )
                .properties(width=480, height=300)
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 4 · How is TDI *classified* here?

    This is the mechanism behind the labels. It is an **IC50‑shift** design:

    - **Direct‑inhibition arm (−NADPH):** compound pre‑incubated with the CYP
      *without* NADPH → no metabolism → measures **reversible** binding of the
      parent (`pIC50_direct`).
    - **TDI arm (+NADPH):** compound pre‑incubated *with* NADPH → enzyme turns the
      compound over → captures **metabolism‑dependent inactivation**
      (`pIC50_TDI_condition`).

    A time‑dependent inhibitor shifts its dose‑response **left** (lower IC50, higher
    pIC50) on pre‑incubation, because metabolism produces a more potent species.
    The **shift** is:

    ```
    shift = pIC50_TDI_condition - pIC50_direct_inhibition
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### The exact classification rule

    Reproducing the shipped `is_TDI` labels from the raw pIC50 numbers, the rule is:

    - **Positive** if `pIC50_direct > 4` **and** `shift > 0.301` — a **2‑fold**
      IC50 shift (`log10(2) = 0.301`).
    - **Inferred positive** if `pIC50_direct <= 4` **but** `pIC50_TDI_condition > 4.3`
      — activity jumps from below‑detectable to detectable, guaranteeing a large
      effective shift. `4.3` is the assay sensitivity floor (≈ 50 µM).

    This rule reproduces **every shipped label exactly (100%)** for both CYP3A4 and
    CYP2D6.
    """)
    return


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
def _(classify_batch, df_tdi, mo, pd):
    validation = {}
    for iso in ["CYP3A4", "CYP2D6"]:
        _lab = f"{iso}_is_TDI"
        _out, _rule, _, _, _ = classify_batch(df_tdi, iso)
        _sub = df_tdi.loc[_out, [_lab]]
        acc = (_rule == _sub[_lab].astype(bool)).mean()
        validation[iso] = round(float(acc), 4)
    mo.vstack(
        [
            mo.md("### Rule validation against shipped labels"),
            mo.ui.table(
                pd.DataFrame(
                    {
                        "isoform": list(validation),
                        "label match rate": list(validation.values()),
                        "status": [
                            "EXACT" if v == 1.0 else "partial"
                            for v in validation.values()
                        ],
                    }
                ),
                selection=None,
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 6 · The 2‑fold shift cut‑off

    Distribution of `shift` (pIC50_TDI − pIC50_direct) for labelled compounds, split
    by class. The dashed line at `0.301` (= log10 2) is exactly where the positives
    begin — the **2‑fold IC50‑shift threshold** defining a time‑dependent inhibitor.
    """)
    return


@app.cell
def _(mo):
    iso3_sel = mo.ui.dropdown(
        options=["CYP3A4", "CYP2D6"], value="CYP3A4", label="Isoform"
    )
    return (iso3_sel,)


@app.cell
def _(alt, classify_batch, df_tdi, iso3_sel, mo, pd, theme_sel):
    alt.theme.enable(theme_sel.value)
    _out, _rule, _direct, _tdi, _shift = classify_batch(df_tdi, iso3_sel.value)
    _lab = f"{iso3_sel.value}_is_TDI"
    _f = df_tdi.loc[_out, [_lab]].copy()
    _f["shift"] = _shift
    _f["label"] = _f[_lab].astype(bool)
    _f = _f.dropna(subset=["shift"])
    _hist = (
        alt.Chart(_f)
        .mark_bar(opacity=0.7)
        .encode(
            alt.X(
                "shift:Q",
                bin=alt.Bin(maxbins=80),
                title="shift = pIC50 TDI − pIC50 direct",
            ),
            alt.Y("count()", title="compounds"),
            alt.Color(
                "label:N",
                scale=alt.Scale(
                    domain=[False, True], range=["#7f7f7f", "#d62728"]
                ),
                title="is_TDI",
            ),
        )
        .properties(width=620, height=320)
    )
    _cut = (
        alt.Chart(pd.DataFrame({"x": [0.301]}))
        .mark_rule(color="#2ca02c", strokeWidth=2)
        .encode(x="x:Q")
    )
    mo.vstack(
        [
            iso3_sel,
            mo.md(
                f"### {iso3_sel.value} — shift distribution split by TDI class (cut at 0.301)"
            ),
            mo.ui.altair_chart(_hist + _cut),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 7 · Flagship candidate scanner

    For the *CYP TDI Investigator* storyline we want **mechanistically interesting**
    TDI‑positives — compounds with a **strong IC50 shift** (a clear, confident
    time‑dependent effect) in an isoform we can build a narrative around (CYP3A4 or
    CYP2D6). This table ranks candidates by shift strength.
    """)
    return


@app.cell
def _(mo):
    iso4_sel = mo.ui.dropdown(
        options=["CYP3A4", "CYP2D6"], value="CYP3A4", label="Isoform"
    )
    top_n = mo.ui.slider(5, 50, value=20, label="Top N by shift")
    return iso4_sel, top_n


@app.cell
def _(alt, classify_batch, df_tdi, iso4_sel, mo, theme_sel, top_n):
    alt.theme.enable(theme_sel.value)
    _out, _rule, _direct, _tdi, _shift = classify_batch(df_tdi, iso4_sel.value)
    _lab = f"{iso4_sel.value}_is_TDI"
    _f = (
        df_tdi.loc[_out, ["Molecule_Name", "SMILES", _lab]]
        .copy()
        .reset_index(drop=True)
    )
    _f["direct"] = _direct.reset_index(drop=True)
    _f["tdi_condition"] = _tdi.reset_index(drop=True)
    _f["shift"] = _shift.reset_index(drop=True)
    _f["is_TDI"] = _f[_lab].astype(bool)
    _ranked = (
        _f[_f["is_TDI"]]
        .sort_values("shift", ascending=False)
        .head(top_n.value)
    )
    _scat2 = (
        alt.Chart(_f)
        .mark_point(opacity=0.3, filled=True, size=26)
        .encode(
            x=alt.X("direct:Q", title="pIC50 direct"),
            y=alt.Y("tdi_condition:Q", title="pIC50 TDI condition"),
            color=alt.condition(
                "datum.is_TDI", alt.value("#d62728"), alt.value("#bbb")
            ),
            tooltip=["Molecule_Name", "SMILES"],
        )
        .properties(width=560, height=400)
    )
    _rank_pts = (
        alt.Chart(_ranked)
        .mark_point(filled=True, size=70, color="#000", opacity=0.6)
        .encode(
            x="direct:Q",
            y="tdi_condition:Q",
            tooltip=["Molecule_Name", "shift"],
        )
    )
    mo.vstack(
        [
            mo.hstack([iso4_sel, top_n]),
            mo.md(
                f"### Top {len(_ranked)} TDI-positive {iso4_sel.value} compounds by shift "
                "strength (highlighted on plot)"
            ),
            mo.ui.altair_chart(_scat2 + _rank_pts),
            mo.ui.table(
                _ranked[
                    [
                        "Molecule_Name",
                        "SMILES",
                        "direct",
                        "tdi_condition",
                        "shift",
                    ]
                ],
                selection=None,
                page_size=10,
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    **Summary of what we learned**

    - **TDI is common here:** ~18% of the 6,145‑compound training set is
      TDI‑positive for ≥1 isoform.
    - **CYP3A4 dominates** (764 positives), then CYP2D6 (324); CYP1A2/CYP2C9 are
      effectively non‑positive (a handful each).
    - **TDI = a ≥2‑fold IC50 shift** (shift > 0.301) on NADPH pre‑incubation, or an
      inferred positive when a compound jumps from below‑detectable direct activity
      to a detectable TDI‑arm effect (`TDI > 4.3`).
    - The full 2‑branch rule **reproduces every shipped label exactly (100%)**.

    The **appendix** below holds the supporting analyses — dataset shape, label
    derivation & validation, the shift distribution and the flagship‑candidate
    scanner.
    """)
    return


if __name__ == "__main__":
    app.run()
