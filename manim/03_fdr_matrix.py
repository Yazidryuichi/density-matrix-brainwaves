"""
03_fdr_matrix.py — 8-hypothesis correlation forest with BH threshold animating in,
followed by a SHAP top-3 panel showing the posterior-parietal-beta result.

Replaces the original 19-channel × 5-band grid (which did not match the actual
analysis). The pre-registered analysis was 8 Spearman correlations linking
conventional QEEG features to behavioural outcomes, FDR-corrected at q=0.05
across the 8 hypotheses. None survived. SHAP feature ranking from the trained
classifier was a separate, descriptive analysis.

Render:
    manim -pqh 03_fdr_matrix.py FDRMatrix

Output:
    media/videos/03_fdr_matrix/1080p60/FDRMatrix.mp4

All values below come verbatim from progress_report_talenta_20260419.md
(GitHub: Yazidryuichi/biomarker-iium-pipeline) — the canonical source.
"""

from manim import *
import numpy as np

# 8 pre-specified correlation hypotheses, verbatim from the progress report.
# (label, Spearman r, raw p, FDR-corrected p, N)
HYPOTHESES = [
    ("Frontal TBR — Global EF",      -0.489, 0.0131, 0.0900, 25),
    ("TBR_Cz — Global EF",           -0.455, 0.0225, 0.0900, 25),
    ("TBR_Fz — Global EF",           -0.389, 0.0544, 0.1451, 25),
    ("Theta_Fz — Global EF",          0.240, 0.2185, 0.3542, 28),
    ("TBR — Digit Span Backward",    -0.254, 0.2214, 0.3542, 25),
    ("Alpha reactivity — Global EF", -0.156, 0.4294, 0.5725, 28),
    ("TBR — Flanker Effect",         -0.116, 0.5803, 0.6632, 25),
    ("FAA — Global EF",               0.031, 0.8773, 0.8773, 28),
]

# SHAP top-3 from the trained classifier (mean absolute SHAP, verbatim).
SHAP_TOP3 = [
    ("psd_rel_beta_Pz", 0.0654),
    ("psd_rel_beta_P3", 0.0524),
    ("psd_rel_beta_O1", 0.0426),
]

Q_THRESHOLD = 0.05  # Benjamini-Hochberg q-value used in the actual analysis

PRIMARY = "#2B3A55"
SECONDARY = "#6E7F99"
DANGER = "#B3253A"
SUCCESS = "#2C7A4D"
BG = "#FBFAF7"


class FDRMatrix(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ——— Phase 1: title and forest of 8 raw p-values ———
        title = Text(
            "Eight pre-specified correlations, FDR-corrected at q = 0.05",
            font_size=22,
            color="#0F1A2E",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        # X-axis: log10(p) on a horizontal scale
        # Use range 0.001 to 1.0
        ax = NumberLine(
            x_range=[-3, 0, 1],
            length=10,
            color=SECONDARY,
            include_numbers=False,
            include_tip=False,
            stroke_width=1.2,
        ).move_to([0, -2.0, 0])

        # Custom tick labels at p = 0.001, 0.01, 0.05, 0.1, 1.0
        tick_positions = [-3, -2, np.log10(0.05), -1, 0]
        tick_labels_text = ["0.001", "0.01", "0.05", "0.1", "1.0"]
        ax_labels = VGroup()
        for pos, lab in zip(tick_positions, tick_labels_text):
            t = Text(lab, font_size=12, color=SECONDARY).move_to(
                [pos * (10 / 3), -2.35, 0]
            )
            tick_mark = Line(
                [pos * (10 / 3), -2.05, 0],
                [pos * (10 / 3), -1.95, 0],
                color=SECONDARY,
                stroke_width=1.0,
            )
            ax_labels.add(t, tick_mark)

        x_axis_label = Text("p-value (log scale)", font_size=14, color=SECONDARY).move_to(
            [0, -2.7, 0]
        )

        self.play(Create(ax), FadeIn(ax_labels), FadeIn(x_axis_label), run_time=0.6)

        # Plot each hypothesis as a labeled point on the p-value axis
        # Stack vertically above the axis
        n = len(HYPOTHESES)
        y_top = 1.5
        y_bot = -1.6
        y_step = (y_top - y_bot) / (n + 1)

        dots = []
        labels = []
        for i, (lab, r, p_raw, p_fdr, N) in enumerate(HYPOTHESES):
            y_pos = y_top - (i + 1) * y_step
            x_pos = np.log10(max(p_raw, 0.001)) * (10 / 3)
            dot = Dot([x_pos, y_pos, 0], radius=0.08, color=PRIMARY)
            label_text = Text(
                f"{lab}  ·  r = {r:+.3f}  ·  p = {p_raw:.3f}",
                font_size=13,
                color="#1A1A1A",
            ).move_to([0, y_pos, 0])
            label_text.align_to([-5.4, 0, 0], LEFT)
            dots.append(dot)
            labels.append(label_text)

        for d, lb in zip(dots, labels):
            self.play(FadeIn(lb, run_time=0.18), Create(d, run_time=0.18), run_time=0.20)

        self.wait(0.6)

        # ——— Phase 2: BH threshold line slides in ———
        bh_line_x = np.log10(Q_THRESHOLD) * (10 / 3)
        bh_line = DashedLine(
            [bh_line_x, -1.85, 0],
            [bh_line_x, 1.7, 0],
            color=DANGER,
            stroke_width=2,
            dash_length=0.12,
        )
        bh_label = Text(
            f"BH threshold line at uncorrected p = {Q_THRESHOLD}",
            font_size=14,
            color=DANGER,
        ).next_to(bh_line, UP, buff=0.1)

        self.play(Create(bh_line), FadeIn(bh_label), run_time=0.7)
        self.wait(0.5)

        # ——— Phase 3: outcome — none survive FDR ———
        verdict = Text(
            "After Benjamini–Hochberg correction across the 8 hypotheses: none survive",
            font_size=18,
            color=DANGER,
        ).to_edge(DOWN, buff=0.4).shift(UP * 0.1)
        self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.7)
        self.wait(1.5)

        # ——— Phase 4: clear forest, pivot to SHAP top-3 ———
        all_forest = VGroup(*dots, *labels, bh_line, bh_label, ax, ax_labels, x_axis_label)
        self.play(FadeOut(all_forest), FadeOut(verdict), run_time=0.6)

        pivot_text = Text(
            "But when a flexible classifier was trained on the same features,",
            font_size=20,
            color="#0F1A2E",
        ).move_to([0, 1.0, 0])
        pivot_text2 = Text(
            "SHAP feature importance picked up a different signal:",
            font_size=20,
            color="#0F1A2E",
        ).move_to([0, 0.4, 0])
        self.play(FadeIn(pivot_text), FadeIn(pivot_text2), run_time=0.7)
        self.wait(0.8)

        # SHAP top-3 horizontal bars
        max_shap = max(s for _, s in SHAP_TOP3)
        bar_left_x = -3.0
        bar_max_width = 5.0
        bar_height = 0.4
        bar_y_centers = [-0.6, -1.2, -1.8]

        shap_group = VGroup()
        for (feat, shap), y in zip(SHAP_TOP3, bar_y_centers):
            width = (shap / max_shap) * bar_max_width
            bar = Rectangle(
                width=width,
                height=bar_height,
                fill_color=SUCCESS,
                fill_opacity=0.9,
                stroke_color=SUCCESS,
                stroke_width=1,
            )
            bar.move_to([bar_left_x + width / 2, y, 0])
            label = Text(feat, font_size=15, color="#0F1A2E").next_to(bar, LEFT, buff=0.15)
            value = Text(f"{shap:.4f}", font_size=14, color=SECONDARY).next_to(
                bar, RIGHT, buff=0.15
            )
            shap_group.add(bar, label, value)

        self.play(LaggedStartMap(FadeIn, shap_group, lag_ratio=0.15), run_time=1.4)

        caption = Text(
            "Top three by mean |SHAP|: relative beta power, posterior-parietal-dominant.",
            font_size=15,
            color=SUCCESS,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.6)

        self.wait(2.5)
