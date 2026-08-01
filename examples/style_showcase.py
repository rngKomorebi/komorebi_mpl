"""Style showcase — one folder per style, one figure per plot type.

For every registered style this writes ``figures/showcase/<style>/`` containing
the same set of plot types, so any two styles can be compared side by side by
opening the same filename in two folders. Each figure deliberately exercises
several style aspects at once — legends, text boxes, error bars, colormaps,
minor ticks, suptitles — so a single glance shows whether the style holds
together. ``00_overview.png`` in each folder is a contact sheet of the rest.

The random data is regenerated from a fixed seed inside every plot function, so
the same figure shows the *same* data in every style.

Doubles as a visual test: run it and inspect the saved PNGs.

``--gallery`` instead writes the small, committed set under ``docs/gallery/``
that the README links to: one comparison grid across all styles, plus a
four-plot card per style.

Usage (from the repo root):
    python examples/style_showcase.py                # all styles, full set
    python examples/style_showcase.py komorebi earth # only these
    python examples/style_showcase.py --gallery      # rebuild docs/gallery/
"""

import os
import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText

import komorebi_mpl
from komorebi_mpl.functions import night_wave_func

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(_HERE, "figures", "showcase")
GALLERY_DIR = os.path.join(os.path.dirname(_HERE), "docs", "gallery")

STYLES = [
    "night_wave",
    "sci_pure",
    "sci_faded",
    "sci_print",
    "sci_pub",
    "blueprint",
    "minimal",
    "solarized",
    "earth",
    "komorebi",
    "dapkel",
    "daplis",
]

SEED = 42


# ── helpers ────────────────────────────────────────────────────────────────


def _rng():
    """Fresh generator, so every style plots identical data."""
    return np.random.default_rng(SEED)


def _save(style: str, name: str) -> None:
    folder = os.path.join(OUT_DIR, style)
    os.makedirs(folder, exist_ok=True)
    plt.savefig(os.path.join(folder, name), bbox_inches="tight")
    plt.close()


# ── 01. Line plot: legend + text box ───────────────────────────────────────


def plot_lines(style: str) -> None:
    komorebi_mpl.use(style)
    fig, ax = plt.subplots()

    x = np.linspace(0, 2 * np.pi, 200)
    for k in range(1, 5):
        ax.plot(x, np.sin(k * x), label=f"$\\sin({k}x)$")

    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(f"{style} — line plot")
    ax.legend(loc="upper right")

    # Text box: shape only, so the colors come from patch.* in the style
    ax.text(
        0.02,
        0.97,
        "Annotation box",
        transform=ax.transAxes,
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    _save(style, "01_lines.png")


# ── 02. Scatter: legend + stats box ────────────────────────────────────────


def plot_scatter(style: str) -> None:
    komorebi_mpl.use(style)
    rng = _rng()
    fig, ax = plt.subplots()

    for k in range(4):
        x = rng.normal(k * 1.5, 0.6, 80)
        y = rng.normal(k * 0.8, 0.5, 80)
        ax.scatter(x, y, label=f"Group {k + 1}", alpha=0.75)

    ax.set_xlabel("X (a.u.)")
    ax.set_ylabel("Y (a.u.)")
    ax.set_title(f"{style} — scatter")
    ax.legend(loc="upper left")

    ax.text(
        0.98,
        0.03,
        "$N = 320$\n4 groups",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    _save(style, "02_scatter.png")


# ── 03. Bar chart: error bars (style capsize) + legend + text box ───────────


def plot_bars(style: str) -> None:
    komorebi_mpl.use(style)
    rng = _rng()
    fig, ax = plt.subplots()

    categories = ["A", "B", "C", "D", "E"]
    values = rng.uniform(0.4, 1.0, len(categories))
    errors = rng.uniform(0.03, 0.12, len(categories))

    # No explicit capsize: errorbar.capsize from the style shows through.
    # ecolor, though, is hardcoded to 'k' by bar() with no rcParam behind it,
    # so it has to be pulled from the style by hand or the bars get black
    # error bars — near-invisible on the dark styles.
    ax.bar(
        categories,
        values,
        yerr=errors,
        ecolor=plt.rcParams["text.color"],
        label="Measurement",
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    ax.set_title(f"{style} — bar chart")
    ax.legend()

    ax.text(
        0.98,
        0.97,
        "$n = 100$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="square,pad=0.3"),
    )

    _save(style, "03_bars.png")


# ── 04. Overlapping histograms: legend + fit-parameter box ─────────────────


def plot_histogram(style: str) -> None:
    komorebi_mpl.use(style)
    rng = _rng()
    fig, ax = plt.subplots()

    for k, label in enumerate(["Sample A", "Sample B", "Sample C"]):
        data = rng.normal(k * 1.5, 0.8, 400)
        ax.hist(data, bins=30, alpha=0.6, label=label)

    ax.set_xlabel("Value")
    ax.set_ylabel("Count")
    ax.set_title(f"{style} — overlapping histograms")
    ax.legend(loc="upper right")

    # The kind of fit-result box analysis code drops next to a histogram
    ax.text(
        0.02,
        0.97,
        "$\\mu = 1.50 \\pm 0.04$\n$\\sigma = 0.80 \\pm 0.03$\n$\\chi^2/\\nu = 1.07$",
        transform=ax.transAxes,
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.5"),
    )

    _save(style, "04_histogram.png")


# ── 05. Histogram + Gaussian fit + residuals: the workhorse figure ─────────


def plot_hist_fit(style: str) -> None:
    """Histogram with a Gaussian fit, a fit-parameter box and a residual panel.

    The 'fit' is the closed-form Gaussian maximum-likelihood estimate (sample
    mean and standard deviation), so this example needs nothing beyond numpy.
    """
    komorebi_mpl.use(style)
    rng = _rng()
    fig, (ax1, ax2) = plt.subplots(
        2, 1, sharex=True, gridspec_kw=dict(height_ratios=[3, 1])
    )
    fig.suptitle(f"{style} — histogram & Gaussian fit")

    data = rng.normal(120.0, 18.0, 4000)
    counts, edges = np.histogram(data, bins=45)
    centres = 0.5 * (edges[:-1] + edges[1:])
    width = edges[1] - edges[0]

    mu, sigma = data.mean(), data.std(ddof=1)
    model = (
        data.size
        * width
        / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-0.5 * ((centres - mu) / sigma) ** 2)
    )

    # Poisson errors; keep only populated bins for the residuals and chi^2
    err = np.sqrt(np.maximum(counts, 1))
    ok = counts > 0
    resid = (counts[ok] - model[ok]) / err[ok]
    chi2_red = np.sum(resid**2) / (ok.sum() - 2)
    fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma

    # ── data + fit ──
    # bar() and plot() draw from *separate* property cycles, so both would
    # otherwise start at colour 0 and the fit would vanish into the bars.
    # "C1" is the style's second cycle colour — in daplis that slot is
    # deliberately the "fits / overlaid curves" colour.
    # ecolor: bar() hardcodes 'k' and has no rcParam, so take the style's ink
    ax1.bar(
        centres,
        counts,
        width=width,
        yerr=err,
        ecolor=plt.rcParams["text.color"],
        label="Data",
    )
    ax1.plot(centres, model, color="C1", label="Gaussian fit")

    ax1.set_ylabel("Counts")
    ax1.legend(loc="upper right")
    ax1.text(
        0.02,
        0.97,
        "\n".join(
            [
                f"$\\mu = {mu:.1f}$ ps",
                f"$\\sigma = {sigma:.1f}$ ps",
                f"FWHM $= {fwhm:.1f}$ ps",
                f"$N = {data.size}$",
                f"$\\chi^2/\\nu = {chi2_red:.2f}$",
            ]
        ),
        transform=ax1.transAxes,
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.5"),
    )

    # ── residuals ──
    ax2.axhline(0.0, linestyle="--", linewidth=1.2, color=plt.rcParams["axes.edgecolor"])
    ax2.plot(centres[ok], resid, marker=".", linestyle="none")
    ax2.set_xlabel("$\\Delta t$ (ps)")
    ax2.set_ylabel("Residuals\n($\\sigma$)")

    fig.tight_layout()
    _save(style, "05_hist_fit.png")


# ── 06. 2D histogram: colormap + colorbar + box over the data ──────────────


def plot_hist2d(style: str) -> None:
    komorebi_mpl.use(style)
    rng = _rng()
    fig, ax = plt.subplots()

    x = rng.normal(0, 1, 2000)
    y = 0.8 * x + rng.normal(0, 0.6, 2000)
    h = ax.hist2d(x, y, bins=40)
    fig.colorbar(h[3], ax=ax, label="Count")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"{style} — 2D histogram")

    # Text box on top of an image: worst case for legibility
    ax.text(
        0.03,
        0.97,
        "$r = 0.80$",
        transform=ax.transAxes,
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    _save(style, "06_hist2d.png")


# ── 07. Step plot + fill_between ───────────────────────────────────────────


def plot_fill(style: str) -> None:
    komorebi_mpl.use(style)
    fig, ax = plt.subplots()

    x = np.linspace(0, 4 * np.pi, 300)
    y1 = np.sin(x)
    y2 = 0.5 * np.sin(2 * x)

    ax.plot(x, y1, label="$\\sin(x)$")
    ax.plot(x, y2, label="$0.5\\sin(2x)$")
    ax.fill_between(x, y1, y2, alpha=0.25, label="Difference")

    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(f"{style} — fill between")
    ax.legend(loc="upper right")

    _save(style, "07_fill.png")


# ── 08. Error bars: markers, caps, legend ──────────────────────────────────


def plot_errorbar(style: str) -> None:
    komorebi_mpl.use(style)
    rng = _rng()
    fig, ax = plt.subplots()

    x = np.arange(1, 11)
    for k, label in enumerate(["Run 1", "Run 2", "Run 3"]):
        y = 10 * np.exp(-x / (4 + 2 * k)) + rng.normal(0, 0.15, x.size)
        yerr = rng.uniform(0.15, 0.5, x.size)
        ax.errorbar(x, y, yerr=yerr, marker="o", label=label)

    ax.set_xlabel("Measurement #")
    ax.set_ylabel("Signal (a.u.)")
    ax.set_title(f"{style} — error bars")
    ax.legend(loc="upper right")

    ax.text(
        0.03,
        0.03,
        "caps and widths\nfrom the style",
        transform=ax.transAxes,
        va="bottom",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    _save(style, "08_errorbar.png")


# ── 09. Box plot: patch.* on real artists, not just text boxes ─────────────


def plot_boxplot(style: str) -> None:
    komorebi_mpl.use(style)
    rng = _rng()
    fig, ax = plt.subplots()

    data = [rng.normal(k * 0.6, 0.4 + 0.1 * k, 200) for k in range(5)]
    # patch_artist: the boxes are drawn with patch.facecolor / patch.edgecolor,
    # i.e. the same colours as the style's text boxes and legend
    ax.boxplot(data, patch_artist=True, tick_labels=list("VWXYZ"))

    ax.set_xlabel("Group")
    ax.set_ylabel("Value")
    ax.set_title(f"{style} — box plot")

    ax.text(
        0.03,
        0.97,
        "boxes use patch.*\n(same as this box)",
        transform=ax.transAxes,
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    _save(style, "09_boxplot.png")


# ── 10. Multi-panel (1×2): suptitle + per-panel legend and box ──────────────


def plot_multipanel(style: str) -> None:
    komorebi_mpl.use(style)
    rng = _rng()
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(f"{style} — multi-panel")

    x = np.linspace(0, 4 * np.pi, 300)
    for k in range(3):
        ax1.plot(x, np.cos(x + k * np.pi / 3), label=f"$\\phi={k}\\pi/3$")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$\\cos(x + \\phi)$")
    ax1.set_title("Lines")
    ax1.legend(loc="upper right")

    cats = ["P", "Q", "R", "S", "T"]
    values = rng.uniform(0.2, 1.0, len(cats))
    ax2.bar(cats, values, label="Counts")
    ax2.set_xlabel("Category")
    ax2.set_ylabel("Value")
    ax2.set_title("Bars")
    ax2.legend(loc="upper right")
    ax2.text(
        0.03,
        0.97,
        "panel 2",
        transform=ax2.transAxes,
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.3"),
    )

    fig.tight_layout()
    _save(style, "10_multipanel.png")


# ── 11. Shared-axis subplots ────────────────────────────────────────────────


def plot_shared_axes(style: str) -> None:
    komorebi_mpl.use(style)
    fig, axes = plt.subplots(3, 1, sharex=True)
    fig.suptitle(f"{style} — shared x-axis")

    x = np.linspace(0, 2 * np.pi, 200)
    signals = [np.sin(x), np.cos(x), np.sin(x) * np.cos(x)]
    labels = ["$\\sin$", "$\\cos$", "$\\sin\\cdot\\cos$"]

    for ax, sig, lbl in zip(axes, signals, labels):
        ax.plot(x, sig, label=lbl)
        ax.legend(loc="upper right")
        ax.set_ylabel(lbl)

    axes[0].text(
        0.02,
        0.9,
        "shared ticks below",
        transform=axes[0].transAxes,
        va="top",
        fontsize="x-small",
        bbox=dict(boxstyle="round,pad=0.3"),
    )

    axes[-1].set_xlabel("$x$")
    fig.tight_layout()
    _save(style, "11_shared_axes.png")


# ── 12. Log scale: minor ticks on both axes ────────────────────────────────


def plot_logscale(style: str) -> None:
    komorebi_mpl.use(style)
    fig, ax = plt.subplots()

    x = np.logspace(-1, 3, 200)
    for alpha in [0.5, 1.0, 1.5, 2.0]:
        ax.plot(x, x**alpha, label=f"$x^{{{alpha}}}$")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(f"{style} — log scale")
    ax.legend(loc="upper left")

    ax.text(
        0.97,
        0.03,
        "log minor ticks",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    _save(style, "12_logscale.png")


# ── 13. Image + colorbar: image.cmap on a 2D map ───────────────────────────


def plot_colormap(style: str) -> None:
    komorebi_mpl.use(style)
    rng = _rng()
    fig, ax = plt.subplots()

    yy, xx = np.mgrid[0:64, 0:64]
    field = np.zeros_like(xx, dtype=float)
    for cx, cy, amp, w in [(18, 22, 1.0, 9), (44, 38, 0.7, 13), (30, 52, 0.5, 6)]:
        field += amp * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * w**2))
    field += rng.normal(0, 0.02, field.shape)

    im = ax.imshow(field, origin="lower", interpolation="nearest")
    fig.colorbar(im, ax=ax, label="Intensity (a.u.)")

    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_title(f"{style} — image & colormap")

    ax.text(
        0.03,
        0.97,
        "3 hot spots",
        transform=ax.transAxes,
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    _save(style, "13_colormap.png")


# ── 14. Annotations: arrows, boxes, and the AnchoredText caveat ─────────────


def plot_annotations(style: str) -> None:
    komorebi_mpl.use(style)
    fig, ax = plt.subplots()

    x = np.linspace(0, 2 * np.pi, 200)
    ax.plot(x, np.sin(x))

    # Arrow annotation, no box
    ax.annotate(
        "Maximum",
        xy=(np.pi / 2, 1.0),
        xytext=(np.pi / 2 + 0.8, 0.7),
        fontsize="small",
        arrowprops=dict(arrowstyle="->", shrinkB=5),
    )

    # Plain text box — colors from patch.*
    ax.text(
        4.5,
        0.45,
        "Plain text box\n$y = \\sin(x)$",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    # Arrow annotation with a box
    ax.annotate(
        "Minimum",
        xy=(3 * np.pi / 2, -1.0),
        xytext=(3 * np.pi / 2 - 1.6, -0.35),
        fontsize="small",
        arrowprops=dict(arrowstyle="->", shrinkB=5),
        bbox=dict(boxstyle="round,pad=0.3"),
    )

    # AnchoredText. Matplotlib hardcodes its frame to white/black and ignores
    # patch.*, so the colours have to be pulled from the active rcParams by
    # hand — see the README. Without these three lines this box comes out a
    # solid white rectangle, invisible-on-invisible under the dark styles.
    at = AnchoredText(
        "AnchoredText\n(rcParams frame)",
        loc="upper left",
        prop=dict(size="x-small", color=plt.rcParams["text.color"]),
        frameon=True,
    )
    at.patch.set_boxstyle("round,pad=0.3")
    at.patch.set_facecolor(plt.rcParams["patch.facecolor"])
    at.patch.set_edgecolor(plt.rcParams["patch.edgecolor"])
    ax.add_artist(at)

    ax.set_xlabel("$x$")
    ax.set_ylabel("$\\sin(x)$")
    ax.set_title(f"{style} — annotations & text boxes")

    _save(style, "14_annotations.png")


# ── 15. Typography ruler: every font slot the style defines ─────────────────


def plot_typography(style: str) -> None:
    komorebi_mpl.use(style)
    fig, ax = plt.subplots()
    fig.suptitle(f"figure.titlesize = {plt.rcParams['figure.titlesize']}", y=1.04)

    ax.set_title(f"{style} — axes.titlesize = {plt.rcParams['axes.titlesize']}")
    ax.set_xlabel(f"axes.labelsize = {plt.rcParams['axes.labelsize']}")
    ax.set_ylabel(f"tick labelsize = {plt.rcParams['xtick.labelsize']}")

    # Flat line low in the axes, so it stays clear of the text rows
    ax.plot(
        [0, 1],
        [0.04, 0.04],
        label=f"legend.fontsize = {plt.rcParams['legend.fontsize']}",
    )
    ax.set_ylim(0, 1)
    ax.legend(loc="lower right")

    rows = [
        ("font.size (base)", plt.rcParams["font.size"], None),
        ("'large'", None, "large"),
        ("'medium'", None, "medium"),
        ("'small'", None, "small"),
        ("'x-small'", None, "x-small"),
    ]
    for i, (label, size, rel) in enumerate(rows):
        y = 0.92 - i * 0.15
        ax.text(
            0.03,
            y,
            f"{label}  —  the quick brown fox",
            transform=ax.transAxes,
            va="center",
            fontsize=size if rel is None else rel,
            bbox=dict(boxstyle="round,pad=0.3") if i == 0 else None,
        )

    _save(style, "15_typography.png")


# ── night_wave extras ───────────────────────────────────────────────────────


def plot_night_wave_line_glow() -> None:
    komorebi_mpl.use("night_wave")
    fig, ax = plt.subplots()

    x = np.linspace(0, 2 * np.pi, 200)
    for k in range(1, 5):
        ax.plot(x, np.sin(k * x), label=f"$\\sin({k}x)$")

    night_wave_func.make_lines_glow(ax)

    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("night_wave — line glow")
    ax.legend(loc="upper right")

    _save("night_wave", "16_lines_glow.png")


def plot_night_wave_glow_gradient() -> None:
    komorebi_mpl.use("night_wave")
    fig, ax = plt.subplots()

    x = np.linspace(0, 2 * np.pi, 200)
    for k in range(1, 4):
        ax.plot(x, np.sin(k * x), label=f"$\\sin({k}x)$")

    night_wave_func.add_glow_and_grad_fill(ax)

    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("night_wave — glow + gradient fill")
    ax.legend(loc="upper right")

    _save("night_wave", "17_lines_glow_grad.png")


def plot_night_wave_bars() -> None:
    komorebi_mpl.use("night_wave")
    rng = _rng()
    fig, ax = plt.subplots()

    categories = ["A", "B", "C", "D", "E"]
    values = rng.uniform(0.4, 1.0, len(categories))
    bars = ax.bar(categories, values)
    night_wave_func.add_bar_gradient(bars, ax)

    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    ax.set_title("night_wave — bar gradient")

    _save("night_wave", "18_bars_grad.png")


def plot_night_wave_hist_gradient() -> None:
    komorebi_mpl.use("night_wave")
    rng = _rng()
    fig, ax = plt.subplots()

    data = rng.normal(0, 1, 1000)
    _, _, hist_container = ax.hist(data, bins=30)
    night_wave_func.add_hist_gradient(hist_container, ax)

    ax.set_xlabel("Value")
    ax.set_ylabel("Count")
    ax.set_title("night_wave — histogram gradient")

    _save("night_wave", "19_hist_grad.png")


def plot_night_wave_scatter_glow() -> None:
    komorebi_mpl.use("night_wave")
    rng = _rng()
    fig, ax = plt.subplots()

    x = rng.normal(0, 1, 150)
    y = rng.normal(0, 1, 150)
    color_vals = np.hypot(x, y)  # colour by distance from origin
    ax.scatter(x, y, c=color_vals, label="Data", zorder=3)
    night_wave_func.make_scatter_glow(ax)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("night_wave — scatter glow")
    ax.legend()

    _save("night_wave", "20_scatter_glow.png")


# ── contact sheet ──────────────────────────────────────────────────────────


def make_overview(style: str) -> None:
    """Assemble the style's figures into a single 00_overview.png."""
    folder = os.path.join(OUT_DIR, style)
    names = sorted(
        f
        for f in os.listdir(folder)
        if f.endswith(".png") and not f.startswith("00_")
    )
    if not names:
        return

    ncols = 4
    nrows = -(-len(names) // ncols)
    # The source figures are ~1500 px wide, so the tiles have to be that big
    # too or the contact sheet turns into unreadable mush: 7.5 in at 200 dpi
    # is 1500 px per tile, i.e. roughly native resolution.
    tile_w, tile_h, dpi = 7.5, 5.0, 200
    # Neutral context so the montage itself is not styled
    with plt.style.context("default"):
        fig, axes = plt.subplots(
            nrows, ncols, figsize=(tile_w * ncols, tile_h * nrows)
        )
        for ax, name in zip(np.ravel(axes), names):
            ax.imshow(plt.imread(os.path.join(folder, name)))
            ax.set_title(name[:-4], fontsize=13)
        for ax in np.ravel(axes):
            ax.axis("off")
        fig.suptitle(style, fontsize=26)
        fig.tight_layout()
        fig.savefig(
            os.path.join(folder, "00_overview.png"),
            dpi=dpi,
            bbox_inches="tight",
            facecolor="#9A9A9A",
        )
        plt.close(fig)


# ── README gallery ─────────────────────────────────────────────────────────

# The four plots that best show what a style does: palette and legend, the
# workhorse fit figure, patch.* on real artists, and every kind of text box.
GALLERY_PLOTS = ["01_lines.png", "05_hist_fit.png", "09_boxplot.png", "14_annotations.png"]

# Kept deliberately small — these are committed to the repo.
GALLERY_DPI = 75
GRID_DPI = 70


def _grid_tile(style: str) -> str:
    """Draw a compact, title-less line plot for the comparison grid.

    The montage puts the style name above each tile, so an axes title here
    would just repeat it and eat space that the palette should be using.
    """
    komorebi_mpl.use(style)
    fig, ax = plt.subplots(figsize=(9, 6))

    x = np.linspace(0, 2 * np.pi, 200)
    for k in range(1, 5):
        ax.plot(x, np.sin(k * x), label=f"$\\sin({k}x)$")

    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="upper right", ncol=2)
    ax.text(
        0.02,
        0.97,
        "Annotation box",
        transform=ax.transAxes,
        va="top",
        fontsize="small",
        bbox=dict(boxstyle="round,pad=0.4"),
    )

    path = os.path.join(OUT_DIR, style, "_grid_tile.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return path


def _montage(paths, ncols, out_path, dpi, suptitle=None, titles=None):
    """Tile already-saved PNGs into one figure, unstyled."""
    nrows = -(-len(paths) // ncols)
    with plt.style.context("default"):
        fig, axes = plt.subplots(nrows, ncols, figsize=(7.0 * ncols, 4.6 * nrows))
        flat = np.ravel(np.atleast_1d(axes))
        for i, ax in enumerate(flat):
            ax.axis("off")
            if i < len(paths):
                ax.imshow(plt.imread(paths[i]))
                if titles:
                    ax.set_title(titles[i], fontsize=17)
        if suptitle:
            fig.suptitle(suptitle, fontsize=24)
        fig.tight_layout()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=dpi, bbox_inches="tight", facecolor="white")
        plt.close(fig)


def build_gallery(styles) -> None:
    """Write the committed docs/gallery/ set the README links to."""
    by_name = dict(zip([n for n, _ in PLOT_FUNCS], [f for _, f in PLOT_FUNCS]))
    needed = {
        "01_lines.png": by_name["line plot"],
        "05_hist_fit.png": by_name["histogram + Gaussian fit"],
        "09_boxplot.png": by_name["box plot"],
        "14_annotations.png": by_name["annotations"],
    }

    for style in styles:
        folder = os.path.join(OUT_DIR, style)
        for name, fn in needed.items():
            if not os.path.exists(os.path.join(folder, name)):
                print(f"  {style} — generating {name}")
                fn(style)

        print(f"  {style} — card")
        _montage(
            [os.path.join(folder, n) for n in GALLERY_PLOTS],
            ncols=2,
            out_path=os.path.join(GALLERY_DIR, f"{style}.png"),
            dpi=GALLERY_DPI,
            suptitle=style,
            titles=["line plot", "histogram & Gaussian fit", "box plot", "annotations"],
        )

    print("  all-styles comparison grid")
    tiles = [_grid_tile(s) for s in styles]
    _montage(
        tiles,
        ncols=4,
        out_path=os.path.join(GALLERY_DIR, "all_styles.png"),
        dpi=GRID_DPI,
        suptitle="komorebi_mpl — the same plot in every style",
        titles=list(styles),
    )


# ── main ───────────────────────────────────────────────────────────────────

PLOT_FUNCS = [
    ("line plot", plot_lines),
    ("scatter", plot_scatter),
    ("bar chart", plot_bars),
    ("histogram", plot_histogram),
    ("histogram + Gaussian fit", plot_hist_fit),
    ("2D histogram", plot_hist2d),
    ("fill between", plot_fill),
    ("error bars", plot_errorbar),
    ("box plot", plot_boxplot),
    ("multi-panel", plot_multipanel),
    ("shared axes", plot_shared_axes),
    ("log scale", plot_logscale),
    ("image & colormap", plot_colormap),
    ("annotations", plot_annotations),
    ("typography", plot_typography),
]

NIGHT_WAVE_EXTRAS = [
    ("line glow", plot_night_wave_line_glow),
    ("glow + gradient", plot_night_wave_glow_gradient),
    ("bar gradient", plot_night_wave_bars),
    ("hist gradient", plot_night_wave_hist_gradient),
    ("scatter glow", plot_night_wave_scatter_glow),
]

if __name__ == "__main__":
    args = sys.argv[1:]
    gallery_only = "--gallery" in args
    requested = [a for a in args if a != "--gallery"] or STYLES

    unknown = [s for s in requested if s not in STYLES]
    if unknown:
        raise SystemExit(f"unknown style(s): {', '.join(unknown)}\nknown: {', '.join(STYLES)}")

    if gallery_only:
        print("Building README gallery…")
        build_gallery(requested)
        raise SystemExit(f"\nGallery written to: {GALLERY_DIR}{os.sep}")

    for style in requested:
        print(style)
        for label, fn in PLOT_FUNCS:
            print(f"  {label}")
            fn(style)

        if style == "night_wave":
            for label, fn in NIGHT_WAVE_EXTRAS:
                print(f"  {label} (night_wave extra)")
                fn()

        print("  overview")
        make_overview(style)

    print(f"\nFigures saved to: {OUT_DIR}{os.sep}<style>{os.sep}")
