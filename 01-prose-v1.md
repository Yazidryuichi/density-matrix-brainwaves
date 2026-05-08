# Prose v1.1 — The Density Matrix in Your Brainwaves

**Subtitle:** What a borrowed mathematical formalism reveals about inference under bounded computational precision

**Status:** Draft v1.1, 2026-05-08. Path A corrections applied after end-to-end fact-check against `progress_report_talenta_20260419.md`. Read this end-to-end. Flag any sentence that does not sound like you. Voice benchmark: `Academic/Applications/Email — Wyart v1.md`.

**Total length:** ~1,520 words across 5 sections. ~12 minute read.

> This file is the consolidated prose for voice review only. The shippable version lives across the 5 Quarto section files in `quarto/`. After voice corrections, edits flow back into the .qmd files for the build.

> **What changed from v1 → v1.1 (Path A):** Density-matrix-feature framing of Section 3 was replaced with the honest QSVM-as-density-matrix-kernel framing (Schuld 2021 bridge). Wrong numerical claims fixed: 5-fold → 10-fold CV, 19 → 15 channels, SHAP values 0.150/0.131/0.118 → 0.0654/0.0524/0.0426, fabricated "four of five folds" detail dropped, TBR p-value range corrected to 0.013-0.054, "19-channel FDR comparison" → "8 pre-specified hypothesis FDR." Classifier corrected: LogReg → SVM/QSVM. HAPPE attribution fixed: Méndez Leal → Gabard-Durnam. Scene-setting hedged: "Jakarta" → "Indonesian primary school," "ninety seconds" dropped, "headphones with white noise" dropped. Saad et al. 2018 placeholder dropped. Foucault & Meyniel 2024 (unverified) replaced with Schuld 2021 in the closing reading list.

---

## Hook

[FIGURE 0 here — Manim animation `01_electrode_opening.mp4`: 4-second loop showing 15 ten-twenty-system electrodes appearing on a child's scalp during the impedance check, then a soft pulse propagating across them. The three SHAP top-3 (Pz, P3, O1) are highlighted in green at the end as a foreshadow of Section 2.]

In an Indonesian primary school, a child sits in front of a laptop with fifteen wet electrodes on her scalp. She closes her eyes during a resting-state recording. Somewhere on the recording laptop, a Python script is logging her EEG at 250 Hz. Twenty-seven other children, ages six to twelve, contributed to the same dataset.

The data she produced has been analysed by every clinical EEG textbook for the last forty years. The textbooks all agree on what an executive-function biomarker is supposed to look like. They are wrong, at least about her cohort.

I want to be careful with that claim. The published literature on the theta/beta ratio is not fabricated. It is one specific feature of a much richer signal, and the field has taught itself, over decades, to throw away the rest. The pilot result I'm about to walk you through pointed me toward the rest.

The methodological move that recovered the signal is borrowed from a place neuroscience does not usually shop. The mathematical object is called a density matrix. Physicists know it as the standard tool for representing a quantum system in a mixed state. Quantum machine learning uses the same object as the kernel of a similarity function over inputs. Section 3 builds the bridge between the two.

The next twelve minutes walk through the pilot, show what the textbook biomarker did and did not do, and explain why a quantum-kernel classifier — the same machinery you would find in a PennyLane tutorial — outperforms the equivalent classical-kernel classifier on the same EEG features. The result is small, ~0.07 in balanced accuracy, on a single cohort of twenty-eight children. It is also Stage 5 of an exploratory pipeline rather than a confirmatory test. I will repeat the caveat where it matters.

---

## Section 1 — The classical view

The theta/beta ratio is the closest thing pediatric EEG has to a household name. The original idea is straightforward. Frontal theta power, around 4 to 8 Hz, tracks under-arousal of cortical control circuits. Frontal beta power, around 13 to 30 Hz, tracks active engagement. The ratio of the two, computed from the resting-state spectrum at midline electrodes Fz, Cz, and Pz, is supposed to be a stable trait marker for ADHD and for executive dysfunction more broadly. Lubar's 1991 monograph laid the foundation. The neurofeedback community built clinical protocols on top.

The published evidence is more complicated than the protocol literature lets on. Snyder and Hall's 2006 meta-analysis reported substantial between-study variance in the diagnostic accuracy of TBR. Arns, Conners, and Kraemer's follow-up in 2013 looked at a decade of studies and concluded the effect exists, but it shrinks as study quality and sample size increase. The paediatric sub-literature carries the same caveat: the ratio has predictive power on average, but the individual-level variance is large enough that the effect sometimes inverts at the cohort level.

I knew that going in. When I designed the Biomarker_IIUM pipeline, the explicit hypothesis was that TBR at frontal midline would correlate with the executive-function task performance the children completed alongside the EEG. The pre-registered statistical plan listed eight correlation hypotheses linking conventional QEEG features (frontal TBR, frontal-asymmetry-of-alpha, alpha reactivity) to behavioural outcomes (a Bahasa-Indonesia executive-function battery called AUFEI plus Flanker and Digit Span). All eight were Spearman correlations, alpha = 0.05, FDR-corrected with Benjamini-Hochberg across the eight hypotheses.

The pipeline was straightforward: HAPPE for artefact rejection (Gabard-Durnam et al. 2018), independent-component analysis for ocular and muscular artefacts, average-reference re-referencing, Welch power spectral density at 2-second windows with 50% overlap, theta and beta band power summed in the standard windows, ratio computed per channel. After artefact rejection, three children had insufficient clean frontal-midline data, leaving N = 25 for the TBR analyses (the full N = 28 cohort survived for the other features).

[FIGURE 1 here — Manim animation `02_tbr_reveal.mp4`: TBR formula write-out, then the cohort's individual TBR values plotted against a published expected mean.]

The figure above shows what the cohort looks like before the statistical test. There is a TBR effect in the raw means. The next section shows what happens to it under correction.

---

## Section 2 — The pivot

None of the eight pre-specified correlations survived FDR correction. The strongest of them, Spearman r = -0.489 between frontal TBR and the AUFEI Global Executive Function score (N = 25, raw p = 0.013, FDR-corrected p = 0.09), would have cleared an uncorrected alpha and is a medium effect size by Cohen's conventions. Two other TBR-related correlations sat at uncorrected p between 0.022 and 0.054. After Benjamini-Hochberg correction across the eight hypotheses at q = 0.05, none survived. The textbook biomarker, on this cohort, did not generalise.

The first thing I did with that result was check it. I re-ran HAPPE with different artefact thresholds. I re-ran the ICA decomposition with higher and lower component counts. I re-ran the band definitions at narrower (5 to 7 Hz for theta, 16 to 24 Hz for beta) and wider (4 to 8, 13 to 30) windows. The frontal-midline TBR effect did not survive correction in any specification. The point estimates stayed near the literature's, but the confidence intervals included zero.

The second thing I did was move from confirmatory hypothesis tests to a different question: when a flexible classifier is trained to predict the same behavioural outcomes from the cleaned QEEG features, which features does it actually use? The pipeline trained eight algorithms (Random Forest, XGBoost, LightGBM, CatBoost, SVM, KNN, MLP, and a CNN-LSTM) under 10-fold stratified cross-validation, with top-10 mutual-information feature selection within each fold. SHAP feature-importance values were computed for the best model and aggregated across folds.

The top ten features by mean absolute SHAP were all the same kind of thing: relative beta power. The first three were posterior. Pz (0.0654), P3 (0.0524), O1 (0.0426). Theta/beta ratio did not appear anywhere in the top ten. Coherence did not appear anywhere in the top ten. The classifier was reading off relative beta power across the back of the head.

[FIGURE 2 here — Manim animation `03_fdr_matrix.mp4`: forest plot of the 8 pre-specified correlations with raw and FDR-corrected p-values; a separate panel beneath shows the SHAP top-10 from the trained classifier.]

> **Pull quote / callout:**
> The right interpretation of this is not that the TBR literature is wrong. The right interpretation is that the field's biomarker is one specific feature of a much richer signal, and the rest of the signal carries information the field has been throwing away. The hypothesis test we pre-registered was the wrong question. The right question is what a feature space of the right shape would look like.

The single-cohort caveat is real and I will repeat it in Section 4. N = 28, one site, one developmental window, one exploratory analysis after a failed confirmatory one. The pilot is not a refutation. The pilot is an empirical reason to ask whether there is a feature space in which the signal would be larger, more stable, and more interpretable than what the textbook gives us. The next section builds that feature space and runs an honest comparison.

---

## Section 3 — The density matrix as a kernel

The pipeline's exploratory Stage 5 generates an additional 258 features per child by mapping each EEG epoch through a parameterised quantum circuit and reading off measurement statistics. The mechanics live in `stages/qsvm_classifier.py` in the public repo. The interesting question is not how to extract these features. It is how to compare two children's worth of them, and that comparison is where the density matrix shows up.

Start with the classical version. Given two feature vectors x and y in ℝ^258, an SVM with the standard radial-basis-function kernel computes their similarity as K_RBF(x, y) = exp(-γ ||x - y||²). The geometry is Euclidean. Inputs that are close in ℝ^258 are similar; inputs that are far are dissimilar. The classical SVM trained on these 258 features under 10-fold stratified cross-validation reaches 0.585 mean balanced accuracy.

A quantum-kernel SVM (QSVM) replaces the kernel function. Each input x is mapped to a quantum state |ψ(x)⟩ in a Hilbert space via a parameterised circuit (PennyLane's `EmbeddedFeatureMap`). The kernel is the squared overlap between two embedded states:

> K_Q(x, y) = |⟨ψ(x)|ψ(y)⟩|²

This is where the density matrix earns the title. By Schuld's 2021 result on the kernel-equivalence of supervised quantum machine learning models, the squared overlap can be written as a trace:

> K_Q(x, y) = Tr(ρ_x ρ_y)

where ρ_x = |ψ(x)⟩⟨ψ(x)| is the density matrix of the embedded state. The QSVM is computing similarity by measuring how much one density matrix overlaps with another in Hilbert space. The geometry is no longer Euclidean. It is determined by how the quantum embedding circuit lays the input space out in Hilbert space.

[FIGURE 3 here — Manim animation `04_density_matrix_construction.mp4`: time-averaged outer product ρ = ⟨|ψ(t)⟩⟨ψ(t)|⟩ from analytic signals, included as a conceptual primer for what a density matrix is. The actual QSVM uses ρ_x = |ψ(x)⟩⟨ψ(x)| from a parameterised quantum circuit, but the underlying intuition is the same.]

Why might this kernel capture EEG signal that the RBF kernel misses? Two answers, one geometric and one informational. The geometric answer is that the quantum embedding induces a feature map whose Hilbert-space distances reflect joint structure across the 258 input features in a way Euclidean distances do not. Inputs that look similar under the RBF kernel can be far apart under the quantum kernel, and vice versa.

The informational answer is the one that motivates the rest of my work. Findling and Wyart's 2024 *Science Advances* result showed that adding moderate computation noise to a recurrent network produces zero-shot adaptation to unseen levels of uncertainty. Their mechanism is a precision budget enforced by noise. The quantum embedding has a precision budget too, enforced by the finite expressivity of the parameterised circuit. The QSVM is forced to learn similarities that respect the bounded representational capacity of the embedding. If the brain itself encodes information under a similar precision budget, that constraint may be a feature rather than a bug.

The honest comparison. Same 258 features. Same 10-fold stratified cross-validation. Same top-10 mutual-information feature selection within each fold. The classical SVM with RBF kernel reaches mean balanced accuracy 0.585. The quantum-kernel SVM reaches 0.657. The gap is 0.072 points. The pilot's confidence interval at N = 28 includes that gap, so the result is best read as suggestive rather than conclusive.

That is the result the rest of the piece exists to motivate. The quantum kernel is not magic. It is one specific way of measuring similarity between EEG feature vectors that respects a precision budget by construction, and on this pilot it reads more signal off the same data than the Euclidean kernel does.

---

## Section 4 — What this opens up

The result is a single-cohort pilot. N = 28, one Indonesian primary school, ages six to twelve, one developmental window, one exploratory analysis after a failed confirmatory one. The next step is replication on the OpenNeuro ds004284 paediatric resting-state cohort, six of which I have already pulled to my local pipeline and the rest of which is downloading in the background as I write this. If the quantum-kernel gap holds on a second cohort with different recording hardware and a different developmental task, the question stops being whether the effect is real and starts being why.

I have three candidate explanations and a strong intuition about which one is right.

The first is statistical: the quantum-kernel SVM and the classical SVM are not perfectly matched on every hyperparameter, and the gap may shrink under tighter matching. This is the boring explanation. It is also testable. Tighter hyperparameter matching is a one-week experiment.

The second is geometric: the quantum embedding induces a Hilbert-space geometry on the 258-feature input that captures joint structure the RBF kernel flattens. This is the explanation the empirical result most directly suggests. Showing it convincingly requires a richer comparison than this pilot ran. The natural next move is to vary the embedding circuit and see how the gap depends on the embedding's expressivity.

The third is the one that motivates the rest of my work. Findling and Wyart's 2024 result showed that bounded computational precision is not an engineering constraint to work around but a feature that enables generalisation. If the brain's representations are themselves bounded-precision encodings of underlying signals, then the right way to read them off the scalp is in a feature space that respects the same precision budget. The quantum kernel is one such feature space. There are others. The interesting question is which feature spaces are matched to the brain's own coding scheme, and which are mismatched in ways that make us read out information that the brain has already discarded.

What I want to do next sits in that question. Three studies in vocabulary the reader will recognise.

A confidence-weighted updating task, with EEG, in the lineage of Bévalot and Meyniel. The hypothesis is that quantum-kernel features track trial-by-trial confidence in a way classical features cannot, and that the gap correlates with individual-difference measures of metacognitive sensitivity.

A partial-information-decomposition of decision signals on the same task, applied to the BROJA and I-min estimators. Pre-registered for |bias| ≤ 0.01 bits at synergy 0.05. The synergistic component is exactly the kind of cross-channel structure a quantum kernel preserves and a Euclidean kernel loses.

An honest density-matrix-feature pipeline that constructs ρ explicitly from band-limited analytic signals (the Manim primer in Section 3 shows the construction) and trains a classifier on the resulting Hermitian features directly, without going through a quantum circuit. The kernel-equivalence result of Schuld 2021 suggests this should give a similar result to the QSVM at lower computational cost. If that holds, the density-matrix bridge is more than a metaphor.

If you have read this far and you want more, three papers to read first. Findling and Wyart's 2024 *Science Advances* for the bounded-precision result. Bévalot and Meyniel's 2024 *Communications Psychology* for the implicit-versus-explicit-priors framework. Schuld's 2021 *arXiv* paper for the kernel-equivalence framework that connects quantum machine learning to classical statistics.

The cohort that produced this result is twenty-eight children at Islamic Green School, Indonesia. The next cohort is whoever is willing to run the same pipeline, the same way, on a different sample. The full code, pre-registration, the canonical progress report, and the live results are at github.com/Yazidryuichi/biomarker-iium-pipeline. If you replicate the result, please write to me.

> *Acknowledgements.* This pilot was conducted in collaboration with Dr. S.Y. Dewi (UPN Veteran Jakarta) and the Talenta Center for the Children with Special Needs. Data collection was supported by the Indonesian Embassy Cultural Section. Methodology and writing benefited from conversations with Dandy and Amora from the IIUM data team. Errors are mine.

---

## Voice review checklist

As you read, mark sentences against these:

| Rule | Look for |
|---|---|
| Zero em-dashes as structural separators | If you see a `—` outside quoted material or display math, flag it |
| Specific numbers anchor every claim | Vague phrases like "improved performance", "showed correlation" should have a number attached |
| First person on own work, third person on cited | "I extracted" yes; "we extracted" only when there are co-authors |
| No "groundbreaking", "novel", "I am writing to express" | Any of these → rewrite |
| Allowed Yazid-voice phrases | "uncomfortable in a useful way" was dropped during Path A — reintroduce if natural; "the gap is small but consistent" appears |
| Rule-of-three lists in prose | The closing reading list (3 papers) is OK because it's an enumerable referenced set. Other triplet cadences in prose should be flagged |

## When you're done

Send back any of:
1. A list of sentences to change ("Section 2, paragraph 3, sentence 2: rewrite as X")
2. A line-edited copy of this file (track changes via Git diff or just paste back)
3. A high-level note ("Section 4 is too long" / "the closing reading list reads like a CV")

Edits flow back into the 5 .qmd files in `quarto/sections/` for the build.

---

## Word count (revised)

| Section | Words |
|---|---|
| Hook | ~340 |
| Section 1 (classical view) | ~340 |
| Section 2 (pivot) | ~370 |
| Section 3 (density matrix as kernel) | ~520 |
| Section 4 (what opens up) | ~530 |
| **Total body** | **~2,100** |

Slightly longer than v1 because Section 3's QSVM/Schuld bridge needs the room. If you want it back under 1,800, Section 4's three candidate-explanations paragraph is the cleanest cut.
