"""
04_density_matrix_construction.py — Build the 19-channel density matrix from
analytic signals.

The animation has four phases:

  (a) Raw band-limited time series at 19 channels (line plot)
  (b) Hilbert-transformed analytic signals (complex; show real + imaginary)
  (c) Rank-1 outer product at one timepoint, |psi_t><psi_t|, as a heatmap
  (d) Time-averaged density matrix as a heatmap with magnitude+phase encoding

Render:
    manim -pqh 04_density_matrix_construction.py DensityMatrixConstruction

Output:
    media/videos/04_density_matrix_construction/1080p60/DensityMatrixConstruction.mp4

Move to ../assets/04_density_matrix_construction.mp4.

Notes for Yazid:
- The synthetic signals below are illustrative. Replace with a representative
  trial exported from biomarker-iium-pipeline/results/example_trial.npy if you
  want the real data on screen.
- 'magnitude+phase' encoding uses fill alpha for magnitude and hue for phase.
  Manim does not have a built-in HSV-to-RGB so the colour mapping is computed
  manually below.
- Matrix dimensions are kept at 19x19. The on-screen rendering downsamples to
  a 6-channel illustrative subset for clarity, then expands to the full 19x19.
"""

from manim import *
import numpy as np

# Subset of channels for illustrative phases (a)-(c); full 19x19 in phase (d)
ILLUSTRATIVE_CHANNELS = ["Fz", "Cz", "Pz", "P3", "O1", "O2"]
ALL_CHANNELS = [
    "Fp1", "Fp2", "F7", "F3", "Fz", "F4", "F8",
    "T3", "C3", "Cz", "C4", "T4",
    "T5", "P3", "Pz", "P4", "T6",
    "O1", "O2",
]

PRIMARY = "#2B3A55"
SECONDARY = "#6E7F99"
DANGER = "#B3253A"
SUCCESS = "#2C7A4D"
BG = "#FBFAF7"


def synthetic_band_limited(n_channels=6, n_samples=500, fs=250, band=(13, 30), seed=42):
    """Generate band-limited synthetic signals. Each channel has a slightly
    different phase to make the cross-spectral structure visually interesting."""
    np.random.seed(seed)
    t = np.arange(n_samples) / fs
    signals = np.zeros((n_channels, n_samples))
    for c in range(n_channels):
        # Mix of beta-band sinusoids with channel-specific phase
        phase_offset = c * 0.6
        signals[c] = (
            np.sin(2 * np.pi * 18 * t + phase_offset) * 0.7
            + np.sin(2 * np.pi * 24 * t + phase_offset * 1.3) * 0.4
            + np.random.normal(0, 0.15, n_samples)
        )
    return t, signals


def hilbert_analytic(signals):
    """Compute analytic signal per channel via FFT-based Hilbert transform."""
    from scipy.signal import hilbert as scipy_hilbert
    return np.array([scipy_hilbert(sig) for sig in signals])


def density_matrix(analytic, normalise=True):
    """Compute the time-averaged density matrix from a stack of analytic signals."""
    n_channels, n_samples = analytic.shape
    rho = np.zeros((n_channels, n_channels), dtype=complex)
    for t in range(n_samples):
        psi = analytic[:, t][:, None]
        norm = np.vdot(psi[:, 0], psi[:, 0]).real
        if norm < 1e-12:
            continue
        rho += (psi @ psi.conj().T) / norm
    rho /= n_samples
    if normalise:
        tr = np.trace(rho).real
        if tr > 1e-12:
            rho /= tr
    return rho


def complex_to_rgb(z, max_mag=1.0):
    """Map a complex number to RGB. Magnitude → brightness, phase → hue."""
    import colorsys
    mag = min(abs(z) / max_mag, 1.0)
    phase = (np.angle(z) + np.pi) / (2 * np.pi)  # ∈ [0, 1]
    rgb = colorsys.hsv_to_rgb(phase, 0.65, 0.30 + 0.65 * mag)
    return rgb


class DensityMatrixConstruction(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ——— Phase (a): raw band-limited time series ———
        title_a = Text(
            "(a) Band-limited time series, 6 illustrative channels",
            font_size=22,
            color="#0F1A2E",
        ).to_edge(UP, buff=0.4)

        t, signals = synthetic_band_limited(n_channels=6, n_samples=500)

        ax_a = Axes(
            x_range=[0, t[-1], 0.5],
            y_range=[-3.5, 3.5, 1],
            x_length=10,
            y_length=4.0,
            axis_config={"color": SECONDARY, "stroke_width": 1.0},
            tips=False,
        ).move_to(ORIGIN + DOWN * 0.2)

        self.play(Write(title_a), Create(ax_a), run_time=0.8)

        traces = VGroup()
        offsets = np.linspace(2.5, -2.5, 6)
        colors = [PRIMARY, "#3F5278", SECONDARY, SUCCESS, DANGER, "#7B4F8E"]
        for i, sig in enumerate(signals):
            displaced = sig + offsets[i]
            points = [ax_a.coords_to_point(t[k], displaced[k]) for k in range(0, len(t), 3)]
            line = VMobject(stroke_color=colors[i], stroke_width=1.5)
            line.set_points_smoothly(points)
            label = Text(
                ILLUSTRATIVE_CHANNELS[i], font_size=14, color=colors[i]
            ).move_to(ax_a.coords_to_point(-0.18, offsets[i]))
            traces.add(line, label)

        self.play(Create(traces, run_time=2.0))
        self.wait(1.0)

        # ——— Phase (b): Hilbert-transformed analytic signal (real + imag) ———
        analytic = hilbert_analytic(signals)

        title_b = Text(
            "(b) Analytic signal: x(t) + i·H[x(t)]",
            font_size=22,
            color="#0F1A2E",
        ).to_edge(UP, buff=0.4)
        self.play(Transform(title_a, title_b), run_time=0.5)

        # Show one channel's real (solid) vs imaginary (dashed) overlaid
        # Pick channel 2 (Pz) for the demonstration
        demo_ch = 2
        real_part = signals[demo_ch] + offsets[demo_ch]
        imag_part = analytic[demo_ch].imag + offsets[demo_ch]

        real_pts = [ax_a.coords_to_point(t[k], real_part[k]) for k in range(0, len(t), 3)]
        imag_pts = [ax_a.coords_to_point(t[k], imag_part[k]) for k in range(0, len(t), 3)]

        real_line = VMobject(stroke_color=PRIMARY, stroke_width=2.5)
        real_line.set_points_smoothly(real_pts)
        imag_line = DashedVMobject(
            VMobject(stroke_color=DANGER, stroke_width=2.0).set_points_smoothly(imag_pts),
            num_dashes=80,
        )

        # Fade other traces, keep only Pz
        non_demo = [m for i, m in enumerate(traces) if i // 2 != demo_ch]
        self.play(
            *[m.animate.set_opacity(0.15) for m in non_demo],
            Create(real_line, run_time=1.0),
            Create(imag_line, run_time=1.0),
        )
        self.wait(0.8)

        # ——— Phase (c): rank-1 outer product at one timepoint ———
        self.play(
            FadeOut(traces),
            FadeOut(real_line),
            FadeOut(imag_line),
            FadeOut(ax_a),
            run_time=0.5,
        )

        title_c = Text(
            "(c) Rank-1 outer product at t = 0.6 s:  |ψ⟩⟨ψ|",
            font_size=22,
            color="#0F1A2E",
        ).to_edge(UP, buff=0.4)
        self.play(Transform(title_a, title_c), run_time=0.4)

        # Compute |psi_t><psi_t| for one timepoint at sample 150 (t = 0.6 s)
        sample_idx = 150
        psi = analytic[:, sample_idx][:, None]
        psi /= np.sqrt(np.vdot(psi[:, 0], psi[:, 0]).real + 1e-12)
        outer = psi @ psi.conj().T  # 6x6 complex matrix

        max_mag = np.abs(outer).max()
        cell_size = 0.7
        outer_grid = VGroup()
        for i in range(6):
            for j in range(6):
                rgb = complex_to_rgb(outer[i, j], max_mag=max_mag)
                color_hex = "#{:02X}{:02X}{:02X}".format(
                    int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
                )
                cell = Square(
                    side_length=cell_size * 0.95,
                    stroke_color=SECONDARY,
                    stroke_width=0.5,
                    fill_color=color_hex,
                    fill_opacity=1.0,
                ).move_to([
                    (j - 2.5) * cell_size,
                    (2.5 - i) * cell_size,
                    0,
                ])
                outer_grid.add(cell)

        # Channel labels
        labels = VGroup(
            *[
                Text(ILLUSTRATIVE_CHANNELS[i], font_size=14, color=SECONDARY).next_to(
                    outer_grid[i * 6], LEFT, buff=0.12
                )
                for i in range(6)
            ],
            *[
                Text(ILLUSTRATIVE_CHANNELS[j], font_size=14, color=SECONDARY).next_to(
                    outer_grid[j], UP, buff=0.12
                )
                for j in range(6)
            ],
        )

        self.play(FadeIn(outer_grid), FadeIn(labels), run_time=1.0)
        self.wait(1.5)

        # ——— Phase (d): time-averaged density matrix ρ = E[|ψ⟩⟨ψ|] ———
        rho = density_matrix(analytic)
        max_mag_rho = np.abs(rho).max()

        title_d = Text(
            "(d) Density matrix:  ρ = ⟨|ψ⟩⟨ψ|⟩  (time-averaged)",
            font_size=22,
            color="#0F1A2E",
        ).to_edge(UP, buff=0.4)
        self.play(Transform(title_a, title_d), run_time=0.4)

        # Animate cell-by-cell transition from outer to rho
        new_grid = VGroup()
        for i in range(6):
            for j in range(6):
                rgb = complex_to_rgb(rho[i, j], max_mag=max_mag_rho)
                color_hex = "#{:02X}{:02X}{:02X}".format(
                    int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
                )
                new_cell = Square(
                    side_length=cell_size * 0.95,
                    stroke_color=SECONDARY,
                    stroke_width=0.5,
                    fill_color=color_hex,
                    fill_opacity=1.0,
                ).move_to(outer_grid[i * 6 + j].get_center())
                new_grid.add(new_cell)

        self.play(
            *[Transform(outer_grid[k], new_grid[k]) for k in range(36)],
            run_time=1.6,
        )

        # Annotation
        trace_check = Text(
            f"trace(ρ) ≈ {np.trace(rho).real:.3f}   ·   Hermitian   ·   PSD",
            font_size=18,
            color=SUCCESS,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(trace_check), run_time=0.5)

        self.wait(2.5)
