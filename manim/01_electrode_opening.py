"""
01_electrode_opening.py — Sensory-hook animation for 'The Density Matrix in Your Brainwaves'.

Renders a 4-second loop showing nineteen 10-20-system EEG electrodes appearing
on a stylised top-down scalp view, then a soft impedance-check pulse propagating
through them.

Render:
    manim -pqh 01_electrode_opening.py ElectrodeOpening

Output target:
    media/videos/01_electrode_opening/1080p60/ElectrodeOpening.mp4

Move to ../assets/01_electrode_opening.mp4 for the Quarto site to find it.

Notes for Yazid (creative direction):
- The scalp colour is intentionally muted (#F2EBE3) to match the cosmo + serif Quarto theme.
- The electrode appearance order follows the standard 10-20 placement scan (frontal -> temporal -> parietal -> occipital).
- The impedance-check pulse uses the danger colour from styles.scss (#B3253A) at 0.6 alpha.
- If the 4-second loop feels too tight, raise PULSE_DURATION below.
"""

from manim import *
import numpy as np

# 10-20 system 15-channel coordinates, normalised to a unit circle.
# Per progress_report_talenta_20260419.md the actual recording was 15 ch / 250 Hz.
# This montage drops the four temporal channels (T3/T4/T5/T6) from the standard
# 19-channel 10-20 system, which is one common 15-ch reduction. If your actual
# hardware uses a different 15-ch subset, edit this list to match before
# re-rendering.
ELECTRODES = [
    # name,  x,    y
    ("Fp1", -0.30, 0.85),
    ("Fp2", 0.30, 0.85),
    ("F7", -0.75, 0.55),
    ("F3", -0.40, 0.55),
    ("Fz", 0.00, 0.55),
    ("F4", 0.40, 0.55),
    ("F8", 0.75, 0.55),
    ("C3", -0.45, 0.00),
    ("Cz", 0.00, 0.00),
    ("C4", 0.45, 0.00),
    ("P3", -0.40, -0.55),
    ("Pz", 0.00, -0.55),
    ("P4", 0.40, -0.55),
    ("O1", -0.30, -0.85),
    ("O2", 0.30, -0.85),
]

SCALP_FILL = "#F2EBE3"
SCALP_STROKE = "#A8A19A"
ELECTRODE_FILL = "#2B3A55"
ELECTRODE_RING = "#FBFAF7"
PULSE_COLOR = "#B3253A"

# These three are highlighted in Section 3 (the FDR-survivors)
HIGHLIGHTED = {"Pz", "P3", "O1"}
HIGHLIGHT_COLOR = "#2C7A4D"


class ElectrodeOpening(Scene):
    def construct(self):
        self.camera.background_color = "#FBFAF7"
        scale = 2.5  # convert unit-circle coordinates to scene units

        # Stylised scalp outline (ellipse approximating top-down head view)
        scalp = Ellipse(
            width=2 * scale * 1.05,
            height=2 * scale * 1.15,
            color=SCALP_STROKE,
            stroke_width=2.5,
            fill_color=SCALP_FILL,
            fill_opacity=1.0,
        )
        # Nose triangle at top
        nose = Polygon(
            np.array([0, scale * 1.18, 0]),
            np.array([-0.12 * scale, scale * 1.05, 0]),
            np.array([0.12 * scale, scale * 1.05, 0]),
            color=SCALP_STROKE,
            stroke_width=2.0,
            fill_color=SCALP_FILL,
            fill_opacity=1.0,
        )
        # Ear flaps
        left_ear = Arc(radius=0.18 * scale, angle=PI, color=SCALP_STROKE).move_to(
            [-scale * 1.05, 0, 0]
        ).rotate(PI / 2)
        right_ear = Arc(radius=0.18 * scale, angle=PI, color=SCALP_STROKE).move_to(
            [scale * 1.05, 0, 0]
        ).rotate(-PI / 2)

        scalp_group = VGroup(scalp, nose, left_ear, right_ear)
        self.play(FadeIn(scalp_group, run_time=0.6))

        # Electrodes appear in scan order
        electrode_dots = []
        electrode_labels = []
        for name, x, y in ELECTRODES:
            ring = Circle(
                radius=0.13,
                color=ELECTRODE_RING,
                stroke_width=2,
                fill_color=ELECTRODE_FILL,
                fill_opacity=1.0,
            ).move_to([x * scale, y * scale, 0])
            label = Text(name, font_size=16, color="#0F1A2E").next_to(
                ring, UP, buff=0.04
            )
            electrode_dots.append(ring)
            electrode_labels.append(label)

        for ring, label in zip(electrode_dots, electrode_labels):
            self.play(
                Create(ring, run_time=0.08),
                FadeIn(label, run_time=0.08),
                run_time=0.10,
            )

        self.wait(0.3)

        # Impedance-check pulse: each electrode pulses outward briefly
        PULSE_DURATION = 1.2
        pulses = []
        for ring in electrode_dots:
            pulse = Circle(
                radius=0.13,
                color=PULSE_COLOR,
                stroke_width=3,
                fill_opacity=0,
            ).move_to(ring.get_center())
            pulses.append(pulse)

        self.play(
            *[
                AnimationGroup(
                    Create(p, run_time=0.4),
                    p.animate.scale(2.5).set_stroke(opacity=0).set_run_time(0.8),
                    lag_ratio=0.0,
                )
                for p in pulses
            ],
            run_time=PULSE_DURATION,
        )

        # Highlight the three FDR-survivors (Pz, P3, O1) — foreshadow Section 3
        for ring, label, (name, _, _) in zip(electrode_dots, electrode_labels, ELECTRODES):
            if name in HIGHLIGHTED:
                self.play(
                    ring.animate.set_fill(HIGHLIGHT_COLOR).set_stroke(HIGHLIGHT_COLOR),
                    label.animate.set_color(HIGHLIGHT_COLOR),
                    run_time=0.25,
                )

        self.wait(0.8)
