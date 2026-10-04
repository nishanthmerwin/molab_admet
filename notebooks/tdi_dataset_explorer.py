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
    import numpy as np
    import pandas as pd
    import shap
    import xgboost as xgb

    DATA_DIR = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "openadmet_cyp_challenge"
    )
    return DATA_DIR, alt, np, os, pd, shap, xgb


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
    structures, plus a SHAP analysis of which **pharmacophore patterns**
    drive TDI (§2).

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


@app.cell
def _(mo):
    mo.md(r"""
    ## 2 · Which pharmacophores drive TDI? (SHAP)

    We featurize each molecule with a **2D pharmacophore fingerprint** rather
    than Morgan/ECFP: ECFP bits enumerate circular *atom environments*
    ("aromatic C with an N neighbour at radius 2") — SHAP can rank them, but
    they are not pharmacophores a chemist can read. Here every bit **is** a
    readable pattern: 2 or 3 points drawn from the standard feature families
    (Donor, Acceptor, Aromatic, Hydrophobe, LumpedHydrophobe, PosIonizable,
    NegIonizable, ZnBinder) at topological-distance bins in **bond counts** —
    e.g. "Acceptor–Donor @ 5–8 bonds". A gradient-boosted classifier predicts
    the §1 decision-boundary label from these bits (splits are grouped by
    molecule to prevent leakage), and TreeSHAP attributes each prediction back
    to its pharmacophore bits.

    *Caveats:* labels are rule-derived (§1), samples are pooled across
    isoforms, and discrimination is modest — read this as a **ranked
    shortlist of candidate pharmacophores**, not causal effects.
    """)
    return


@app.cell
def _(ISO, classify_batch, df_tdi, mo, np, os, pd):
    import rdkit
    from rdkit import Chem, RDLogger
    from rdkit.Chem import ChemicalFeatures
    from rdkit.Chem.Pharm2D import Generate
    from rdkit.Chem.Pharm2D.SigFactory import SigFactory

    RDLogger.DisableLog("rdApp.*")

    # 2D pharmacophore signature: 2- and 3-point patterns over 8 feature
    # families, 5 topological-distance bins (bond counts, not Å).
    _fdef = os.path.join(os.path.dirname(rdkit.__file__), "Data", "BaseFeatures.fdef")
    PHARM_SIG = SigFactory(
        ChemicalFeatures.BuildFeatureFactory(_fdef),
        minPointCount=2,
        maxPointCount=3,
        trianglePruneBins=False,
    )
    PHARM_SIG.SetBins([(0, 2), (2, 3), (3, 4), (4, 5), (5, 8)])
    PHARM_SIG.Init()

    with mo.status.spinner(
        title=f"Computing {PHARM_SIG.GetSigSize():,}-bit pharmacophore fingerprints "
        "(first run only, cached per molecule)"
    ):
        BITS = {
            _smi: np.asarray(
                Generate.Gen2DFingerprint(Chem.MolFromSmiles(_smi), PHARM_SIG), np.uint8
            )
            for _smi in df_tdi["SMILES"].dropna().unique()
        }

    # pooled (compound, isoform) samples labelled by the §1 rule
    _rows = []
    for _iso in ISO:
        _out, _rule, *_ = classify_batch(df_tdi, _iso)
        _sub = df_tdi.loc[_out, ["Molecule_Name", "SMILES"]].copy()
        _sub["isoform"] = _iso
        _sub["label"] = _rule.to_numpy()
        _rows.append(_sub)
    PHARM_DATA = pd.concat(_rows, ignore_index=True)

    mo.md(
        f"**{len(BITS):,}** molecules fingerprinted → "
        f"**{PHARM_SIG.GetSigSize():,}** pharmacophore bits each · "
        f"**{len(PHARM_DATA):,}** (compound, isoform) samples · "
        f"TDI rate **{PHARM_DATA.label.mean():.0%}**"
    )
    return BITS, Chem, Generate, PHARM_DATA, PHARM_SIG


@app.cell
def _(BITS, PHARM_DATA, mo, np, xgb):
    from sklearn.metrics import average_precision_score, roc_auc_score
    from sklearn.model_selection import GroupShuffleSplit

    SH_X = np.stack([BITS[s] for s in PHARM_DATA["SMILES"]]).astype(np.float32)
    _y = PHARM_DATA["label"].astype(int).to_numpy()
    _tr, SH_TE = next(
        GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=0).split(
            SH_X, _y, PHARM_DATA["SMILES"]
        )
    )
    SH_CLF = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.5,
        tree_method="hist",
        n_jobs=-1,
        eval_metric="auc",
        scale_pos_weight=float((_y[_tr] == 0).sum() / (_y[_tr] == 1).sum()),
        random_state=0,
    )
    SH_CLF.fit(SH_X[_tr], _y[_tr])
    _p = SH_CLF.predict_proba(SH_X[SH_TE])[:, 1]
    mo.md(
        f"Hold-out (molecule-grouped): AUROC **{roc_auc_score(_y[SH_TE], _p):.2f}** · "
        f"average precision **{average_precision_score(_y[SH_TE], _p):.2f}** "
        f"(base rate {PHARM_DATA.label.mean():.0%}) — modest, as expected for "
        "rule-derived labels and 0/1 bits, but enough signal to rank "
        "pharmacophores by SHAP attribution."
    )
    return SH_CLF, SH_TE, SH_X


@app.cell
def _(PHARM_SIG, SH_CLF, SH_TE, SH_X, alt, mo, np, pd, shap, theme_sel):
    alt.theme.enable(theme_sel.value)

    _BINS = [(0, 2), (2, 3), (3, 4), (4, 5), (5, 8)]

    def bit_label(i):
        feats, *mat = PHARM_SIG.GetBitDescription(i).split("|")
        names = "-".join(w.replace("Ionizable", "Ion") for w in feats.split())
        dists = "/".join(
            f"{_BINS[int(d)][0]}\u2013{_BINS[int(d)][1]}" for d in mat[0].split()
        )
        return f"{names} @ {dists} bonds"

    _sub = np.random.RandomState(0).choice(
        SH_TE, size=min(1500, len(SH_TE)), replace=False
    )
    SH_EXPL = shap.TreeExplainer(SH_CLF)
    SH_SCORES = SH_CLF.predict_proba(SH_X)[:, 1]
    _sv = SH_EXPL.shap_values(SH_X[_sub].astype(np.float32))
    _mean, _mag = _sv.mean(0), np.abs(_sv).mean(0)
    _idx = np.argsort(-_mag)[:15]
    SH_TOP = pd.DataFrame(
        {
            "bit": _idx,
            "pharmacophore": [bit_label(i) for i in _idx],
            "mean |SHAP|": _mag[_idx],
            "signed mean SHAP": _mean[_idx],
            "direction": np.where(_mean[_idx] > 0, "presence \u2192 TDI", "presence \u2192 non-TDI"),
            "carrier rate": [float((SH_X[:, i] > 0).mean()) for i in _idx],
        }
    )
    mo.md(
        "Top 15 pharmacophore bits by mean |SHAP|. Positive attribution means "
        "**bit presence pushes the prediction toward TDI**; click bars for "
        "magnitude, sign and how often each bit is switched on across the "
        "dataset."
    )
    return SH_EXPL, SH_SCORES, SH_TOP, bit_label


@app.cell
def _(SH_TOP, alt, theme_sel):
    alt.theme.enable(theme_sel.value)
    _bar = (
        alt.Chart(SH_TOP)
        .mark_bar()
        .encode(
            x=alt.X("mean |SHAP|:Q", title="mean |SHAP| attribution"),
            y=alt.Y("pharmacophore:N", sort="-x", title=None),
            color=alt.Color(
                "direction:N",
                scale=alt.Scale(
                    domain=["presence \u2192 TDI", "presence \u2192 non-TDI"],
                    range=["#d62728", "#1f77b4"],
                ),
                title=None,
            ),
            tooltip=[
                alt.Tooltip("pharmacophore:N", title="pharmacophore"),
                alt.Tooltip("mean |SHAP|:Q", format=".3f"),
                alt.Tooltip("signed mean SHAP:Q", format=".3f"),
                alt.Tooltip("carrier rate:Q", format=".1%", title="carrier rate"),
            ],
        )
        .properties(height=380, title="Top pharmacophore bits by SHAP attribution")
    )
    _bar
    return


@app.cell
def _(PHARM_DATA, SH_SCORES, mo, pd):
    _sc = pd.DataFrame(
        {"SMILES": PHARM_DATA["SMILES"], "name": PHARM_DATA["Molecule_Name"], "p": SH_SCORES}
    )
    _sc = (
        _sc.groupby("SMILES", as_index=False)
        .agg({"p": "max", "name": "first"})
        .sort_values("p", ascending=False)
    )
    _opts = {}
    for _, _r in pd.concat([_sc.head(20), _sc.tail(15)]).iterrows():
        _opts[f"{_r['name']}  \u00b7  p(TDI) {_r['p']:.2f}"] = _r["SMILES"]
    mol_src = mo.ui.radio(
        options={"Dataset molecule": "dataset", "Custom SMILES": "custom"},
        value="Dataset molecule",
        inline=True,
        label="Molecule source",
    )
    mol_pick = mo.ui.dropdown(
        options=_opts,
        value=next(iter(_opts)),
        label="Curated: 20 highest- and 15 lowest-scoring dataset molecules",
        full_width=True,
    )
    smi_box = mo.ui.text(
        value="OC(Cn1cncn1)(Cn2cncn2)c3ccc(F)cc3F",
        label="Arbitrary SMILES (e.g. paste a candidate)",
        full_width=True,
    )
    mo.vstack([mol_src, mol_pick, smi_box])
    return mol_pick, mol_src, smi_box


@app.cell
def _(
    Chem,
    Generate,
    PHARM_SIG,
    SH_EXPL,
    bit_label,
    mo,
    mol_pick,
    mol_src,
    np,
    smi_box,
):
    if mol_src.value == "dataset":
        _smi = mol_pick.value
    else:
        _smi = smi_box.value
    EXPL_MOL = Chem.MolFromSmiles(_smi)
    if EXPL_MOL is None:
        EXPL_BITINFO, EXPL_SV = {}, np.zeros(0)
        bit_sel = mo.ui.multiselect(
            options={"(no valid molecule)": ""},
            value=[],
            label="Pharmacophore bits to highlight",
            full_width=True,
        )
    else:
        _bi = {}
        _fp = Generate.Gen2DFingerprint(EXPL_MOL, PHARM_SIG, bitInfo=_bi)
        EXPL_BITINFO = _bi
        EXPL_SV = SH_EXPL.shap_values(np.asarray(_fp, np.float32).reshape(1, -1))[0]
        _on = sorted(
            ((int(_b), float(EXPL_SV[_b])) for _b in _bi if abs(EXPL_SV[_b]) >= 0.01),
            key=lambda _t: -abs(_t[1]),
        )
        _opts = {f"{bit_label(_b)}  (SHAP {_s:+.2f})": _b for _b, _s in _on[:30]}
        _fallback = {"(no pharmacophore bits above threshold)": ""}
        bit_sel = mo.ui.multiselect(
            options=_opts if _opts else _fallback,
            value=[],
            label="Pharmacophore bits to highlight (none selected = SHAP map only)",
            full_width=True,
        )
    bit_sel
    return EXPL_BITINFO, EXPL_MOL, EXPL_SV, bit_sel


@app.cell
def _(EXPL_BITINFO, EXPL_MOL, EXPL_SV, SH_EXPL, bit_label, bit_sel, mo, np):
    import matplotlib

    from rdkit.Chem import Draw, rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D
    from rdkit.Geometry import Point2D

    if EXPL_MOL is None:
        _view = mo.md("**Invalid SMILES** \u2014 try another string.")
    elif EXPL_MOL.GetNumAtoms() < 2:
        _view = mo.md("Molecule too small to contour \u2014 needs at least 2 atoms.")
    else:
        # net SHAP attribution distributed over the atoms of each ON bit
        _w = np.zeros(EXPL_MOL.GetNumAtoms())
        for _b, _occs in EXPL_BITINFO.items():
            for _occ in _occs:
                for _pt in _occ:
                    for _a in _pt:
                        _w[_a] += EXPL_SV[_b] / (len(_occs) * len(_occ))

        # atoms covered by the selected bits -> single shared highlight colour
        _hl = set()
        for _b in bit_sel.value:
            if _b != "":
                for _occ in EXPL_BITINFO[int(_b)]:
                    for _pt in _occ:
                        _hl.update(_pt)
        _hb = [
            _bond.GetIdx()
            for _bond in EXPL_MOL.GetBonds()
            if _bond.GetBeginAtomIdx() in _hl and _bond.GetEndAtomIdx() in _hl
        ]

        # inline the similarity-map drawing so highlights can be passed through
        _mol = rdMolDraw2D.PrepareMolForDrawing(EXPL_MOL, addChiralHs=False)
        if not _mol.GetNumConformers():
            rdDepictor.Compute2DCoords(_mol)
        _conf = _mol.GetConformer()
        if _mol.GetNumBonds() > 0:
            _b0 = _mol.GetBondWithIdx(0)
            _sigma = 0.3 * (
                _conf.GetAtomPosition(_b0.GetBeginAtomIdx())
                - _conf.GetAtomPosition(_b0.GetEndAtomIdx())
            ).Length()
        else:
            _sigma = 0.3 * (
                _conf.GetAtomPosition(0) - _conf.GetAtomPosition(1)
            ).Length()
        _locs = [
            Point2D(_conf.GetAtomPosition(_i).x, _conf.GetAtomPosition(_i).y)
            for _i in range(_mol.GetNumAtoms())
        ]
        _d2d = Draw.MolDraw2DCairo(450, 400)
        _ps = Draw.ContourParams()
        _ps.fillGrid = True
        _ps.gridResolution = 0.1
        _ps.extraGridPadding = 0.5
        _ps.setColourMap(
            [tuple(_c) for _c in matplotlib.colormaps["RdBu_r"]([0, 0.5, 1])]
        )
        _d2d.ClearDrawing()
        Draw.ContourAndDrawGaussians(
            _d2d,
            _locs,
            _w.tolist(),
            [round(_sigma, 2)] * _mol.GetNumAtoms(),
            nContours=5,
            params=_ps,
        )
        _d2d.drawOptions().clearBackground = False
        _d2d.drawOptions().highlightColour = (1.0, 0.7, 0.0)
        _d2d.DrawMolecule(_mol, highlightAtoms=sorted(_hl), highlightBonds=_hb)
        _d2d.FinishDrawing()

        _p = float(1 / (1 + np.exp(-(SH_EXPL.expected_value + EXPL_SV.sum()))))
        _head = mo.callout(
            mo.md(
                f"**Model p(TDI) = {_p:.0%}** \u2014 predicted probability this "
                "molecule behaves as a time-dependent inhibitor."
            ),
            kind="warn" if _p >= 0.5 else "neutral",
        )
        if _hl:
            _cap = mo.md(
                f"p(TDI) = **{_p:.0%}**. Red = pushed **toward** TDI, blue = away. "
                "Amber highlights the atoms of: "
                + "; ".join(bit_label(int(_b)) for _b in bit_sel.value if _b != "")
                + "."
            )
        else:
            _cap = mo.md(
                f"p(TDI) = **{_p:.0%}**. Red atoms are pushed **toward** TDI by the "
                "model, blue **away** \u2014 the per-atom sum of signed SHAP over every "
                "pharmacophore bit this molecule switches on. Select bits above to "
                "highlight (amber) where they sit."
            )
        _view = mo.vstack([_head, mo.image(_d2d.GetDrawingText(), width=520), _cap])
    _view
    return


if __name__ == "__main__":
    app.run()
