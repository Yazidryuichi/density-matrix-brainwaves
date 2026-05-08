# Manim animations — `The Density Matrix in Your Brainwaves`

Four animations, one per script, mapped to the four section figures in the prose.

| Script | Section | Output target |
|---|---|---|
| `01_electrode_opening.py` | Hook (index.qmd) | `../assets/01_electrode_opening.mp4` |
| `02_tbr_reveal.py` | Section 1 (`02-classical.qmd`) | `../assets/02_tbr_reveal.mp4` |
| `03_fdr_matrix.py` | Section 2 (`03-pivot.qmd`) | `../assets/03_fdr_matrix.mp4` |
| `04_density_matrix_construction.py` | Section 3 (`04-density-matrix.qmd`) | `../assets/04_density_matrix_construction.mp4` |

## Setup (one-time)

```bash
# Recommended: dedicated conda env for Manim, isolates from biomarker pipeline env
conda create -n density-matrix python=3.11 -y
conda activate density-matrix
pip install manim==0.18.* numpy scipy
# macOS extras for Cairo / Pango (skip on Linux)
brew install pango cairo ffmpeg
```

Verify install:

```bash
manim --version
# Expected: Manim Community v0.18.x
```

## Render each scene

```bash
cd manim/

# 1080p60, preview opens automatically (-p), high quality (-qh)
manim -pqh 01_electrode_opening.py ElectrodeOpening
manim -pqh 02_tbr_reveal.py TBRReveal
manim -pqh 03_fdr_matrix.py FDRMatrix
manim -pqh 04_density_matrix_construction.py DensityMatrixConstruction
```

Each render lands at `media/videos/<script_name>/1080p60/<SceneName>.mp4`. Move
to `../assets/` so the Quarto site picks it up:

```bash
mv media/videos/01_electrode_opening/1080p60/ElectrodeOpening.mp4 ../assets/01_electrode_opening.mp4
mv media/videos/02_tbr_reveal/1080p60/TBRReveal.mp4 ../assets/02_tbr_reveal.mp4
mv media/videos/03_fdr_matrix/1080p60/FDRMatrix.mp4 ../assets/03_fdr_matrix.mp4
mv media/videos/04_density_matrix_construction/1080p60/DensityMatrixConstruction.mp4 ../assets/04_density_matrix_construction.mp4
```

## Lower-quality preview render (faster iteration)

While iterating on visual choices, use `-ql` instead of `-qh`:

```bash
manim -pql 02_tbr_reveal.py TBRReveal
```

Renders at 480p15 in ~10 seconds. Switch to `-qh` when you're happy with the
visual layout.

## Replacing placeholder data with real exports

Each script has a `PLACEHOLDER` section at the top of the file marked with a
docstring note. Replace as follows:

| Script | Placeholder variable | Replace with |
|---|---|---|
| `02_tbr_reveal.py` | `COHORT_TBR` (28 floats) | `biomarker-iium-pipeline/results/per_subject_features.csv` column `tbr_Fz`, list of 28 |
| `03_fdr_matrix.py` | `RAW_PVALUES` (19×5 array) | `biomarker-iium-pipeline/results/per_channel_band_pvalues.csv` |
| `04_density_matrix_construction.py` | synthetic signals via `synthetic_band_limited()` | Replace function call with `np.load('biomarker-iium-pipeline/results/example_trial.npy')` |

The `01_electrode_opening.py` script has no data dependency — coordinates are
the standard 10-20 system layout.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `cairo not found` on macOS | Missing system dep | `brew install cairo pango` |
| Renders are blurry | Default quality is 480p | Pass `-qh` or `-qk` (4K) |
| `LaTeX Error: File 'standalone.cls' not found` | TeX Live not installed | `brew install --cask mactex` (full MacTeX) or use `manimce-fonts` build |
| `ModuleNotFoundError: scipy` (script 04) | Conda env missing scipy | `pip install scipy` in the `density-matrix` env |
| Animations run too fast | `run_time` per `play()` too short | Each script has `run_time=` arguments commented inline; raise them |

## File-size targets

The Quarto site embeds these as `<video>` tags. Aim for:

- 1080p60 H.264, ~5-10 MB per clip, 4-12 second loops
- If a clip exceeds 15 MB, re-encode with `ffmpeg -i input.mp4 -c:v libx264 -crf 24 -preset slow output.mp4`

## Voice / aesthetic

All four scripts inherit the same colour tokens from `../quarto/styles.scss`:

- Primary `#2B3A55` (deep navy, body text accent)
- Secondary `#6E7F99` (muted, axes / labels)
- Danger `#B3253A` (the FDR threshold, the empirical pivot)
- Success `#2C7A4D` (surviving cells, density-matrix annotations)
- Background `#FBFAF7` (warm-paper Distill-pub aesthetic)

Keep that palette consistent across renders. If you change `styles.scss`, also
update the `PRIMARY`, `SECONDARY`, `DANGER`, `SUCCESS`, `BG` constants at the
top of each `.py` file.
