"""Structural and legibility tests for the bundled style sheets.

These lock in the invariants the styles are built on:

* every sheet declares the same parameters in the same order;
* every sheet is accepted by matplotlib without warnings;
* text boxes and legends share their colours;
* nothing is drawn in a colour that vanishes into its own background.
"""

import glob
import os
import warnings

import matplotlib
import pytest

matplotlib.use("Agg")

import matplotlib as mpl  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

import komorebi_mpl  # noqa: E402

STYLES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src",
    "komorebi_mpl",
    "styles",
)
SHEETS = sorted(glob.glob(os.path.join(STYLES_DIR, "*.mplstyle")))
STYLE_NAMES = [os.path.basename(p)[: -len(".mplstyle")] for p in SHEETS]

# The style all others are compared against; any sheet may play this role,
# since they are required to be identical in structure.
REFERENCE = "komorebi"

# Minimum perceived-luminance separation for something to count as visible.
MIN_CONTRAST = 0.10


def _declared_keys(path):
    """RcParam names in a sheet, in file order, comments stripped."""
    keys = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.split("#")[0].strip()
            if line and ":" in line:
                keys.append(line.split(":")[0].strip())
    return keys


def _luminance(color):
    r, g, b = mpl.colors.to_rgb(color)
    return 0.299 * r + 0.587 * g + 0.114 * b


def _contrast(a, b):
    return abs(_luminance(a) - _luminance(b))


@pytest.fixture(params=STYLE_NAMES)
def style(request):
    """Apply one style, then restore matplotlib's defaults afterwards."""
    komorebi_mpl.apply(request.param)
    yield request.param
    mpl.rcdefaults()


def test_sheets_exist():
    assert SHEETS, f"no style sheets found in {STYLES_DIR}"
    assert REFERENCE in STYLE_NAMES


def test_every_sheet_is_registered():
    for name in STYLE_NAMES:
        assert name in plt.style.available, f"{name} not registered on import"


@pytest.mark.parametrize("name", STYLE_NAMES)
def test_same_keys_in_same_order(name):
    """The whole point of the template: no sheet may drift from the others."""
    reference = _declared_keys(os.path.join(STYLES_DIR, f"{REFERENCE}.mplstyle"))
    keys = _declared_keys(os.path.join(STYLES_DIR, f"{name}.mplstyle"))

    missing = set(reference) - set(keys)
    extra = set(keys) - set(reference)
    assert not missing, f"{name} is missing {sorted(missing)}"
    assert not extra, f"{name} declares extra {sorted(extra)}"
    assert keys == reference, f"{name} declares the same keys in a different order"


@pytest.mark.parametrize("name", STYLE_NAMES)
def test_no_duplicate_keys(name):
    keys = _declared_keys(os.path.join(STYLES_DIR, f"{name}.mplstyle"))
    duplicates = {k for k in keys if keys.count(k) > 1}
    assert not duplicates, f"{name} declares {sorted(duplicates)} more than once"


@pytest.mark.parametrize("name", STYLE_NAMES)
def test_applies_without_warnings(name):
    """A bad key or value makes matplotlib warn rather than raise."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        komorebi_mpl.apply(name)
    mpl.rcdefaults()


def test_text_box_matches_legend(style):
    """patch.* must equal legend.* so a text box and a legend look alike."""
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], label="a")
    legend = ax.legend()
    text = ax.text(0.5, 0.5, "x", bbox=dict(boxstyle="round,pad=0.4"))
    fig.canvas.draw()

    box = text.get_bbox_patch()
    to_hex = mpl.colors.to_hex
    assert to_hex(box.get_facecolor()) == to_hex(legend.get_frame().get_facecolor())
    assert to_hex(box.get_edgecolor()) == to_hex(legend.get_frame().get_edgecolor())
    plt.close(fig)


def test_text_is_readable_on_its_own_box(style):
    """Guards the bug where patch.facecolor fell back to the first cycle color."""
    assert (
        _contrast(mpl.rcParams["text.color"], mpl.rcParams["patch.facecolor"])
        > MIN_CONTRAST
    ), f"{style}: text.color is illegible on patch.facecolor"


def test_box_border_is_visible(style):
    assert (
        _contrast(mpl.rcParams["patch.facecolor"], mpl.rcParams["patch.edgecolor"])
        > MIN_CONTRAST
    ), f"{style}: patch.edgecolor disappears into patch.facecolor"


def test_boxplot_artists_are_visible(style):
    """Matplotlib defaults these to literal black, invisible on dark styles."""
    background = mpl.rcParams["axes.facecolor"]
    for key in (
        "boxplot.boxprops.color",
        "boxplot.whiskerprops.color",
        "boxplot.capprops.color",
        "boxplot.flierprops.color",
        "boxplot.flierprops.markeredgecolor",
    ):
        assert (
            _contrast(mpl.rcParams[key], background) > MIN_CONTRAST
        ), f"{style}: {key} disappears into axes.facecolor"


def test_style_path_round_trip(style):
    path = komorebi_mpl.style_path(style)
    assert os.path.isfile(path)
    assert os.path.basename(path) == f"{style}.mplstyle"


def test_style_path_rejects_unknown_names():
    with pytest.raises(FileNotFoundError):
        komorebi_mpl.style_path("no_such_style")


def test_use_locks_out_package_defaults():
    """An explicit user choice must survive a package applying its default."""
    komorebi_mpl.unlock()
    try:
        komorebi_mpl.use("night_wave")
        komorebi_mpl.apply_default("sci_pub")
        assert mpl.colors.to_hex(mpl.rcParams["axes.facecolor"]) == "#221d2f"
    finally:
        komorebi_mpl.unlock()
        mpl.rcdefaults()


def test_apply_default_works_when_unlocked():
    komorebi_mpl.unlock()
    try:
        komorebi_mpl.apply_default("night_wave")
        assert mpl.colors.to_hex(mpl.rcParams["axes.facecolor"]) == "#221d2f"
    finally:
        komorebi_mpl.unlock()
        mpl.rcdefaults()
