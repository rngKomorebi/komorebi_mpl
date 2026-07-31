# komorebi_mpl

![Tests](https://github.com/rngKomorebi/komorebi_mpl/actions/workflows/tests.yml/badge.svg)
![PyPI - Version](https://img.shields.io/pypi/v/komorebi_mpl)
![PyPI - License](https://img.shields.io/pypi/l/komorebi_mpl)

A collection of matplotlib style sheets for scientific plots — from
publication-ready and greyscale-print-safe to warm parchment and neon-on-dark.

Every sheet is built on **one shared template**: the same 66 parameters in the
same order, so styles differ only in their values and switching between them
never leaves a stray matplotlib default behind.

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/all_styles.png" width="900">

## Installation

```
pip install komorebi_mpl
```

## Usage

`use()` applies a style and hands back `pyplot`, ready to go:

```python
import komorebi_mpl as kmpl

plt = kmpl.use("sci_pub")
plt.plot([i for i in range(30)])
```

Or register the styles and drive matplotlib yourself:

```python
from matplotlib import pyplot as plt
import komorebi_mpl  # importing registers the styles

plt.style.use("sci_faded")
plt.plot([i for i in range(30)])
```

### As a package default

`use()` marks your choice as final; `apply_default()` is the library-safe
counterpart that steps aside once a user has chosen. A package can set its own
look on import without ever clobbering an explicit selection, whatever the
import order:

```python
# in yourpackage/__init__.py
import komorebi_mpl
komorebi_mpl.apply_default("dapkel")   # no-op if the user already called use()
```

This is how [dapkel](https://github.com/rngKomorebi/dapkel) and
[daplis](https://github.com/rngKomorebi/daplis) pick up their house styles.

| function | what it does |
|---|---|
| `use(name)` | apply a style, close open figures, lock it as the user's choice, return `pyplot` |
| `apply(name)` | apply a style to the current rcParams without touching open figures |
| `apply_default(name)` | apply a package default; a no-op once `use()` has been called |
| `unlock()` | clear the lock so `apply_default()` can take effect again |
| `style_path(name)` | on-disk path of a bundled sheet |

## Styles

| Style | Look | Background | Best for |
|---|---|---|---|
| `sci_pub` | colorblind-safe rebeccapurple + Okabe-Ito, linestyle & marker cycling | white | journal figures |
| `sci_pure` | vivid, clean, linestyle & marker cycling | white | papers, slides |
| `sci_print` | no colour at all; series told apart by linestyle and marker | white | greyscale print |
| `sci_faded` | soft desaturated colours, graph-paper grid | aged paper `#F1EBDE` | a gentler paper look |
| `minimal` | Tufte-inspired; no grid, outward ticks, bottom-left spines only | white | data-forward figures |
| `solarized` | Ethan Schoonover's Solarized light | `#FDF6E3` | easy on the eyes |
| `earth` | terracotta, rust, olive, sage | parchment `#F5ECD7` | posters, warm decks |
| `komorebi` | 木漏れ日 — forest canopy gold, green and sky blue | parchment `#FAF8F0` | posters, talks |
| `blueprint` | white and ice-blue lines, like a CAD drawing | deep navy `#0D1F3C` | dark slides |
| `night_wave` | neon synthwave, with optional glow and gradient helpers | `#221D2F` | dark slides |
| `dapkel` | green-to-blue house style of the dapkel package | white | Kelpie analysis |
| `daplis` | colorblind-accessible house style of the daplis package, outward ticks | white | LinoSPAD2 analysis |

Each block below shows a line plot, a histogram with a Gaussian fit, a box plot
and the annotation set, all in that style.

<details>
<summary><b>sci_pub</b> — colorblind-safe publication style</summary>

Anchored on rebeccapurple and darkorange, with the rest drawn from Okabe-Ito so
the series stay distinguishable under protanopia, deuteranopia and tritanopia.
Linestyle and marker cycling give a second differentiation axis, so the figure
also survives black-and-white reproduction.

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/sci_pub.png" width="800">
</details>

<details>
<summary><b>sci_pure</b> — clean and vivid</summary>

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/sci_pure.png" width="800">
</details>

<details>
<summary><b>sci_print</b> — greyscale only</summary>

Every series is black. They are told apart by linestyle alone *or* by marker
alone, so nothing is lost when the journal prints in greyscale. Legends and
text boxes are white with a black border, for minimum ink.

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/sci_print.png" width="800">
</details>

<details>
<summary><b>sci_faded</b> — sun-faded paper</summary>

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/sci_faded.png" width="800">
</details>

<details>
<summary><b>minimal</b> — Tufte-inspired</summary>

No grid, outward ticks, no minor ticks, only the bottom and left spines, and a
frameless legend. The grid and minor-tick parameters are still declared in the
sheet, so re-enabling them gives a coherent look rather than matplotlib defaults.

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/minimal.png" width="800">
</details>

<details>
<summary><b>solarized</b> — Solarized light</summary>

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/solarized.png" width="800">
</details>

<details>
<summary><b>earth</b> — warm and natural</summary>

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/earth.png" width="800">
</details>

<details>
<summary><b>komorebi</b> — 木漏れ日, sunlight through leaves</summary>

The Japanese word for the dappled interplay of light and shadow under a forest
canopy: deep gold for the sunlight shafts, forest green for the foliage, sky
blue for the glimpses of sky, sienna for bark, leaf green and a dusk lavender.

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/komorebi.png" width="800">
</details>

<details>
<summary><b>blueprint</b> — CAD drawing</summary>

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/blueprint.png" width="800">
</details>

<details>
<summary><b>night_wave</b> — neon on dark</summary>

Heavily inspired by Dominik Haitz's
[mplcyberpunk](https://github.com/dhaitz/mplcyberpunk). This is the one style
with helper functions: `komorebi_mpl.functions.night_wave_func` adds glow to
lines and scatter points, and gradient fills under lines, bars and histograms.

```python
import komorebi_mpl as kmpl
from komorebi_mpl.functions import night_wave_func

plt = kmpl.use("night_wave")
fig, ax = plt.subplots()
ax.plot(x, y)
night_wave_func.make_lines_glow(ax)
```

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/night_wave.png" width="800">

Glow and gradient, applied to lines, bars, histograms and scatter:

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/examples/figures/night_wave_style%2Bneon%2Bgrad.png" width="700">
</details>

<details>
<summary><b>dapkel</b> — green to blue</summary>

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/dapkel.png" width="800">
</details>

<details>
<summary><b>daplis</b> — colorblind-accessible, outward ticks</summary>

The eight-colour cycle maps onto recurring roles in the daplis plots:
rebeccapurple for primary data, darkorange for fits, teal for single-pixel
histograms, salmon for the full sensor, and so on.

<img src="https://raw.githubusercontent.com/rngKomorebi/komorebi_mpl/main/docs/gallery/daplis.png" width="800">
</details>

## Examples

- **[`examples/style_showcase.py`](https://github.com/rngKomorebi/komorebi_mpl/blob/main/examples/style_showcase.py)** — every style
  rendered across 14 plot types. Run it to produce the full set locally:

  ```
  python examples/style_showcase.py                  # all styles
  python examples/style_showcase.py komorebi earth   # only these
  python examples/style_showcase.py --gallery        # rebuild docs/gallery/
  ```

  Output lands in `examples/figures/showcase/<style>/`, with the same 14
  filenames in every folder — so two styles can be compared by opening the same
  name twice — plus a `00_overview.png` contact sheet per style. The data is
  regenerated from a fixed seed inside each plot function, so every style shows
  identical numbers. This output is gitignored; `docs/gallery/` holds the small
  committed subset shown above.

- **[`examples/plot_examples.py`](https://github.com/rngKomorebi/komorebi_mpl/blob/main/examples/plot_examples.py)** — short,
  self-contained snippets per style and per `night_wave` helper.

## Style structure

Every sheet declares the **same 66 parameters in the same section order** —
Fonts, Figure, Axes, Ticks, Grid, Legend, Lines & markers, Box plots, Text
boxes, Colors. Only the values differ. That makes styles diffable against each
other, and it means switching styles never leaves a parameter sitting at a
matplotlib default that some other style happened to set.

Three conventions are worth knowing:

- **Typography is one scale in every style.** `font.size: 30` is the base and
  every other slot is deliberately smaller (`axes.titlesize: 28`,
  `axes.labelsize: 26`, tick labels `22`, `legend.fontsize: 20`). Free-floating
  text has no rcParam of its own, so in your own code use matplotlib *relative*
  sizes (`fontsize="small"`, `"x-small"`, ...) — they are fractions of that base
  and therefore follow the style too.
- **Text boxes mirror the legend.** `patch.facecolor` / `patch.edgecolor` are
  set to the same values as `legend.facecolor` / `legend.edgecolor`, so a text
  box and a legend are visually the same object. `patch.*` also colours box
  plots drawn with `patch_artist=True`.
- **Box plots use the style's ink.** Matplotlib defaults
  `boxplot.boxprops.color`, `.whiskerprops.color`, `.capprops.color` and
  `.flierprops.*` to literal `black`, which disappears on a dark background, so
  every style sets them to its own tick colour. Medians and means already follow
  the property cycle (`C1` / `C2`) and are left alone.

### Text boxes and annotations

`ax.text(...)` and `ax.annotate(...)` pick up the style automatically as long as
you don't pass explicit colours — give the `bbox` only a shape:

```python
ax.text(0.02, 0.97, "Annotation", transform=ax.transAxes, va="top",
        bbox=dict(boxstyle="round,pad=0.4"))   # colours come from patch.*
```

### Where matplotlib ignores the style

Two places hardcode colours that a style ought to own, and neither has an
rcParam behind it, so they have to be passed by hand:

- **`ax.bar(..., yerr=...)`** draws its error bars with `ecolor='k'`, hardcoded.
  On the dark styles that is a black error bar on a near-black background:

  ```python
  ax.bar(x, y, yerr=err, ecolor=plt.rcParams["text.color"])
  ```

- **`matplotlib.offsetbox.AnchoredText`** hardcodes a white face and a black
  edge and ignores `patch.*` entirely. Under `night_wave`, whose text is
  near-white, that produces a white box with invisible text:

  ```python
  import matplotlib as mpl
  from matplotlib.offsetbox import AnchoredText

  at = AnchoredText("text", loc="upper right", frameon=True)
  at.patch.set_facecolor(mpl.rcParams["patch.facecolor"])
  at.patch.set_edgecolor(mpl.rcParams["patch.edgecolor"])
  ax.add_artist(at)
  ```

## Adding or editing a style

Copy any existing sheet in [`src/komorebi_mpl/styles/`](https://github.com/rngKomorebi/komorebi_mpl/blob/main/src/komorebi_mpl/styles/)
and change the values, keeping every parameter and the section order intact —
the test suite enforces this:

```
pip install pytest
pytest tests/
```

The tests check that all sheets share one parameter set in one order, apply
without matplotlib warnings, keep text boxes and legends in agreement, and draw
nothing that vanishes into its own background.

## Acknowledgment

Shout-out to Dominik Haitz, who wrote the mindblowing
[mplcyberpunk](https://github.com/dhaitz/mplcyberpunk) package, and from which
the `night_wave` helper functions are adapted. Also check out John Garrett's
[SciencePlots](https://github.com/garrettj403/SciencePlots) for
publication-ready plots.

## License and contact info

This package is available under the MIT license. See [LICENSE](https://github.com/rngKomorebi/komorebi_mpl/blob/main/LICENSE) for
more information. If you'd like to contact me, the author, feel free to write at
sergei.kulkov23@gmail.com.
