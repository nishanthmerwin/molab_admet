# OpenADMET TDI Mechanistic Investigation & Medicinal Chemistry Design Notebook

## 1. Project Overview

Build an interactive **marimo / molab notebook** that explores **cytochrome P450 time-dependent inhibition (TDI)** from the perspective of a medicinal chemist responding to an experimental result.

The notebook should deliberately **not** focus primarily on building the highest-performing TDI classifier.

Instead, begin with a more practical drug-discovery scenario:

> We have a promising compound. We ran a CYP TDI assay and discovered that it exhibits time-dependent inhibition. What should we do next?

The notebook should guide the user through a computational investigation designed to:

1. understand plausible mechanistic explanations for the observed TDI;
2. identify structural features and metabolic pathways that may contribute to the liability;
3. formulate testable mechanistic hypotheses;
4. propose medicinal-chemistry modifications that could reduce the liability;
5. evaluate whether those modifications are consistent with the proposed mechanism; and
6. recommend the **next experiment** that would most efficiently test the hypothesis.

The core philosophy is:

**Prediction → explanation → hypothesis → molecular design → experiment**

The notebook should demonstrate how computational tools can help a scientist decide **what to do next**, rather than stopping at a prediction or visualization.

---

# 2. Scientific Context

## The problem

Cytochrome P450 enzymes are responsible for the metabolism of many drugs and xenobiotics.

A compound may inhibit a CYP enzyme through conventional reversible inhibition. However, some compounds exhibit **time-dependent inhibition**, where inhibition becomes stronger following incubation with the enzyme.

One important mechanism underlying TDI is **metabolism-dependent enzyme inactivation**.

A simplified conceptual pathway is:

**Parent compound**

↓

**CYP-mediated metabolism**

↓

**Metabolite or reactive intermediate**

↓

**Interaction with the CYP enzyme**

↓

**Reduced CYP activity**

This creates a particularly interesting medicinal-chemistry problem.

The problematic molecular species may not simply be the compound that was synthesized. The CYP enzyme itself may transform the compound into a species responsible for the observed liability.

Therefore, understanding TDI can require reasoning about:

- molecular structure;
- sites of metabolism;
- CYP reaction chemistry;
- candidate metabolites;
- reactive intermediates;
- CYP binding geometry;
- enzyme mechanism;
- and medicinal-chemistry modifications.

This makes TDI a useful case study for **mechanistically informed computational drug design**.

---

# 3. Central Question

The notebook should revolve around one primary question:

> **Given a compound experimentally observed to exhibit CYP time-dependent inhibition, what mechanistic hypotheses could explain the observation, and what molecule or experiment should we try next?**

This framing is important.

We are **not** asking:

> Can we predict whether this molecule is TDI positive?

We already know the assay result.

Instead, we are asking:

> Why might this molecule behave this way, and how can we use that hypothesis to guide the next medicinal-chemistry decision?

---

# 4. Intended User Experience

The notebook should feel like an **interactive scientific investigation**.

The user should progressively move through several levels of evidence:

**Experimental observation**

→ **Molecular structure**

→ **Potential sites of metabolism**

→ **Candidate metabolic transformations**

→ **Potential reactive chemistry**

→ **Structural plausibility in the CYP active site**

→ **Mechanistic hypothesis**

→ **Medicinal-chemistry intervention**

→ **Re-analysis of proposed analogs**

→ **Experimental recommendation**

The notebook should progressively reveal complexity rather than showing everything simultaneously.

A user should be able to follow the story even without being an expert in CYP metabolism.

At the same time, the notebook should contain enough chemical detail to be scientifically interesting to medicinal chemists and computational chemists.

---

# 5. Critical Scientific Principle: Separate Evidence From Hypothesis

This distinction should be visible throughout the notebook.

Every major piece of information should conceptually fall into one of three categories.

### Observed

Experimental information.

Examples:

- compound structure;
- experimentally measured TDI status;
- assay target;
- experimental IC50 or other measurements when available.

### Predicted

Outputs produced by computational models.

Examples:

- predicted site of metabolism;
- predicted metabolite;
- predicted CYP binding pose;
- predicted protein-ligand complex.

### Hypothesized

Scientific interpretations constructed from the evidence.

Examples:

- a particular metabolic pathway could generate a reactive intermediate;
- this intermediate may contribute to enzyme inactivation;
- blocking a metabolic soft spot may reduce TDI;
- a particular analog may test the proposed mechanism.

The notebook must **never present a predicted mechanism as experimentally established fact**.

Ideally, the UI should visually distinguish:

**Observed | Predicted | Hypothesized**

This is both scientifically important and an opportunity for excellent notebook design.

---

# 6. Notebook Narrative

## Section 1 — The Medicinal Chemistry Problem

Begin with the scenario rather than the dataset.

For example:

> You are working on a promising lead compound.
>
> Its potency and other properties look encouraging.
>
> A CYP assay comes back with an unwanted result:
>
> **The compound exhibits time-dependent inhibition.**
>
> What do you do next?

Briefly explain why this matters.

Possible consequences include:

- altered clearance of co-administered drugs;
- drug-drug interaction risk;
- development complications;
- the need to understand whether the liability can be removed through medicinal chemistry.

Introduce the notebook's mission:

> Rather than building another TDI classifier, we will investigate an experimentally observed TDI compound and use computational tools to generate a hypothesis for what might be happening — and what experiment we should run next.

---

# 7. Section 2 — What Is Time-Dependent Inhibition?

Create a concise interactive explanation.

Contrast two conceptual scenarios.

### Conventional reversible inhibition

**Drug + CYP ⇌ CYP–drug complex**

Removing the drug allows enzyme activity to recover.

### Metabolism-dependent inhibition

**Drug**

→ CYP metabolism

→ reactive or inhibitory species

→ enzyme inactivation or persistent inhibition

Explain that TDI is not synonymous with one specific molecular mechanism. Multiple mechanisms can produce time-dependent behavior.

The notebook should therefore avoid assuming:

> TDI positive = reactive metabolite proven.

Instead:

> TDI provides an experimental clue that motivates mechanistic investigation.

A small animated diagram would work particularly well here.

---

# 8. Section 3 — Select a Real OpenADMET Case

Load the OpenADMET TDI dataset.

Allow the user to choose an experimentally TDI-positive compound.

Useful controls could include:

- CYP isoform;
- compound identifier;
- molecular structure;
- assay result;
- optional filtering by chemical scaffold or structural motif.

Display:

- 2D molecular structure;
- SMILES;
- relevant experimental values;
- CYP isoform;
- TDI label/result.

This establishes the **observed evidence**.

The remainder of the notebook should operate on this selected molecule.

---

# 9. Section 4 — Where Could CYP Metabolism Occur?

Run a **site-of-metabolism prediction** on the selected molecule.

The result should ideally assign probabilities or relative scores to candidate atoms.

Visualize the molecule in 2D with atoms colored according to predicted metabolic susceptibility.

For example:

- high probability = strongly highlighted;
- medium probability = moderately highlighted;
- low probability = weakly highlighted.

The user should be able to click an atom.

The UI might display:

> Atom 17  
> Predicted metabolism probability: 0.74  
> Likely transformation: aromatic hydroxylation

or:

> Atom 8  
> Potential N-dealkylation site

The important conceptual transition is:

**Where might CYP attack this molecule?**

---

# 10. Section 5 — What Could CYP Produce?

For the selected metabolic site, enumerate plausible CYP transformations.

Examples might include:

- hydroxylation;
- N-dealkylation;
- O-dealkylation;
- epoxidation;
- heteroatom oxidation;
- oxidative deamination;
- other appropriate CYP-mediated transformations.

Generate candidate metabolite structures.

Show the transformation visually:

**Parent → transformation → candidate metabolite**

Highlight exactly which atoms changed.

If multiple metabolites are plausible, display them as alternative branches rather than implying a single correct answer.

This section should make CYP metabolism visually understandable.

---

# 11. Section 6 — Could Any Pathway Explain the TDI Observation?

This is the major reasoning step.

For each plausible metabolic pathway, ask whether the resulting chemistry could plausibly contribute to time-dependent inhibition.

The system should inspect structural motifs and transformations associated with possible bioactivation.

The goal is **not** to automatically declare:

> This metabolite causes TDI.

Instead, construct hypotheses such as:

> CYP oxidation at this position could plausibly generate an electrophilic intermediate. This provides one possible mechanistic explanation for the experimental TDI observation.

Each pathway could receive a qualitative assessment such as:

**Low mechanistic interest**

**Potentially relevant**

**Strong hypothesis worth testing**

Every assessment should be accompanied by an explanation.

Where possible, identify:

- the relevant structural motif;
- predicted metabolic transformation;
- possible intermediate;
- why that intermediate may be chemically reactive;
- what interaction with the enzyme could theoretically occur.

---

# 12. Section 7 — Add the 3D Structural Context

Now move from 2D metabolism to the CYP active site.

Obtain a CYP–ligand complex using an appropriate structure-prediction or docking workflow.

If technically feasible, this could include calling an external structure-prediction API capable of predicting protein-ligand complexes.

Visualize the complex interactively in 3D.

Important visual elements:

- CYP protein;
- heme group;
- heme iron;
- ligand;
- predicted metabolic atom;
- distance between that atom and the heme/iron;
- nearby residues.

Allow rotation and zooming.

The critical question is:

> **Is the metabolic hypothesis geometrically plausible in the CYP active site?**

For example:

> Our site-of-metabolism model identifies carbon 17 as a likely oxidation site.
>
> In the predicted CYP complex, carbon 17 is positioned near the catalytic heme.
>
> These independent computational observations are therefore consistent with the proposed pathway.

Again, this is **supporting evidence**, not proof.

A predicted pose must be explicitly identified as predicted.

---

# 13. Section 8 — Build a Mechanistic Hypothesis

At this point, synthesize the investigation.

Present something resembling a **mechanistic evidence card**.

For example:

### Experimental observation

Compound X exhibits CYP3A4 time-dependent inhibition.

### Predicted metabolism

Carbon 17 is a high-probability metabolic site.

### Candidate transformation

Oxidation at carbon 17 could produce metabolite Y.

### Reactive chemistry hypothesis

Further transformation could generate intermediate Z, which has chemical characteristics consistent with potential enzyme inactivation.

### Structural context

The predicted CYP3A4 complex places carbon 17 near the catalytic heme.

### Working hypothesis

> Metabolism at carbon 17 may initiate a bioactivation pathway contributing to the experimentally observed CYP3A4 TDI.

### Confidence / uncertainty

Explicitly list what remains unknown.

This section should feel like the moment where disparate computational results become a **scientific hypothesis**.

---

# 14. Section 9 — Put on the Medicinal Chemist Hat

Now ask:

> **If this hypothesis is correct, how could we modify the molecule to test it?**

Generate several medicinal-chemistry strategies.

Examples:

### Block the metabolic soft spot

Modify the relevant position to make oxidation less favorable.

### Remove or replace the suspected structural alert

Replace a functional group implicated in the proposed bioactivation pathway.

### Sterically shield the metabolic site

Introduce substitution that makes productive CYP orientation less favorable.

### Alter electronics

Modify neighboring substituents to reduce susceptibility to oxidation.

### Redirect metabolism

Design an analog where metabolism is more likely to occur through a benign pathway elsewhere in the molecule.

The notebook should generate a **small number of interpretable analogs**, not a giant virtual library.

Perhaps 3–5 analogs.

Every analog must have an explicit rationale.

For example:

> **Analog A — metabolic blocking experiment**
>
> Change: C17 H → F
>
> Rationale: If oxidation at C17 drives the TDI mechanism, blocking oxidation here should reduce formation of the proposed reactive intermediate.

That rationale is more important than a generic predicted score.

---

# 15. Section 10 — Re-run the Investigation on the Proposed Analogs

For each proposed analog, repeat relevant computational analyses.

For example:

**Original**

Site A: 0.78  
Site B: 0.31  
Site C: 0.12

**Analog A**

Site A: 0.16  
Site B: 0.55  
Site C: 0.28

Now the notebook can ask:

> Did our intervention actually remove the suspected pathway?

This creates an iterative design loop:

**Identify liability**

→ **Form hypothesis**

→ **Design analog**

→ **Recompute metabolism**

→ **Inspect whether the hypothesis predicts the desired change**

An important consideration is **metabolic switching**.

Blocking one site may simply move metabolism somewhere else.

Therefore, the notebook should explicitly inspect whether new metabolic liabilities appear.

---

# 16. Section 11 — Compare Parent and Proposed Analog

Create a strong visual comparison.

### Parent

Show:

- structure;
- metabolic hotspots;
- proposed pathway;
- relevant 3D geometry;
- mechanistic concern.

### Analog

Show:

- highlighted structural modification;
- updated metabolic hotspots;
- whether the proposed pathway remains possible;
- any new liabilities.

Then summarize:

> This modification is predicted to substantially reduce metabolism at the hypothesized bioactivation site while preserving most of the parent scaffold.

Do **not** conclude:

> This analog will not exhibit TDI.

That remains an experimental question.

---

# 17. Section 12 — The Most Important Output: What Experiment Should We Run?

The notebook should deliberately end with an **experimental recommendation**, not a computational prediction.

Generate an **Experiment Card**.

For example:

## Proposed experiment

Synthesize Analog A and compare it directly with the parent compound.

### Hypothesis

Oxidation at C17 contributes to the observed CYP3A4 time-dependent inhibition.

### Perturbation

Block C17 metabolism through the proposed substitution.

### Experiment

Run the same CYP3A4 TDI assay on:

- parent compound;
- Analog A.

Optionally run metabolite-identification experiments to determine whether the predicted pathway disappears.

### Expected result if the hypothesis is correct

Analog A should exhibit reduced time-dependent inhibition relative to the parent.

### Result that would falsify the hypothesis

Analog A retains similar TDI despite suppression of the predicted metabolic pathway.

### Follow-up

If TDI remains, investigate the next-ranked metabolic pathway.

This is the endpoint of the notebook.

The computational analysis has produced a **falsifiable experimental hypothesis**.

---

# 18. Optional Feature — Matched Molecular Pair / Counterexample

An especially powerful extension would be to search the OpenADMET dataset for a structurally similar compound with a different TDI result.

For example:

**Compound A — TDI positive**

versus

**Compound B — TDI negative**

with only a small structural difference.

The notebook could ask:

> What changed?

Then compare:

- structures;
- metabolic hotspots;
- candidate metabolites;
- structural alerts;
- CYP poses.

This could provide experimental support for the proposed mechanistic interpretation.

A matched pair would be particularly compelling because it connects mechanistic reasoning back to **observed experimental data**.

---

# 19. Optional Feature — Literature Evidence

Where feasible, connect hypotheses to known CYP chemistry.

For a suspected bioactivation motif, show concise references explaining:

- known CYP transformations;
- known reactive intermediates;
- known mechanism-based inhibitor motifs;
- analogous medicinal-chemistry examples.

This should be presented as **supporting literature**, not as evidence that the selected compound necessarily follows the same mechanism.

---

# 20. UI / Visualization Goals

The notebook should showcase what an interactive scientific notebook can do beyond a conventional static analysis.

Potential interactive elements include:

- searchable compound selector;
- interactive 2D molecular structures;
- atoms colored by site-of-metabolism probability;
- clickable atoms;
- reaction pathway diagrams;
- parent → metabolite animations;
- interactive CYP 3D viewer;
- heme-distance measurements;
- toggles between parent and analog;
- side-by-side molecule comparison;
- matched-pair exploration;
- progressive disclosure of mechanistic reasoning;
- interactive experiment cards.

Avoid creating a giant dashboard.

The notebook should instead feel like a **guided scientific story**.

Each interaction should answer a question and naturally introduce the next question.

---

# 21. Proposed Visual Language

A recurring visual vocabulary should distinguish epistemic status.

For example:

### OBSERVED
Experimental evidence.

### PREDICTED
Computational result.

### HYPOTHESIS
Mechanistic interpretation.

### PROPOSED
Design or experiment that has not yet been tested.

Every major claim in the notebook should fit one of these categories.

This prevents the notebook from accidentally turning speculative mechanistic reasoning into apparent fact.

---

# 22. Technical Architecture

The notebook should be implemented using **marimo** and designed to run in **molab** where practical.

Potential components include:

### Data

OpenADMET TDI challenge dataset.

### Cheminformatics

RDKit for:

- molecule parsing;
- 2D depiction;
- atom highlighting;
- substructure analysis;
- reaction transformations;
- analog generation;
- similarity calculations.

### Site-of-metabolism prediction

Investigate suitable open or accessible tools for CYP site-of-metabolism prediction.

Requirements:

- ideally atom-level predictions;
- preferably CYP-specific predictions;
- callable programmatically;
- suitable licensing for a public notebook.

### Metabolite enumeration

Use reaction templates and/or an appropriate metabolite-prediction model to generate plausible CYP metabolites.

The notebook should retain the relationship:

**parent atom → reaction → product**

so transformations can be explained visually.

### Reactive-metabolite reasoning

Investigate:

- known structural alerts;
- CYP bioactivation reaction rules;
- literature-derived transformations;
- mechanistic rules;
- potentially model-assisted reasoning.

This component must remain conservative about uncertainty.

### Protein-ligand structure

Investigate external APIs or locally accessible tools for:

- CYP–ligand complex prediction;
- docking;
- Boltz-family structure prediction where appropriate.

### 3D visualization

Investigate:

- 3Dmol.js;
- py3Dmol;
- marimo-compatible molecular viewers;
- other WebGL-based protein visualization components.

The viewer should support atom highlighting and measurements to the heme.

---

# 23. Important Technical Constraint

The notebook should ideally remain useful even if expensive or remote computations cannot be run live.

Consider a hybrid architecture:

1. precompute expensive predictions for a curated collection of interesting compounds;
2. cache protein-ligand structures and metabolite predictions;
3. make notebook exploration completely interactive using cached outputs;
4. optionally allow advanced users to submit new calculations.

This may make the public notebook significantly faster and more reliable.

---

# 24. Compound Selection Strategy

Do not initially attempt to make every molecule equally compelling.

Find several **excellent case-study molecules**.

Prefer molecules that have:

- clear TDI-positive experimental results;
- interpretable chemistry;
- interesting predicted metabolic sites;
- plausible bioactivation pathways;
- structurally related compounds in the dataset;
- ideally related TDI-negative analogs.

The final notebook could provide free exploration, but its default state should open on a carefully selected example with a strong story.

---

# 25. What the Notebook Is NOT

Avoid turning the project into:

### A leaderboard model

Predictive performance is not the primary objective.

### A black-box mechanistic oracle

We cannot infer an experimentally proven TDI mechanism from structure alone.

### A generic chemical dashboard

Every visualization should contribute to the scientific argument.

### An analog generator

Generating hundreds of molecules without rationale defeats the purpose.

### A structure-prediction demo

3D structures should support the mechanistic question rather than becoming the entire project.

The notebook is fundamentally a **scientific hypothesis-generation workflow**.

---

# 26. Core Design Philosophy

The notebook should repeatedly ask:

> **What decision does this analysis enable?**

A site-of-metabolism prediction by itself is not the endpoint.

It enables:

> Which metabolic pathways should we investigate?

A candidate metabolite is not the endpoint.

It enables:

> Could this pathway plausibly explain our assay result?

A CYP pose is not the endpoint.

It enables:

> Is the proposed metabolism geometrically plausible?

A proposed analog is not the endpoint.

It enables:

> What perturbation would test our mechanistic hypothesis?

And a computational analysis is not the endpoint.

It enables:

> **What experiment should we run next?**

---

# 27. Ideal Final Story

The notebook should allow the user to experience something like this:

> **We experimentally know this compound exhibits CYP3A4 TDI.**
>
> We predict that CYP metabolism is particularly favorable at this part of the molecule.
>
> That metabolic transformation could lead to this candidate pathway.
>
> One branch of that pathway contains chemistry that could plausibly contribute to enzyme inactivation.
>
> Our predicted CYP3A4 complex places the implicated metabolic site near the catalytic heme, making the proposed pathway structurally plausible.
>
> Therefore, we hypothesize that metabolism at this position contributes to the observed TDI.
>
> We designed three analogs that perturb this hypothesis in different ways.
>
> One analog specifically blocks the suspected metabolic pathway while minimally altering the rest of the molecule.
>
> Computational re-analysis suggests that the targeted pathway is substantially reduced, although another metabolic site becomes somewhat more favorable.
>
> **Therefore, our next experiment is to synthesize this analog and run the same CYP3A4 TDI assay.**
>
> If TDI decreases, the result supports our hypothesis.
>
> If TDI remains unchanged, the hypothesis is weakened and we investigate another pathway.

That transformation —

**experimental observation → mechanistic reasoning → falsifiable experiment**

— is the central purpose of the project.

---

# 28. Initial Development Plan for the AI Agent

Do not attempt to implement the complete notebook immediately.

Work in phases.

## Phase 1 — Validate the scientific workflow

Research and document:

1. the exact OpenADMET TDI dataset structure;
2. available TDI measurements and labels;
3. CYP isoforms represented;
4. suitable site-of-metabolism prediction approaches;
5. metabolite-generation approaches;
6. methods for identifying plausible reactive-metabolite pathways;
7. CYP structures suitable for structural analysis;
8. protein-ligand prediction/docking options;
9. marimo-compatible 2D and 3D molecular visualization approaches.

For each external model or service, document:

- scientific purpose;
- input/output;
- availability;
- licensing;
- computational requirements;
- suitability for a public molab notebook.

Do not choose a tool merely because it is convenient.

## Phase 2 — Identify a compelling case study

Search the TDI-positive compounds for a molecule with an interpretable potential mechanism.

For promising candidates:

- inspect predicted sites of metabolism;
- generate plausible metabolites;
- search for known bioactivation motifs;
- search for related molecules;
- identify potential matched molecular pairs.

Select one excellent default example.

## Phase 3 — Build the minimum scientific prototype

Implement:

**compound → site of metabolism → candidate metabolites → mechanistic hypothesis**

Before adding 3D visualization or analog generation, verify that this part produces scientifically useful output.

## Phase 4 — Add structural context

Add:

**hypothesis → CYP complex → heme geometry**

Determine whether the 3D analysis adds useful evidence rather than simply attractive visualization.

## Phase 5 — Add medicinal-chemistry design

Implement:

**hypothesis → proposed structural perturbations → re-analysis**

Every proposed analog should explicitly test some aspect of the hypothesis.

## Phase 6 — Build the experimental endpoint

Generate the final experiment card containing:

- hypothesis;
- proposed molecule;
- rationale;
- assay;
- expected result;
- falsification criterion;
- next action.

## Phase 7 — Polish the interactive narrative

Only after the scientific workflow works should substantial effort go into animation, visual polish, transitions, and presentation.

---

# 29. Definition of Success

The notebook succeeds if a scientist can open it knowing relatively little about the project and, by the end, understand:

1. what CYP TDI is;
2. why it creates a medicinal-chemistry problem;
3. what is experimentally known about the selected compound;
4. where metabolism may occur;
5. what metabolites or reactive pathways might result;
6. why one pathway is mechanistically interesting;
7. whether structural modeling supports its plausibility;
8. what molecular modification could test the hypothesis;
9. what uncertainty remains;
10. and exactly **what experiment should be performed next**.

The final reaction should not be:

> “That's a cool prediction.”

It should be:

> **“I understand why we would make this molecule next, what experiment we'd run, and what we'd learn from the result.”**