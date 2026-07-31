# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-30

Every style sheet rebuilt onto one shared parameter template, two new styles,
and a set of fixes for places where matplotlib's hardcoded colours were leaking
through and breaking the darker styles.

**This release changes how existing styles render.** Tick labels, titles and
legends are smaller, and several box and border colours moved. Pin `0.0.5` if
you need the previous look.

### Added

- `dapkel` style — green-to-blue house style of the
  [dapkel](https://github.com/rngKomorebi/dapkel) Kelpie analysis package.
- `daplis` style — colorblind-accessible house style of the
  [daplis](https://github.com/rngKomorebi/daplis) LinoSPAD2 analysis package,
  moved here from that repository so there is one source of truth.
- `style_path(name)`, returning the on-disk path of a bundled sheet. Lets a
  package expose its own style location without shipping a copy of the file.
- A **Box plots** section in every sheet
  (`boxplot.boxprops.color`, `.whiskerprops.color`, `.capprops.color`,
  `.flierprops.color`, `.flierprops.markeredgecolor`). Matplotlib defaults these
  to literal `black`, which is invisible on `night_wave` and `blueprint`.
- Test suite (`tests/test_styles.py`) asserting the template invariants: every
  sheet declares the same parameters in the same order, applies without
  warnings, keeps text boxes and legends in agreement, and draws nothing that
  vanishes into its own background. Run on 3.9 / 3.11 / 3.13 in CI.
- `docs/gallery/` with a comparison grid across all styles and a four-plot card
  per style, rebuilt by `python examples/style_showcase.py --gallery`.
- `CHANGELOG.md`, `[project.urls]`, keywords and trove classifiers.

### Changed

- **All 12 sheets now declare the same 66 parameters in the same section
  order** — Fonts, Figure, Axes, Ticks, Grid, Legend, Lines & markers, Box
  plots, Text boxes, Colors — so any two styles differ only in their values.
  Previously the sheets ranged from 12 to 55 parameters with no common order.
- **One typography scale everywhere**: `font.size: 30` as the base with every
  other slot deliberately smaller (`axes.titlesize: 28`, `axes.labelsize: 26`,
  tick labels `22`, `legend.fontsize: 20`). Previously most styles left tick
  labels at the 30 pt base and used `axes.titlesize: 32`.
- **Text boxes mirror the legend** in every style: `patch.facecolor` and
  `patch.edgecolor` now equal `legend.facecolor` and `legend.edgecolor`.
- `daplis` ticks point outward; every other style keeps inward ticks.
- `night_wave` text-box and legend borders are `#5E5278` instead of black and
  the figure background respectively.
- `sci_print` legends and text boxes are white with a black border, for minimum
  ink in greyscale print.
- Minimum matplotlib raised to 3.9 and `requirements.txt` switched from exact
  pins to matching ranges. Minimum Python is now 3.9, following matplotlib.
- `examples/style_showcase.py` rewritten: one folder per style under
  `examples/figures/showcase/<style>/`, the same 14 filenames in each so styles
  can be diffed by opening the same name twice, a contact sheet per style, and
  fixed-seed data so every style plots identical numbers.

### Fixed

- **`dapkel` and `daplis` text boxes were illegible.** Neither sheet set
  `patch.facecolor`, so matplotlib fell back to `C0` — the first colour of the
  cycle — putting dark text on a dark blue or rebeccapurple box.
- **Invisible legend frames** in `sci_faded` and `sci_pure`, where
  `legend.edgecolor` equalled `legend.facecolor`.
- `axes.edgecolor` was undeclared in `sci_faded` and `sci_pure`, leaving them on
  the matplotlib default while every other style tinted its spines.
- Trailing comma in `font.sans-serif` producing an empty font-family entry.
- Inconsistent value syntax: bare `ffffff` without `#`, unquoted hex, and
  numeric greys mixed with hex.
- Stale comments describing colours the styles no longer used — `sci_faded` and
  `sci_pure` documented "very light grey" text over black and a "bluish dark
  grey" background over parchment.

### Known matplotlib limitations

Documented in the README, since no style sheet can reach them:

- `ax.bar(..., yerr=...)` hardcodes `ecolor='k'` with no rcParam behind it.
- `matplotlib.offsetbox.AnchoredText` hardcodes a white face and black edge and
  ignores `patch.*` entirely.

## [0.0.5] - 2026-03-27

### Added

- `blueprint`, `earth`, `minimal`, `sci_print`, `sci_pub` and `solarized` styles.

## [0.0.4] - 2026-03-27

### Fixed

- Version metadata.

## [0.0.3] - 2026-03-27

### Fixed

- Packaging: style sheets are now included in the distribution.

## [0.0.2] - 2026-03-27

### Changed

- Project renamed to `komorebi_mpl` and prepared for PyPI.
