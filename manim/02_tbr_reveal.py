"""
02_tbr_reveal.py — Theta/beta ratio formula reveal + 28-child cohort scatter.

Renders the TBR formula write-out and plots each of the 28 children's per-child
TBR value at frontal midline (Fz), with the published expected mean for paediatric
typically-developing samples overlaid as a dashed reference.

Render:
    manim -pqh 02_tbr_reveal.py TBRReveal

Output:
    media/videos/02_tbr_reveal/1080p60/TBRReveal.mp4

Move to ../assets/02_tbr_reveal.mp4.

Notes for Yazid:
- The 28 TBR values below are PLACEHOLDER. Replace `COHORT_TBR` with the real
  per-child Fz TBR values exported from `biomarker-iium-pipeline/results/`.
- The published reference mean (`PUBLISHED_TBR_MEAN`) is from Snyder & Hall 2006
  and Arns et al. 2013 averaged. Adjust if you cite a different source in
  Section 1 of the prose.
- The colours follow styles.scss (primary #2B3A55, secondary #6E7F99, danger #B3253A).
"""

from manim import *
import numpy as np

# PLACEHOLDER per-child TBR values at Fz — replace with actual exported values
# from biomarker-iium-pipeline/results/per_subject_features.csv
# Generated here with a plausible distribution (mean ~3.2, sd ~1.0)
np.random.seed(42)
COHORT_TBR = np.clip(np.random.normal(loc=3.2, scale=1.0, size=28), 1.2, 6.5).tolist()

PUBLISHED_TBR_MEAN = 2.5  # paediatric typically-developing reference, illustrative
PUBLISHED_TBR_HIGH_ADHD = 4.0  # threshold above which ADHD literature suggests elevated TBR

PRIMARY = "#2B3A55"
SECONDARY = "#6E7F99"
DANGER = "#B3253A"
SUCCESS = "#2C7A4D"
BG = "#FBFAF7"


class TBRReveal(Scene):
    def construct(self):
        self.camera.background_color = BG

        # PHASE 1 — TBR formula
        title = Text(
            "Theta / beta ratio at Fz",
            font_size=32,
            color="#0F1A2E",
        ).to_edge(UP, buff=0.6)

        formula = MathTex(
            r"\mathrm{TBR}_{Fz} \;=\; \frac{P_\theta(\mathrm{Fz})}{P_\beta(\mathrm{Fz})}",
            font_size=56,
            color=PRIMARY,
        )
        formula.move_to(ORIGIN + UP * 0.5)

        theta_band = MathTex(
            r"\theta : 4\!-\!8 \,\mathrm{Hz}",
            font_size=28,
            color=SECONDARY,
        ).next_to(formula, DOWN, buff=0.7).shift(LEFT * 1.2)

        beta_band = MathTex(
            r"\beta : 13\!-\!30 \,\mathrm{Hz}",
            font_size=28,
            color=SECONDARY,
        ).next_to(formula, DOWN, buff=0.7).shift(RIGHT * 1.2)

        self.play(Write(title, run_time=0.6))
        self.play(Write(formula, run_time=1.4))
        self.play(
            FadeIn(theta_band, shift=UP * 0.1, run_time=0.5),
            FadeIn(beta_band, shift=UP * 0.1, run_time=0.5),
        )
        self.wait(1.2)

        # PHASE 2 — clear formula, build axes for the cohort scatter
        self.play(
            FadeOut(formula),
            FadeOut(theta_band),
            FadeOut(beta_band),
            title.animate.to_edge(UP, buff=0.4),
            run_time=0.6,
        )

        ax = Axes(
            x_range=[0, 29, 5],
            y_range=[0, 7, 1],
            x_length=10,
            y_length=4.5,
            axis_config={"color": SECONDARY, "stroke_width": 1.5},
            tips=False,
        ).move_to(ORIGIN + DOWN * 0.4)

        x_lab = Text("Subject (1–28)", font_size=20, color=SECONDARY).next_to(
            ax.x_axis, DOWN, buff=0.3
        )
        y_lab = Text("TBR at Fz", font_size=20, color=SECONDARY).next_to(
            ax.y_axis, LEFT, buff=0.3
        ).rotate(PI / 2)

        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)

        # Plot per-child TBR values
        dots = VGroup()
        for i, tbr in enumerate(COHORT_TBR, start=1):
            color = DANGER if tbr > PUBLISHED_TBR_HIGH_ADHD else PRIMARY
            d = Dot(
                ax.coords_to_point(i, tbr),
                radius=0.07,
                color=color,
            )
            dots.add(d)

        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.04), run_time=2.0)

        # Reference line at the published TD mean
        ref_line = DashedLine(
            ax.coords_to_point(0, PUBLISHED_TBR_MEAN),
            ax.coords_to_point(29, PUBLISHED_TBR_MEAN),
            color=SUCCESS,
            stroke_width=2,
            dash_length=0.18,
        )
        ref_label = Text(
            f"Published TD mean ≈ {PUBLISHED_TBR_MEAN}",
            font_size=18,
            color=SUCCESS,
        ).next_to(ref_line, RIGHT, buff=0.1).shift(UP * 0.05)

        self.play(Create(ref_line), FadeIn(ref_label), run_time=0.8)

        # Reference line at high-TBR ADHD threshold
        adhd_line = DashedLine(
            ax.coords_to_point(0, PUBLISHED_TBR_HIGH_ADHD),
            ax.coords_to_point(29, PUBLISHED_TBR_HIGH_ADHD),
            color=DANGER,
            stroke_width=1.5,
            dash_length=0.12,
        ).set_opacity(0.6)
        adhd_label = Text(
            f"Elevated-TBR threshold ≈ {PUBLISHED_TBR_HIGH_ADHD}",
            font_size=16,
            color=DANGER,
        ).next_to(adhd_line, RIGHT, buff=0.1).shift(UP * 0.05)

        self.play(Create(adhd_line), FadeIn(adhd_label), run_time=0.6)
        self.wait(2.5)
