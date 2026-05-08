# The Density Matrix in Your Brainwaves

A web-native interactive essay published as the inaugural piece of a Substack-mirrored academic publication. The piece walks through a 28-child EEG biomarker pilot result, the methodological reframe that recovered the signal, and the open question it points toward.

**Status:** v1.1 shippable as of 2026-05-09. Prose (Path A + B + Tier 1 polish), citation ecosystem (β), and three tiers of interactivity (A: progress bar, number chips, navbar dots, notation glossary, badge rows, reduced-motion guard; B: Vega-Lite AUC chart, equation expander, sticky pivot-callout, floating next-CTA, density-matrix panel PNG; C: Manim hero loop, live D3 ρ_b heatmap, Plotly kernel-MDS scatter, CV-fold slider iframe) all shipped. GitHub Pages auto-deploy via `.github/workflows/publish.yml`.

**Spec:** see [`00-OUTLINE.md`](./00-OUTLINE.md). That doc is the source of truth.

## File map

```
.
├── 00-OUTLINE.md                  ← spec doc (read first)
├── README.md                      ← this file
├── quarto/                        ← the actual essay
│   ├── _quarto.yml                  Quarto site config
│   ├── index.qmd                    Section 1: Hook
│   ├── sections/
│   │   ├── 02-classical.qmd         Section 2: The classical view (TBR)
│   │   ├── 03-pivot.qmd             Section 3: The empirical pivot (FDR failure)
│   │   ├── 04-density-matrix.qmd    Section 4: Density-matrix structured features
│   │   └── 05-closing.qmd           Section 5: What this opens up
│   ├── references.bib               BibTeX citations
│   └── styles.scss                  Custom Distill-inspired theme
├── manim/                         ← 4 set-piece animations
│   ├── 01_electrode_opening.py
│   ├── 02_tbr_reveal.py
│   ├── 03_fdr_matrix.py
│   ├── 04_density_matrix_construction.py
│   └── README.md                    rendering instructions
├── interactive/
│   └── cv_slider_shap.html        ← D3 cross-validation slider
└── assets/
    ├── shap_data_schema.json      ← schema for the SHAP export
    └── (rendered MP4s land here)
```

## Build

### Prerequisites (one-time)

```bash
# Quarto (the essay engine)
brew install --cask quarto
quarto --version  # ≥ 1.4

# Manim (the animation engine)
conda create -n density-matrix python=3.11 -y
conda activate density-matrix
pip install manim==0.18.* numpy scipy
brew install pango cairo ffmpeg  # macOS system deps
```

### Render the Manim animations

See [`manim/README.md`](./manim/README.md) for full instructions. Short version:

```bash
cd manim/
manim -pqh 01_electrode_opening.py ElectrodeOpening
manim -pqh 02_tbr_reveal.py TBRReveal
manim -pqh 03_fdr_matrix.py FDRMatrix
manim -pqh 04_density_matrix_construction.py DensityMatrixConstruction

# Move outputs into ../assets/ where Quarto expects them
mv media/videos/01_electrode_opening/1080p60/ElectrodeOpening.mp4 ../assets/01_electrode_opening.mp4
mv media/videos/02_tbr_reveal/1080p60/TBRReveal.mp4 ../assets/02_tbr_reveal.mp4
mv media/videos/03_fdr_matrix/1080p60/FDRMatrix.mp4 ../assets/03_fdr_matrix.mp4
mv media/videos/04_density_matrix_construction/1080p60/DensityMatrixConstruction.mp4 ../assets/04_density_matrix_construction.mp4
```

### Export SHAP data for the D3 interactive

The chart at the end of Section 4 reads `assets/shap_data.json` (NOT in git yet — needs to be generated).

The schema is documented in [`assets/shap_data_schema.json`](./assets/shap_data_schema.json). Export from the biomarker pipeline as:

```python
# In biomarker-iium-pipeline (or in a notebook that imports its CV results)
import json
import shap

# After training the matched classical and structured LogReg classifiers under
# 5-fold StratifiedKFold cross-validation:

export = {
    "classical_mean": float(np.mean(classical_balacc_per_fold)),
    "structured_mean": float(np.mean(structured_balacc_per_fold)),
    "folds": [],
}

for fold_idx in range(5):
    classical_explainer = shap.LinearExplainer(classical_models[fold_idx], classical_X_train[fold_idx])
    structured_explainer = shap.LinearExplainer(structured_models[fold_idx], structured_X_train[fold_idx])

    classical_shap_abs = np.abs(classical_explainer.shap_values(classical_X_test[fold_idx])).mean(axis=0)
    structured_shap_abs = np.abs(structured_explainer.shap_values(structured_X_test[fold_idx])).mean(axis=0)

    top_classical = sorted(
        [{"name": classical_feature_names[i], "shap": float(classical_shap_abs[i])} for i in range(len(classical_shap_abs))],
        key=lambda x: -x["shap"],
    )[:20]
    top_structured = sorted(
        [{"name": structured_feature_names[i], "shap": float(structured_shap_abs[i])} for i in range(len(structured_shap_abs))],
        key=lambda x: -x["shap"],
    )[:20]

    export["folds"].append({
        "fold": fold_idx + 1,
        "classical": float(classical_balacc_per_fold[fold_idx]),
        "structured": float(structured_balacc_per_fold[fold_idx]),
        "top_features_classical": top_classical,
        "top_features_structured": top_structured,
    })

with open("assets/shap_data.json", "w") as f:
    json.dump(export, f, indent=2)
```

Until that file is generated, the D3 chart falls back to synthetic placeholder data (still illustrative; see `interactive/cv_slider_shap.html` `SYNTHETIC` constant).

### Build the Quarto site

```bash
cd quarto/
quarto preview          # local dev server with live reload
quarto render           # production build → _site/
```

`_site/` is what gets pushed to GitHub Pages.

## Voice calibration

All prose follows the voice rules locked in [`00-OUTLINE.md`](./00-OUTLINE.md#voice-calibration). Benchmark exemplar: `Academic/Applications/Email — Wyart v1.md`.

Quick-reference rules:
- First-person on own work, third-person on cited work
- Specific numbers anchor every claim
- Zero em-dashes as structural separators in body prose
- No "groundbreaking", no "I am writing to express", no rule-of-three lists in prose
- Allowed phrases: "uncomfortable in a useful way", "the gap is small but consistent"

Pre-publish, the prose passes through three skills in sequence:

```bash
# 1. Structural / IMRAD fit
# Use: scientific-writing skill (review pass on each .qmd file)

# 2. AI-tell sweep (academic register)
# Use: humanizer-academic-en skill

# 3. Final detection sweep
# Use: undetectable-ai skill
```

## Open creative-direction calls (Yazid decides)

These are flagged in [`00-OUTLINE.md`](./00-OUTLINE.md#notes-for-yazid-creative-direction). Summary:

1. **Site theme.** Currently `cosmo` (light) + `darkly` (dark) with custom `styles.scss`. Override in `_quarto.yml` if you want something else.
2. **Custom domain.** Suggested: `density-matrix.science`, `yazid.research`, `habiburahman.io`. Pick + register before week 3.
3. **Hero banner.** Section 1 uses the Manim electrode-opening loop. If you want a static banner instead, the `gpt-image-2` skill is installed and can produce candidates.
4. **Substack vs custom-domain primary.** Currently configured for GitHub Pages primary, Substack mirror. Reverse if you prefer.
5. **Whether to gate any content.** Currently free. Don't recommend gating v1.

## Deploy

Auto-publishes to GitHub Pages on every push to `main` via `.github/workflows/publish.yml`. The workflow installs Quarto 1.9.37, runs `quarto render` against `quarto/`, and pushes the rendered `_site/` to the `gh-pages` branch.

Public URL: <https://yazidryuichi.github.io/density-matrix-brainwaves>.

To activate Pages on the repo (one-time, after the first push):

```bash
gh repo edit Yazidryuichi/density-matrix-brainwaves \
  --enable-issues=true --enable-wiki=false
gh api -X PATCH repos/Yazidryuichi/density-matrix-brainwaves/pages \
  -f source.branch=gh-pages -f source.path=/
```

To preview locally before pushing:

```bash
~/.local/quarto/bin/quarto render quarto/
( cd quarto/_site && python3 -m http.server 8765 )
open http://127.0.0.1:8765/
```

To wire a custom domain (`density-matrix.science` / `habiburahman.io`) once registered:

1. Set the `A`/`AAAA`/`CNAME` records to GitHub Pages per <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site>.
2. Commit a `CNAME` file containing the domain at `quarto/CNAME` (or update the workflow to inject it).
3. Update `quarto/_quarto.yml`'s `site-url` field to the custom domain.
4. Wait for Pages to issue the HTTPS certificate.

## Build artefacts (data assets)

The widgets in Section 3 fetch three JSON files at runtime, all generated locally and committed to `quarto/assets/`:

- `density_matrix_data.json` (37 KB) — cohort-mean |ρ_b| + phase + diag for the D3 heatmap.
- `kernel_mds_data.json` (3 KB) — 2D MDS coordinates under HS-kernel and flat-feature kernel for the Plotly scatter.
- `shap_data.json` (22 KB) — per-fold (10×10 averaged) BAcc + top-feature importance for the CV slider iframe.

Build scripts live at `~/Desktop/Second Brain/Academic/Applications/scripts/`:

- `build_density_matrix_heatmap.py` — needs `pipeline/results/density_matrices.npz`.
- `build_kernel_mds_data.py` — needs the same NPZ + `density_matrix_features.csv` + `full_dataset.csv`.
- `build_cv_fold_data.py` — needs `density_matrix_features.csv` + `full_dataset.csv`.

These run only when the underlying data changes. CI does NOT regenerate them; the JSON outputs are committed.

## License

- Code (Manim scripts, D3 HTML, Quarto config): MIT
- Prose and figures: CC-BY-4.0 (attribution required for reuse)

The biomarker pipeline at `github.com/Yazidryuichi/biomarker-iium-pipeline` is the data + methods reference. It currently has no license — adding MIT or BSD-3 to that repo is on the cleanup queue.
