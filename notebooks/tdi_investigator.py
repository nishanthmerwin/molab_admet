import marimo

__generated_with = "0.24.0"
app = marimo.App(app_title="CYP TDI Investigator (skeleton)")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(f"""
    # CYP Time-Dependent Inhibition Investigator
    ### *Skeleton — mocked pipeline, narrative per `docs/project_specs.md` §6–§17*

    **Mission:** start from an experimentally TDI-positive compound and walk the path
    **observation → explanation → hypothesis → molecular design → experiment**.

    This notebook is a **structural skeleton**: every computational step is a
    deterministic mock. Cells are already wired reactively — change the compound
    selection and everything downstream updates. Each section carries a
    **TODO callout** describing what replaces the mock.

    **Epistemic legend:**
    🔵 OBSERVED (experiment) · 🟠 PREDICTED (computation) · 🟣 HYPOTHESIS
    (mechanism) · 🟢 PROPOSED (design/experiment)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    _BADGE_STYLES = {
        "OBSERVED": ("#dbeafe", "#1e40af"),
        "PREDICTED": ("#fef3c7", "#92400e"),
        "HYPOTHESIS": ("#f3e8ff", "#6b21a8"),
        "PROPOSED": ("#dcfce7", "#166534"),
    }

    def badge(kind, text=""):
        _bg, _fg = _BADGE_STYLES[kind]
        _label = f"{kind} · {text}" if text else kind
        return mo.Html(
            f'<span style="background:{_bg};color:{_fg};padding:2px 8px;'
            f'border-radius:999px;font-size:0.75em;font-weight:700;'
            f'letter-spacing:0.03em">{_label}</span>'
        )

    def todo(msg, phase="Week 2"):
        return mo.callout(
            mo.md(f"**TODO ({phase}):** {msg}"), kind="warn"
        )

    return badge, todo


@app.cell(hide_code=True)
def _():
    import hashlib

    MOCK_COMPOUNDS = {
        "Placeholder-01": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
        "Placeholder-02": "CN1CCCC1c1cccnc1",
        "Placeholder-03": "CC(=O)Oc1ccccc1C(=O)O",
    }

    MOCK_ASSAY = {
        "Placeholder-01": {"isoform": "CYP3A4", "tdi": "positive", "note": "IC50 shift 4.1x (mock)"},
        "Placeholder-02": {"isoform": "CYP2D6", "tdi": "positive", "note": "IC50 shift 2.7x (mock)"},
        "Placeholder-03": {"isoform": "CYP2C9", "tdi": "positive", "note": "IC50 shift 3.3x (mock)"},
    }

    def mock_scores(smiles, n=5):
        """Deterministic placeholder 'model' output keyed to the structure."""
        digest = hashlib.sha256(smiles.encode()).digest()
        out = {}
        for i in range(min(len(smiles), 40)):
            out[i] = round(((digest[i % len(digest)] + 7 * i) % 100) / 100, 2)
        return dict(sorted(out.items(), key=lambda kv: -kv[1])[:n])

    return MOCK_ASSAY, MOCK_COMPOUNDS, mock_scores


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Section 1 — The Medicinal Chemistry Problem
    🔵 **OBSERVED**: a promising lead came back **TDI-positive** in a CYP assay.

    Consequences of ignoring it: drug–drug interaction risk, altered clearance of
    co-administered drugs, development complications.

    > Rather than building another TDI classifier, we investigate *this* compound,
    > generate a mechanistic hypothesis, and decide **what experiment to run next**.

    **TODO (narrative polish, Week 4):** scenario framing, `mo.md` voice, badge system.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Section 2 — What Is Time-Dependent Inhibition?

    **Reversible inhibition** — Drug + CYP ⇌ CYP·Drug — activity recovers on dilution.

    **Metabolism-dependent inhibition** — Drug → CYP metabolism → reactive species
    → enzyme inactivation — activity does *not* recover.

    ⚠️ TDI is a **clue**, not a mechanism: multiple mechanisms produce
    time-dependent behavior.

    **TODO (Phase 7 polish):** animated reversible-vs-MBI mini-diagram (plan §Week 4).
    """)
    return


@app.cell(hide_code=True)
def _(MOCK_COMPOUNDS, badge, mo, todo):
    compound_select = mo.ui.dropdown(
        options=list(MOCK_COMPOUNDS),
        value=next(iter(MOCK_COMPOUNDS)),
        label="TDI-positive compound",
    )
    mo.vstack(
        [
            mo.md("## Section 3 — Select a Real OpenADMET Case"),
            badge("OBSERVED", "mock dataset rows"),
            todo(
                "load the real OpenADMET TDI dataset (HF dataset id pinned in "
                "`docs/research/tools.md`); add isoform / scaffold filters and a "
                "searchable selector."
            ),
            compound_select,
        ]
    )
    return (compound_select,)


@app.cell(hide_code=True)
def _(MOCK_ASSAY, MOCK_COMPOUNDS, badge, compound_select, mo):
    compound_name = compound_select.value
    smiles = MOCK_COMPOUNDS[compound_name]
    assay = MOCK_ASSAY[compound_name]

    mo.vstack(
        [
            badge("OBSERVED", "experimental record"),
            mo.md(
                f"""
                **Compound:** `{compound_name}`
                **SMILES:** `{smiles}`

                | isoform | TDI result | detail |
                |---|---|---|
                | {assay["isoform"]} | {assay["tdi"]} | {assay["note"]} |
                """
            ),
        ]
    )
    return compound_name, smiles


@app.cell(hide_code=True)
def _(badge, mo, mock_scores, smiles, todo):
    mo.vstack(
        [
            mo.md("## Section 4 — Where Could CYP Metabolism Occur?"),
            badge("PREDICTED", "site-of-metabolism model"),
            todo(
                "swap `mock_scores` for a real SOM predictor (SMARTCyp-style RDKit "
                "rules / XenoSite / BioTransformer — see `docs/research/tools.md`) and "
                "render a 2D depiction with atoms colored by probability."
            ),
            mo.md(
                "Top predicted sites (atom index → probability, **mock**): "
                + ", ".join(f"`{i}` → {p:.2f}" for i, p in mock_scores(smiles).items())
            ),
        ]
    )
    som = mock_scores(smiles)
    return (som,)


@app.cell(hide_code=True)
def _(badge, mo, som, todo):
    _atom_options = {f"atom {i} (p={p:.2f})": i for i, p in som.items()}
    atom_select = mo.ui.dropdown(
        options=_atom_options,
        value=next(iter(_atom_options)),
        label="Metabolic site (placeholder for clickable-atom anywidget)",
    )
    mo.vstack(
        [
            badge("PREDICTED", "atom-level ranking"),
            todo(
                "replace dropdown with Anywidget #1: clickable RDKit/SVG atom map "
                "emitting `(atomIdx)` into the reactive graph.",
                phase="Week 2",
            ),
            atom_select,
        ]
    )
    return (atom_select,)


@app.cell(hide_code=True)
def _(atom_select, badge, mo, smiles, todo):
    atom_idx = atom_select.value

    def mock_metabolites(smi, idx):
        return [
            {
                "pathway": f"hydroxylation @ atom {idx}",
                "product": f"{smi}+O (mock)",
                "verdict": "Potentially relevant",
                "why": " oxidation could expose a soft spot",
            },
            {
                "pathway": f"N-dealkylation @ atom {idx}",
                "product": "fragment A (mock)",
                "verdict": "Low mechanistic interest",
                "why": " benign, stable product",
            },
            {
                "pathway": f"epoxidation @ atom {idx}",
                "product": "epoxide (mock)",
                "verdict": "Strong hypothesis worth testing",
                "why": " electrophilic intermediate plausible",
            },
        ]

    candidates = mock_metabolites(smiles, atom_idx)
    mo.vstack(
        [
            mo.md("## Section 5 — What Could CYP Produce?"),
            badge("PREDICTED", "metabolite enumeration"),
            todo(
                "enumerate real metabolites via reaction SMARTS templates; retain "
                "parent atom → reaction → product provenance for the reaction diagram."
            ),
            mo.md(
                f"Parent → transformation → candidate metabolites for **atom {atom_idx}** "
                "(*branches, not a single truth*):"
            ),
        ]
    )
    return atom_idx, candidates


@app.cell(hide_code=True)
def _(badge, candidates, compound_name, mo, todo):
    pathway_table = mo.ui.table(
        data=[
            {
                "pathway": c["pathway"],
                "candidate metabolite": c["product"],
                "assessment": c["verdict"],
                "rationale": c["why"],
            }
            for c in candidates
        ],
        selection=None,
    )
    mo.vstack(
        [
            mo.md("## Section 6 — Could Any Pathway Explain the TDI Observation?"),
            badge("HYPOTHESIS", "bioactivation reasoning"),
            todo(
                "replace mock tiers with a vetted structural-alert SMARTS set + "
                "explanations tied to motif / transformation / intermediate / enzyme "
                "interaction; every tier must ship with a written rationale."
            ),
            mo.md(f"Qualitative pathway assessment for `{compound_name}` (**mock**):"),
            pathway_table,
        ]
    )
    return


@app.cell(hide_code=True)
def _(atom_idx, badge, mo, todo):
    heme_distance = 4.2  # Å — MOCK
    mo.vstack(
        [
            mo.md("## Section 7 — Add the 3D Structural Context"),
            badge("PREDICTED", "CYP–ligand complex"),
            todo(
                "prepared PDB co-crystal of the target isoform + ligand placement; "
                "3Dmol.js anywidget with heme-distance annotation. Fallback documented "
                "in `docs/research/tools.md`.",
                phase="Week 3",
            ),
            mo.md(
                f"""
                **Is the metabolic hypothesis geometrically plausible?**

                Predicted complex would place **atom {atom_idx}** near the catalytic heme.
                Mock heme Fe–atom distance: **{heme_distance} Å** — consistent with
                productive oxidation, *supporting evidence, not proof*.
                """
            ),
        ]
    )
    return (heme_distance,)


@app.cell(hide_code=True)
def _(atom_idx, candidates, compound_name, heme_distance, mo):
    top = candidates[0]
    mo.vstack(
        [
            mo.md("## Section 8 — Build a Mechanistic Hypothesis"),
            mo.md(
                f"""
                ### Evidence card — `{compound_name}`

                | | |
                |---|---|
                | 🔵 **Observed** | {compound_name} is TDI-positive |
                | 🟠 **Predicted SOM** | atom {atom_idx} is a high-probability metabolic site |
                | 🟠 **Candidate transformation** | {top["pathway"]} → {top["product"]} |
                | 🟠 **Structural context** | predicted heme distance {heme_distance} Å |
                | 🟣 **Working hypothesis** | metabolism at atom {atom_idx} may initiate a bioactivation pathway contributing to the observed TDI |

                **Uncertainties:** real metabolite identity unverified; pose is predicted;
                alternative pathways remain open.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(MOCK_ASSAY, atom_idx, badge, compound_name, mo, todo):
    MOCK_ANALOGS = [
        {
            "name": "Analog A — block soft spot",
            "change": f"atom {atom_idx}: H → F",
            "rationale": f"If oxidation at atom {atom_idx} drives TDI, blocking it should suppress the proposed reactive intermediate.",
        },
        {
            "name": "Analog B — remove alert group",
            "change": "replace suspected motif with bioisostere (mock)",
            "rationale": "Removes the structural alert implicated in the bioactivation hypothesis.",
        },
        {
            "name": "Analog C — redirect metabolism",
            "change": "add remote metabolic handle (mock)",
            "rationale": "Shifts metabolism to a benign site, testing metabolic switching.",
        },
    ]
    analog_select = mo.ui.dropdown(
        options=[a["name"] for a in MOCK_ANALOGS],
        value=MOCK_ANALOGS[0]["name"],
        label="Proposed analog",
    )
    mo.vstack(
        [
            mo.md(f"## Section 9 — Medicinal Chemistry Strategies for `{compound_name}`"),
            badge("PROPOSED", "untested designs"),
            todo(
                "generate 3–5 analogs from templated perturbations via RDKit "
                "(block soft spot, remove alert, sterically shield, electronic tuning, "
                "redirect); every analog keeps an explicit rationale.",
                phase="Week 3",
            ),
            mo.md(f"Target isoform: **{MOCK_ASSAY[compound_name]['isoform']}**"),
            analog_select,
        ]
    )
    return MOCK_ANALOGS, analog_select


@app.cell(hide_code=True)
def _(MOCK_ANALOGS, analog_select, badge, mo, mock_scores, smiles, todo):
    selected_analog = next(
        a for a in MOCK_ANALOGS if a["name"] == analog_select.value
    )
    rescored = mock_scores(smiles + selected_analog["change"], n=3)
    switching = list(rescored)[0]
    _sites = ", ".join(f"`{i}` → {p:.2f}" for i, p in rescored.items())
    mo.vstack(
        [
            mo.md("## Section 10 — Re-run the Investigation on the Analog"),
            badge("PREDICTED", "re-analysis"),
            todo(
                "re-run the real SOM predictor on each analog and check **metabolic "
                "switching**: did the intervention remove the pathway, or move it?",
                phase="Week 3",
            ),
            mo.md(
                f"""
                **Change:** {selected_analog["change"]} — *Rationale:* {selected_analog["rationale"]}

                Top re-scored sites (**mock**): {_sites}

                ⚠️ New top site `atom {switching}` — check whether a new liability appeared.
                """
            ),
        ]
    )
    return (selected_analog,)


@app.cell(hide_code=True)
def _(badge, mo, selected_analog, smiles, todo):
    mo.vstack(
        [
            mo.md("## Section 11 — Parent vs. Analog"),
            badge("PROPOSED", "side-by-side comparison"),
            todo(
                "2D depiction pair with highlighted modification + hotspot maps; toggle "
                "parent/analog; explicitly avoid claiming 'analog will not show TDI'.",
                phase="Week 3",
            ),
            mo.md(
                f"""
                | | Parent | {selected_analog["name"]} |
                |---|---|---|
                | SMILES (mock) | `{smiles}` | `{smiles} + edit` |
                | Suspected pathway | active | **predicted reduced** |
                | New liabilities | — | check Section 10 |

                > This modification is *predicted* to reduce metabolism at the
                > hypothesized bioactivation site while preserving the parent scaffold.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(MOCK_ASSAY, atom_idx, badge, compound_name, mo, selected_analog, todo):
    isoform = MOCK_ASSAY[compound_name]["isoform"]
    mo.vstack(
        [
            mo.md("## Section 12 — What Experiment Should We Run Next?"),
            badge("PROPOSED", "falsifiable experiment"),
            todo(
                "auto-generate the experiment card from the live hypothesis state "
                "(hypothesis, perturbation, assay, expected result, falsification "
                "criterion, follow-up).",
                phase="Week 3",
            ),
            mo.md(
                f"""
                ### 🧪 Experiment Card

                | | |
                |---|---|
                | **Hypothesis** | oxidation at atom {atom_idx} contributes to {compound_name}'s {isoform} TDI |
                | **Perturbation** | {selected_analog["change"]} |
                | **Experiment** | synthesize {selected_analog["name"]}; run the same {isoform} TDI assay on parent + analog |
                | **Expected if correct** | analog shows reduced TDI vs. parent |
                | **Falsification** | analog retains TDI despite the blocked pathway |
                | **Follow-up** | if TDI persists, test the next-ranked pathway (Section 6) |
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    **Skeleton status:** all pipeline steps mocked & deterministic; reactive chain
    fully wired. Run locally: `./scripts/marimo.sh` (defaults to this notebook;
    editor reloads on external edits via `--watch`).
    """)
    return


if __name__ == "__main__":
    app.run()
