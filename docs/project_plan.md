# Project Plan — OpenADMET TDI Mechanistic Investigation Notebook

Target: molab Notebook Competition #3 (deadline **2026-10-04 23:59 PST**, ~5.5 weeks).
Deliverables: **molab notebook link + short video explainer**. Unrunnable = disqualified.

## 0. Scoring strategy → design decisions

| Rubric (weight) | How we win it |
|---|---|
| Creativity & Impact (20) | Investigator narrative (prediction→explanation→hypothesis→design→experiment), matched-pair counterexample, falsifiable experiment card — a question-driven story, not a model demo |
| Interactivity & Workflow (20) | True marimo reactivity: every UI element drives downstream cells (compound selector → SOM highlight → clicked atom → metabolites → pose → analog re-analysis). Progressive disclosure |
| Design & Shareability (20) | Consistent epistemic visual language (**OBSERVED / PREDICTED / HYPOTHESIS / PROPOSED** badges), mo.md() framing, guided sections, opens on curated flagship example |
| Customization (20) | **Custom anywidget(s)**: (a) interactive clickable atom-map viewer emitting selected atom index into the reactive graph; (b) parent→metabolite pathway/diagram widget; (c) 3Dmol.js wrapper with heme-distance annotation. Purpose-built, not bolted-on |
| Code Quality (10) | Single self-contained `.py`, pinned deps via inline script metadata, deterministic caching, clean sectioned cells, runs end-to-end cold |
| Chemical Validity (10) | RDKit sanitization + explicit invalid-SMILES handling; transformations via vetted SMARTS templates; stereochemistry preserved; no train/test leakage claims; every mechanism stated as hypothesis |

## 1. Timeline (5 phases + buffer)

### Week 1 (Aug 27–Sep 2) — Research & case study selection
- [ ] Pin down exact OpenADMET TDI dataset source (HF dataset id, columns, labels, isoforms); load locally into workspace.
- [ ] Tool survey doc `docs/research/tools.md`: site-of-metabolism predictors (SMARTCyp-style RDKit rules, XenoSite web API, BioTransformer…), metabolite enumeration (reaction templates), bioactivation structural alerts (MDL/expert SMARTS set), protein-ligand options (existing PDB co-crystals of CYP3A4/2C9/2D6/1A2 vs. docking vs. AF server).
- Decision rules recorded: availability on molab runtime (network), license, latency, determinism.
- [ ] Precompute pilot: run SOM prediction over all TDI-positive compounds → rank **flagship candidate compounds** by story potential (interpretable motif, related analogs/matched pair in dataset).
- [ ] Set up repo skeleton: `notebooks/`, `src/`, `precompute/`, `docs/research/`.

**Gate G1:** chosen flagship compound + 2 backups, with printed evidence sheet (SOM probabilities, alert hits, dataset relatives).

### Week 2 (Sep 3–9) — Minimum scientific prototype (no 3D, no widgets yet)
- [ ] Core pipeline as tested pure functions in `src/`: parse → SOM ranking → transformation enumeration (atom-tracked) → bioactivation alert scan → verdict tiers (*low interest / potentially relevant / strong hypothesis*).
- [ ] Marble prototype notebook: plain `mo.ui` elements wired to the pipeline on the flagship compound. Ugly is fine.
- [ ] Anywidget #1 spike: clickable RDKit/SVG atom map returning `(atomIdx)` to python.

**Gate G2:** compound → SOM → metabolites → hypothesis card produces scientifically sensible output end-to-end. Run headless (`marimo run` / scripted exec) with zero errors.

### Week 3 (Sep 10–16) — Structural context + analog loop
- [ ] CYP complex approach finalized (prefer prepared PDB co-crystal of target isoform as base + ligand placement/scoring; fallback documented).
- [ ] Heme Fe–metabolic-site distance computed & displayed; 3Dmol.js anywidget (#3) integrated (rotation/zoom, highlight metabolic atom, measure distance).
- [ ] Medicinal chemistry layer: 3–5 rationale-explicit analogs from templated perturbations (block soft spot e.g. C→F, remove alert group, sterically shield, electronic tuning, redirect metabolism).
- [ ] Re-analysis loop on analogs incl. **metabolic switching** check (new liabilities surfacing elsewhere).

**Gate G3:** full scientific arc works live on ≥2 compounds (flagship + backup): hypothesis → analog → re-scoring consistent.

### Week 4 (Sep 17–23) — Narrative, polish, customization depth
- [ ] Full notebook narrative per spec §6–§17 (sections 1–12), epistemic badge system throughout, animated reversible-vs-MBI mini-diagram (section 2).
- [ ] Matched-pair optional feature wired in if a good pair exists near flagship.
- [ ] Design pass: headings, spacing, mo.md voice, defaults tuned so fresh-open looks great.
- [ ] Code-quality pass: docstrings, dead cells removed, cell ordering, dependency pins, no commented-out cruft.

**Gate G4:** runs cold in ≤ reasonable time on molab hardware; screenshot review of every section.

### Week 5 (Sep 24–30) — Harden & rehearse
- [ ] Cold-start drill: fresh clone → follow setup as a stranger → zero errors; cache fallback verified when remote compute unavailable.
- [ ] Edge cases invalid SMILES/salts/tautomer handling exercised; error states friendly, never silent.
- [ ] Record video explainer; write submission blurb; disclose AI assistance in-notebook (explicitly rewarded by organizers).
- [ ] Buffer days.

### Oct 1–4 — Freeze
- Final molab upload & link check on separate account/browser, submit before **Oct 4, 11:59 PM PST**.

## 2. Iterative development loop (how we work)

1. **Single source of truth**: `notebooks/tdi_dataset_explorer.py` is THE submission artifact; heavy logic lives in `src/openadmet_tdi/` while developing, gets folded/inlined or imported robustly before freeze.
2. **Precompute/cache contract** (`precompute/` → `data/cache/*.json|parquet`): expensive steps (bulk SOM scans, poses) happen offline; notebook reads cache by default, exposes opt-in live-compute toggles. Guarantees speed + reliability on molab.
3. **Milestone PRs, tiny steps**: each session ends with: change made → `marimo check .` green → headless run green → git commit (never auto-push without ask).
4. **Rendered review**: after each milestone you open `uv run marimo edit` locally (or `marimo.sh`) and react to visuals — you're the design judge; I iterate.
5. **Gates G1–G4 above**: no advancing until the gate passes; keeps us from polishing animations before science is right (spec §28 warns about this).
6. **Risk burn-down order** (biggest unknowns first): dataset shape → SOM tool viability → whether 3D adds real evidence → anywidget reliability → polish.

## 3. Top risks & mitigations

| Risk | Mitigation |
|---|---|
| External API unreachable/unlicensed on molab runtime | Everything important precomputed & committed to repo cache; remote calls strictly optional |
| Notebook fails cold on molab (deps mismatch) | Inline PEP-723 script metadata pins exact versions; wheel-size sanity check (rdkit et al.) early in Week 2 |
| Anywidget jank across molab sandbox | Prototype widget Week 2, not late; graceful degradation to static SVG fallback |
| Dataset labeling ambiguities (TDI definitions/units) | Resolved and documented in Phase 1; citations shown in-notebook |
| Scope creep (docking rabbit hole) | Timeboxed per spec §25; docking only if it strengthens hypothesis, never the headline |

## 4. Definition of done

Rubric table in §0 fully addressed AND spec §29 list (1–10) is true for a stranger opening the notebook, ending at: *"synthesize this analog, rerun the same TDI assay — decrease supports, unchanged weakens and we pivot to next-ranked pathway."*
