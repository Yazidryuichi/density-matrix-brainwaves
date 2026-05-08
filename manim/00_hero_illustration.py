"""
00_hero_illustration.py — Static hero image for the essay's landing page.

Composition: an EEG signal on the left morphing through a Hilbert-transform
arrow into a 6x6 density matrix heatmap on the right. A title plate sits
beneath the composition.

Renders as a single high-resolution PNG (1920x1080 by default) for embedding
at the top of `index.qmd`.

Render:
    manim -sqh 00_hero_illustration.py HeroIllustration

  -s = single still frame (no animation, faster)
  -qh = high quality (1080p)

Output:
    media/images/00_hero_illustration/HeroIllustration_ManimCE_v0.18.1.png

Move to ../assets/00_hero.png for the Quarto site to find it.
"""

from manim import *
import numpy as np
import colorsys

# Colour tokens — matched to styles.scss
PRIMARY = "#2B3A55"
SECONDARY = "#6E7F99"
ACCENT = "#6B4F8E"
DANGER = "#B73E3E"
SUCCESS = "#2C5F4F"
BG = "#FBF9F4"


def complex_to_rgb(z, max_mag=1.0):
    mag = min(abs(z) / max_mag, 1.0)
    phase = (np.angle(z) + np.pi) / (2 * np.pi)
    rgb = colorsys.hsv_to_rgb(phase, 0.55, 0.30 + 0.60 * mag)
    return rgb


class HeroIllustration(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ——— LEFT: EEG-style time series ———
        # Build a stylised band-limited signal
        t = np.linspace(0, 4 * np.pi, 400)
        sig1 = np.sin(2.3 * t) * 0.6 + np.sin(5.7 * t + 0.4) * 0.3 + np.random.normal(0, 0.05, len(t))
        sig2 = np.sin(2.8 * t + 1.1) * 0.55 + np.sin(7.2 * t) * 0.25 + np.random.normal(0, 0.05, len(t))
        sig3 = np.sin(3.5 * t + 0.7) * 0.5 + np.sin(6.5 * t + 1.4) * 0.3 + np.random.normal(0, 0.05, len(t))

        # EEG axes
        eeg_left_x = -6.0
        eeg_right_x = -1.6
        eeg_y_offsets = [1.0, 0.0, -1.0]
        eeg_signals = [sig1, sig2, sig3]
        colors_eeg = [PRIMARY, ACCENT, SUCCESS]

        eeg_traces = VGroup()
        for sig, y_off, color in zip(eeg_signals, eeg_y_offsets, colors_eeg):
            x_coords = np.linspace(eeg_left_x, eeg_right_x, len(t))
            points = [
                np.array([x, sig[i] * 0.35 + y_off, 0])
                for i, x in enumerate(x_coords)
            ]
            line = VMobject(stroke_color=color, stroke_width=1.7)
            line.set_points_smoothly(points[::3])
            eeg_traces.add(line)

        # Light-touch labels for the three traces
        for ch, y_off in zip(["Pz", "P3", "O1"], eeg_y_offsets):
            label = Text(ch, font_size=18, color=SECONDARY, weight=NORMAL)
            label.move_to(np.array([eeg_left_x - 0.38, y_off, 0]))
            eeg_traces.add(label)

        # ——— CENTER: arrow + label "Hilbert + embed" ———
        arrow_start = np.array([-1.4, 0, 0])
        arrow_end = np.array([0.4, 0, 0])
        arrow = Arrow(
            arrow_start, arrow_end,
            buff=0.05,
            stroke_width=2.0,
            color=ACCENT,
            max_tip_length_to_length_ratio=0.10,
        )

        arrow_label = Text(
            "Hilbert + quantum embedding",
            font_size=15,
            color=ACCENT,
            slant=ITALIC,
            weight=NORMAL,
        ).move_to(np.array([-0.5, 0.32, 0]))

        # ——— RIGHT: density matrix heatmap ———
        # Construct a synthetic Hermitian PSD matrix
        np.random.seed(7)
        n = 6
        A = np.random.normal(0, 0.6, (n, n)) + 1j * np.random.normal(0, 0.4, (n, n))
        rho = A @ A.conj().T
        rho = rho / np.trace(rho).real

        cell = 0.42
        rho_origin_x = 1.3
        rho_origin_y = 1.05  # top of grid

        max_mag = np.abs(rho).max()
        rho_grid = VGroup()
        for i in range(n):
            for j in range(n):
                rgb = complex_to_rgb(rho[i, j], max_mag=max_mag)
                hex_color = "#{:02X}{:02X}{:02X}".format(
                    int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
                )
                sq = Square(
                    side_length=cell * 0.94,
                    fill_color=hex_color,
                    fill_opacity=1.0,
                    stroke_color=BG,
                    stroke_width=1.4,
                )
                sq.move_to(np.array([
                    rho_origin_x + j * cell,
                    rho_origin_y - i * cell,
                    0,
                ]))
                rho_grid.add(sq)

        # ρ label above the matrix
        rho_label = MathTex(r"\rho", color=ACCENT, font_size=44).move_to(
            np.array([rho_origin_x + (n - 1) * cell / 2, rho_origin_y + cell + 0.10, 0])
        )

        # ——— TITLE PLATE at the bottom ———
        title_text = Text(
            "The Density Matrix in Your Brainwaves",
            font_size=38,
            color="#0F1A2E",
            weight=BOLD,
        )
        title_text.move_to(np.array([0, -2.40, 0]))

        subtitle_text = Text(
            "What a borrowed mathematical formalism reveals about inference\n"
            "under bounded computational precision",
            font_size=18,
            color="#4A5A76",
            slant=ITALIC,
        )
        subtitle_text.move_to(np.array([0, -3.05, 0]))

        # Decorative ρ glyph between the composition and the title
        rho_divider_left = Line(
            np.array([-1.5, -1.85, 0]),
            np.array([-0.35, -1.85, 0]),
            stroke_color=ACCENT,
            stroke_width=1.0,
        )
        rho_divider_right = Line(
            np.array([0.35, -1.85, 0]),
            np.array([1.5, -1.85, 0]),
            stroke_color=ACCENT,
            stroke_width=1.0,
        )
        rho_glyph = MathTex(r"\rho", color=ACCENT, font_size=32).move_to(
            np.array([0, -1.85, 0])
        )

        # Compose the still
        self.add(eeg_traces)
        self.add(arrow, arrow_label)
        self.add(rho_grid, rho_label)
        self.add(rho_divider_left, rho_divider_right, rho_glyph)
        self.add(title_text, subtitle_text)
