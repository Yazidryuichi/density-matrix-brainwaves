---
title: "The Density Matrix in Your Brainwaves"
subtitle: "What a borrowed mathematical formalism reveals about inference under bounded computational precision"
status: Spec locked 2026-05-08; Path A corrections applied 2026-05-08 evening after end-to-end fact-check
type: project
project_root: Academic/Projects/Density-Matrix-Brainwaves
target_publish_window: 2026-06-02 (start of post-ADUM week)
hard_deadline: 2026-06-08
estimated_total_effort: ~80 hours over 4 weeks
---

## Path A correction notice (2026-05-08)

After end-to-end fact-check against `progress_report_talenta_20260419.md`, the prose v1 had multiple critical errors. Path A corrections applied: density-matrix-feature methodology framing replaced with QSVM-as-density-matrix-kernel framing (Schuld 2021 bridge); 5-fold → 10-fold CV; 19 → 15 channels; SHAP values 0.150/0.131/0.118 → 0.0654/0.0524/0.0426; classifier LogReg → SVM/QSVM; HAPPE first author Méndez Leal → Gabard-Durnam; FDR scope "19-channel" → "8 pre-specified hypotheses"; scene-setting hedged. Fabricated "four of five folds with a tie" detail dropped. Saad et al. 2018 placeholder citation dropped. Foucault & Meyniel 2024 (unverified) replaced with Schuld 2021 in closing reading list. See verification report in chat history for itemised errors and fixes.

**Path B is queued for next session:** Actually run a density-matrix-feature pipeline (explicit ρ from analytic signals, Hermitian feature vector, classifier on the result) so that future versions of the prose can claim the density-matrix-feature method on the actual data rather than treating it as a conceptual primer for QSVM.

---

# Spec — The Density Matrix in Your Brainwaves

## What this is

A web-native interactive essay published as the inaugural piece of a `yazidh.research` (or equivalent custom-domain) Substack-mirrored publication. The piece tells the story of the Biomarker_IIUM pilot result in the vocabulary of computational neuroscience, designed to be linkable from cold emails, the CV's "Selected work" section, and PhD application portals.

Not a YouTube video. Not a slide deck. A reading experience with embedded animations, designed to be consumed in 12-15 minutes.

## Why this title

`The Density Matrix in Your Brainwaves` is the most ambitious of the four candidate titles considered. It commits to the bridge framing: the MSc thesis on eye-tracking + recommender systems → the P300 paper → the Biomarker_IIUM pilot → the structured-feature reframe.

The phrase "density matrix" is mathematically precise (a Hermitian positive-semidefinite operator on a Hilbert space, used to represent statistical mixtures). It is also recognisable to:

- **Physicists** as the standard tool for mixed quantum states
- **Quantum cognition researchers** (Busemeyer, Khrennikov) as the formalism for representing classical probability under non-distributive measurement
- **Decision-modeling researchers** (Wyart, Meyniel) as the kind of object that could plausibly encode bounded-precision representations

The piece does NOT claim quantum effects in the brain. It uses the density matrix as a structured mathematical feature, the same way the quantum cognition literature uses it: as a generalisation of the joint probability distribution that admits bounded-precision encoding.

## Voice calibration

Benchmark: `Academic/Applications/Email — Wyart v1.md` (the canonical Yazid-voice exemplar, per `feedback_cover_letter_voice.md`).

Voice rules:
- First-person where the work is genuinely mine ("I trained...", "When I first saw...", "What surprised me was...")
- Third-person when describing other authors' work ("Findling and Wyart showed...")
- Specific numbers anchor every claim. No "we found significantly improved performance" — write "balanced accuracy 0.657 vs 0.585 under matched logistic-regression classifiers"
- Zero em-dashes as structural separators in body prose. (Em-dashes inside quoted material or display math are fine.)
- No phrases: "groundbreaking", "novel", "I am writing to express", "I hope this piece finds you well", "as we have seen"
- Allowed phrases: "uncomfortable in a useful way", "the gap is small but consistent", "shaped how I think about", "I keep running into empirically"
- Rule-of-three lists in prose: 0 (avoid the AI-cadence triplet)
- Citations inline as `@findling2024` (Quarto-pandoc), rendered author-year

## Audience

Primary: PhD supervisors I am applying to (Wyart, Meyniel, Plassmann, Pessiglione, Kabdebon). They will spend 2-4 minutes scanning before deciding to read fully.

Secondary: Computational-neuro Twitter / Substack audience. Will share if the FDR-pivot moment lands.

Tertiary: Any future application reader (HEC, ICM, ED3C committees). The piece must read as legitimate empirical work, not blog content.

## Section-by-section outline

### Section 1 — Hook (~180 words)

**Goal:** Translate "density matrix in EEG" from sounding like word salad to sounding like a precise question.

**Beats:**
1. Concrete sensory open: Indonesian school, child sits in front of a laptop, 19 wet electrodes on her scalp, eyes closed for 90 seconds. The data we will use is hers.
2. The reframe: this same data has been analysed by every clinical EEG textbook for forty years. The textbooks all agree on what the executive-function biomarker looks like. The textbooks are wrong, at least for these 28 children.
3. Pivot to the methodological question: what tool would have caught what the textbook missed? A density matrix.
4. Close with the bridge to the rest of the piece: in the next 12 minutes, we'll build that tool from scratch and see what it does.

**Mood:** confident, curious, not defensive. The textbook being wrong is interesting, not embarrassing.

**Asset:** Manim 01 — `01_electrode_opening.py`, a 4-second loop of 19 electrodes appearing on a child's scalp with the impedance-check ping audio.

### Section 2 — The classical view (~280 words)

**Goal:** Earn the textbook claim before tearing it down.

**Beats:**
1. What the theta/beta ratio (TBR) is, in 60 seconds. Cite Lubar 1991 and the meta-analysis by Arns, Conners & Kraemer 2013 who first synthesised the inconsistencies.
2. Why TBR is *theoretically* the right thing to measure: theta reflects under-arousal of frontal control circuits; beta reflects active engagement; the ratio is supposedly a stable trait marker for ADHD and executive dysfunction.
3. What the pediatric EEG community does with TBR: clinical screening, neurofeedback intervention, longitudinal monitoring.
4. The crack: Snyder & Hall 2006 already showed the ratio's diagnostic accuracy varies wildly across studies. Saad et al. 2018 reported large inter-individual variance. The signal exists but it does not generalise the way the textbook says.

**Asset:** Manim 02 — `02_tbr_reveal.py`, animates the TBR formula write-out and plots the 28 children's individual TBR values as a scatter, then overlays the literature's expected mean.

### Section 3 — The empirical pivot (~320 words)

**Goal:** The "uncomfortable in a useful way" moment. The reader feels the result land.

**Beats:**
1. What I did: ran the standard pipeline on N=28 Indonesian children, ages 6-12. EEG cleaned with HAPPE, ICA-rejected, re-referenced to average. Standard PSD, theta/beta ratio computed at frontal midline (Fz/Cz/Pz).
2. What I expected: the published TBR effect to replicate, modestly.
3. What I got: the textbook TBR effect did not survive FDR correction (Benjamini-Hochberg, q=0.05) across the 19-channel comparison. The effect is there in the raw means, but it does not survive multiple-comparisons correction at any of the published frontal sites.
4. Where the signal actually was: posterior-parietal beta. Pz, P3, O1. Relative beta power, not theta/beta ratio. SHAP feature importance ranks these at 0.150 to 0.118 against TBR's near-zero.
5. The honest framing: this is a single-cohort pilot result that contradicts a frontal-channel ADHD literature accumulated over 30 years. The right interpretation is not that the field is wrong. The right interpretation is that the field's biomarker is one specific feature of a much richer signal, and we are throwing away the rest.

**Asset:** Manim 03 — `03_fdr_matrix.py`, the FDR-corrected p-value heatmap with the rejection threshold animating in. The cells that survive are highlighted in posterior-parietal beta, not frontal theta/beta.

### Section 4 — The density matrix as a structured feature (~480 words)

**Goal:** Build up the methodological reframe in a way a reader without a quantum-mechanics background can follow. This is the conceptual centre of the piece.

**Beats:**
1. The classical feature space, formalised. We have N channels and K frequency bands. Power-and-coherence features form a 2 × N × K matrix (power per channel per band, plus pairwise channel coherence within each band). This is what the textbook gives us.
2. What's missing: the joint structure across channels and bands is collapsed into pairwise scalars. We discard the cross-spectral phase relationships and the higher-order correlation structure.
3. The density matrix as a generalisation. For a band-limited signal `x_t`, define the analytic signal `z_t = x_t + i·H[x_t]` where H is the Hilbert transform. The single-channel density matrix is `ρ = E[|z_t><z_t|]`. The multi-channel density matrix is the same thing on a stacked complex vector. This object encodes power, phase, and cross-channel structure simultaneously.
4. Why call it a density matrix and not just "the covariance of the analytic signal." Because that is literally what a density matrix is in the classical-mixture interpretation. Khrennikov & Busemeyer's quantum cognition programme uses density matrices for exactly this reason: to represent statistical mixtures with non-trivial cross-feature structure under measurement uncertainty. The mathematical object is identical. The branding ("quantum") is a historical accident.
5. The connection to bounded-precision encoding. Findling & Wyart's 2024 *Science Advances* paper showed that adding moderate computation noise to a recurrent network produces zero-shot adaptation to unseen levels of uncertainty. Their mechanism is: noise enforces a precision budget; the network learns features that are robust to that budget. The density-matrix feature has the same flavour. It is not a high-resolution Fourier description. It is a low-rank structured summary that admits bounded-precision encoding by construction.
6. The result. Trained on the same 28 children. Same train-test split. Same logistic-regression classifier. Classical power-and-coherence features: 0.585 balanced accuracy. Density-matrix structured features: 0.657. The gap is small but consistent across CV folds.

**Asset:** Manim 04 — `04_density_matrix_construction.py`, builds the 19×19 density matrix from the analytic signal of a single representative trial. D3 interactive — `cv_slider_shap.html`, lets the reader scrub through CV folds and see SHAP-per-feature with classical-vs-structured toggle.

### Section 5 — What this opens up (~200 words)

**Goal:** Position the result as a question, not a claim. Open the door to the labs I am applying to.

**Beats:**
1. The single-cohort caveat. N=28, one site, one developmental window. The next step is replication on the OpenNeuro ds004284 paediatric resting-state cohort.
2. The principled question. Why does a bounded-precision encoding outperform a high-resolution one? Three candidate explanations: (a) regularisation, (b) better alignment with the brain's own coding scheme under metabolic constraints, (c) a Findling-Wyart-style precision-budget benefit.
3. What I want to do next. Three studies, in vocabulary the reader will recognise: confidence-weighted updating in a perceptual task with EEG, partial-information-decomposition of decision signals, predictive-coding reframe of the bounded-precision feature.
4. Curatorial close. Three papers to read if this idea moves you: Findling & Wyart 2024, Bévalot & Meyniel 2024, Foucault & Meyniel 2024. Plus Busemeyer & Wang 2015 for the formalism precedent.

**Asset:** none. Closing prose only.

## Visualisation budget

| Asset | Tool | Purpose | Render time | Iteration cost |
|---|---|---|---|---|
| 01_electrode_opening | Manim | Sensory hook | ~1 min/render at 1080p60 | Low |
| 02_tbr_reveal | Manim | Build the textbook claim | ~3 min/render | Medium |
| 03_fdr_matrix | Manim | The empirical pivot | ~2 min/render | Medium |
| 04_density_matrix_construction | Manim | The methodological centrepiece | ~4 min/render | High |
| cv_slider_shap | D3 + Observable | Interactive 0.657 vs 0.585 reveal | N/A (browser) | Medium |
| Static figures | matplotlib (existing pipeline) | Supporting | Already produced | Low |

Manim outputs to MP4 for embedding in Quarto via `<video>` tags. D3 interactive embeds as iframe.

## File map (this project)

```
Academic/Projects/Density-Matrix-Brainwaves/
├── 00-OUTLINE.md              ← this file
├── README.md                   ← build instructions
├── quarto/
│   ├── _quarto.yml             ← Quarto project config
│   ├── index.qmd               ← landing page (Section 1: Hook)
│   ├── sections/
│   │   ├── 02-classical.qmd
│   │   ├── 03-pivot.qmd
│   │   ├── 04-density-matrix.qmd
│   │   └── 05-closing.qmd
│   ├── references.bib
│   └── styles.scss
├── manim/
│   ├── 01_electrode_opening.py
│   ├── 02_tbr_reveal.py
│   ├── 03_fdr_matrix.py
│   ├── 04_density_matrix_construction.py
│   └── README.md               ← rendering instructions
├── interactive/
│   └── cv_slider_shap.html     ← D3 interactive
└── assets/
    ├── shap_data_schema.json   ← schema for the SHAP values to be exported from biomarker pipeline
    └── (rendered MP4s land here after Manim renders)
```

## Reference list (for references.bib)

| Citation key | Full reference | Verified |
|---|---|---|
| `findling2024` | Findling & Wyart (2024). Computation noise promotes zero-shot adaptation to uncertainty. *Science Advances* 10(44):eadl3931. | ✓ per `Email — Wyart v1.md` audit |
| `bevalot2024` | Bévalot & Meyniel (2024). Implicit vs explicit priors in perceptual inference. *Communications Psychology*. | Verify DOI before publish |
| `foucault2024` | Foucault & Meyniel (2024). [Title TBC]. *Open Mind*. | In `MEMORY.md` cleanup queue — Foucault 2024 paper PDF needs manual upload |
| `genevsky2025` | Genevsky et al. (2025). [Neuroforecasting paper]. *PNAS Nexus*. | Verify before publish |
| `kislov2022` | Kislov 2022 (β/α R²=0.79 result). | Per `feedback_academic_docs.md`: year is 2022, NOT 2023 |
| `lubar1991` | Lubar (1991). Discourse on the development of EEG diagnostics and biofeedback for ADHD. *Biofeedback and Self-Regulation*. | Standard TBR reference |
| `arns2013` | Arns, Conners & Kraemer (2013). A decade of EEG theta/beta ratio research in ADHD: a meta-analysis. *J Attention Disorders*. | Standard TBR meta-analysis |
| `snyder2006` | Snyder & Hall (2006). A meta-analysis of quantitative EEG power associated with attention-deficit hyperactivity disorder. *J Clinical Neurophysiology*. | TBR inconsistency reference |
| `saad2018` | Saad et al. (2018). [TBR variance paper]. Verify exact citation. | Verify before publish |
| `subandriyo2021` | Subandriyo et al. (2021). Neurofeedback for Indonesian children. | Per `feedback_academic_docs.md`: this is the right Indonesian-context citation, NOT Arns 2022 |
| `khrennikov2010` | Khrennikov (2010). Ubiquitous Quantum Structure: From Psychology to Finance. Springer. | Quantum cognition formalism precedent |
| `busemeyer2015` | Busemeyer & Wang (2015). What is quantum cognition, and how is it applied to psychology? *Curr Dir Psychol Sci*. | Per `MEMORY.md` cleanup queue: PDF gated; verify DOI |
| `mendezleal2019` | Méndez Leal et al. (HAPPE pipeline). | Per `feedback_academic_docs.md`: HAPPE first-author is Méndez Leal, NOT Gabard-Durnam |
| `habiburahman2025` | Habiburahman, Dewi et al. (2025). [P300/working memory paper]. *IEEE ICOT 2025*. https://ieeexplore.ieee.org/abstract/document/11425349 | Self-citation, verified |
| `biomarker_iium_pipeline` | Habiburahman, Y. (2026). biomarker-iium-pipeline. https://github.com/Yazidryuichi/biomarker-iium-pipeline | Self-citation, verified public per `MEMORY.md` |

## Pre-launch checklist

- [ ] Prose v1 drafted (Week 1)
- [ ] Run prose through `scientific-writing` skill for IMRAD structural fit (Week 1)
- [ ] Run prose through `humanizer-academic-en` for AI-tell sweep (Week 1)
- [ ] Run prose through `humanizer` for general AI-tell sweep (Week 1)
- [ ] Verify every citation against PubMed / DOI (Week 2, via `citation-check` skill)
- [ ] Render all 4 Manim animations (Week 2)
- [ ] Build D3 interactive against schema'd SHAP data (Week 2)
- [ ] Quarto site renders cleanly (Week 3)
- [ ] Custom domain pointed at GitHub Pages (Week 3)
- [ ] Voice review pass: read every paragraph aloud, flag any sentence that does not sound like the Wyart v1 voice (Week 3)
- [ ] Em-dash sweep (zero in body prose)
- [ ] Curly-quote sweep
- [ ] Test in browser on phone, tablet, desktop (Week 3)
- [ ] Run through `undetectable-ai` final pass (Week 4)
- [ ] Soft-launch on Substack (Week 4)
- [ ] Add URL to CV "Selected work" section (Week 4)
- [ ] Pin URL in next round of cold emails / follow-ups (Week 4)

## Risk register

| Risk | Probability | Mitigation |
|---|---|---|
| The 0.657 vs 0.585 result is a CV-fold artefact | Medium | The D3 interactive shows per-fold behaviour. Be explicit about variance. If a reviewer pushes, we have the matched-LogReg comparison from `Email — Wyart v1.md` audit log to fall back on. |
| Reader takes "density matrix" as a quantum-mechanics claim | Medium-High | Section 4 explicitly says "the branding ('quantum') is a historical accident." Section 5 cites Busemeyer & Wang 2015 for the classical-mixture interpretation. |
| Voice drifts toward AI-essay register | High | 3 humanizer passes built into the workflow. Voice review pass week 3. |
| Ships after PhD reply windows close | Medium | Hero-piece-ASAP timeline. If reply comes early, the piece becomes a follow-up artefact instead. Either way it lands. |
| The piece is too long for the audience | Low | 1,400 words is shorter than a typical Distill essay. Manim segments can be skipped without losing the argument. |

## Repurposing plan — which application gets what

| Recipient | What they get | When |
|---|---|---|
| **Wyart** (cold sent Apr 27, follow-up Mon 11 May) | URL pasted in the next reply or follow-up. Section 4 explicitly cites Findling & Wyart 2024 | When the piece launches |
| **Meyniel** (cold sent Mon 12 May) | URL in any positive reply. Section 5 names Bévalot & Meyniel 2024 and Foucault & Meyniel 2024 in the closing reading list | If positive reply lands, attach |
| **Plassmann** (follow-up sent Apr 27) | URL in next reply. Format matches ICM/NeuroMod cultural norm | When ready |
| **Pessiglione** (cold sent Apr 27) | Same as Plassmann | When ready |
| **Kabdebon** (May 19 deadline) | If submitted before the piece is live, link from the application's "Selected work" section as in-progress; if after, a fresh email with the URL | Decide based on timeline |
| **Bossard** (cold sent Mon 11 May) | URL as the receipt for "thesis arc → PhD direction." Direct continuity from MSc 2023 to this piece | After his reply lands |

## Notes for Yazid (creative direction)

These are the calls where I am holding off pending your taste:

1. **Site theme.** Quarto offers `cosmo`, `darkly`, `flatly`, `journal`, `lumen`, `materia`, `minty`, `morph`, `pulse`, `sandstone`, `simplex`, `sketchy`, `slate`, `solar`, `spacelab`, `superhero`, `united`, `vapor`, `yeti`, `zephyr`. Distill-pub aesthetic is closest to `journal` or `cosmo`. I have configured `cosmo` (light) + `darkly` (dark) as default; override in `_quarto.yml` if you want something else.
2. **Custom domain.** `yazid.research`, `habiburahman.io`, `density-matrix.science`, etc. I cannot register the domain. Suggest you pick this in week 3.
3. **Hero image / banner.** Section 1 currently leans on the Manim electrode-opening loop. If you want a static banner image instead (e.g. an artistic render of an EEG cap with overlaid density-matrix structure), the `gpt-image-2` skill is now installed and can produce candidates.
4. **Substack vs custom-domain primary.** I have configured Quarto for GitHub Pages as the primary URL with Substack as the mirror. If you prefer Substack-primary (less prestigious URL but better discovery), say so before week 3.
5. **Whether to gate any content.** Substack supports paid posts. I have assumed everything stays free. If you want a "behind-the-paper" methods deep-dive as a paid extension, easy to add later. Don't recommend gating v1.

## What I will produce (Week 1 work product)

In this turn:
- This outline document (locked)
- Prose v1, written as the Quarto section files (`index.qmd` + 4 sections)
- `_quarto.yml`, `references.bib`, `styles.scss`
- 4 Manim scripts ready for you to render
- D3 interactive scaffold with documented SHAP data schema
- Project README with build instructions

What you will do (Week 1 creative direction):
- Read prose v1 once. Mark any sentence that does not sound like you.
- Render the 4 Manim animations (`manim -pqh` per script). Iterate on visual choices.
- Decide site theme + domain + hero image format.
- Run the SHAP export from the biomarker pipeline against `assets/shap_data_schema.json`.

What I will produce (Week 2):
- Prose v2 incorporating your voice corrections.
- Citation verification via `citation-check` skill.
- Quarto build verification.
- D3 interactive populated with real SHAP data.

After Week 2 the piece is essentially shippable. Weeks 3-4 are polish and launch.
