"""Glow and gradient effects for line, scatter, bar and histogram plots.

Each helper redraws artists already present on an axes, so call them after
plotting and before saving. Built for the ``night_wave`` style, but they work
on any of the bundled sheets.
"""

# PEP 585 builtin generics ('list[Line2D]') are used directly: they are valid
# at runtime from Python 3.9 on, which is this package's floor.
from typing import Optional, Union

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.path import Path


def _identity(x):
    """Return ``x`` unchanged - the no-op stand-in for ``np.log``."""
    return x


def make_lines_glow(
    ax: Optional[plt.Axes] = None,
    n_glow_lines: int = 20,
    diff_linewidth: float = 1.05,
    alpha_line: float = 0.3,
    lines: Union[Line2D, list[Line2D]] = None,
) -> None:
    """
    Add a glow effect to lines in a Matplotlib axes.

    Each line is redrawn multiple times with increasing linewidth and
    low alpha to create a glowing appearance around the line.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        The axes containing the lines to enhance. Defaults to the
        current global figure.
    n_glow_lines : int, optional
        Number of additional line layers to draw for the glow effect.
        Default is 10.
    diff_linewidth : float, optional
        Increment added to the linewidth for each successive glow layer.
        Default is 1.05.
    alpha_line : float, optional
        Overall transparency of the glow effect. Divided among the glow
        layers. Default is 0.3.
    lines : matplotlib.lines.Line2D or list of Line2D, optional
        Specific line(s) to apply the glow effect to. Defaults to all
        lines in the axes.
    """
    if ax is None:
        ax = plt.gca()

    lines = ax.get_lines() if lines is None else lines
    lines = [lines] if isinstance(lines, Line2D) else lines

    alpha_value = alpha_line / n_glow_lines

    for line in lines:
        data = line.get_data(orig=False)
        linewidth = line.get_linewidth()

        try:
            step_type = line.get_drawstyle().split("-")[1]
        except Exception:
            step_type = None

        for n in range(1, n_glow_lines + 1):
            if step_type:
                (glow_line,) = ax.step(*data)
            else:
                (glow_line,) = ax.plot(*data)
            glow_line.update_from(line)
            glow_line.set_label("_nolegend_")

            glow_line.set_alpha(alpha_value)
            glow_line.set_linewidth(linewidth + (diff_linewidth * n))
            glow_line.is_glow_line = True


def add_gradient_fill(
    ax: Optional[plt.Axes] = None,
    alpha_gradientglow: Union[float, tuple[float, float]] = 0.45,
    gradient_start: str = "bottom",
    N_sampling_points: int = 50,
) -> None:
    """
    Add a gradient fill under or around each line in a plot.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        The Matplotlib axes to draw on. Defaults to the current global
        figure.
    alpha_gradientglow : float or tuple of float
        If a single float, the gradient goes from 0 to this value.
        If a tuple (float, float), the gradient goes from
        alpha_gradientglow[0] to alpha_gradientglow[1].
    gradient_start : {'min', 'max', 'bottom', 'top', 'zero'}, optional
        Sets the reference point for the gradient:
            - 'min' (default): gradient starts at the minimum of each
            curve (fills below the curve)
            - 'max': gradient starts at the maximum of each curve (fills
            above the curve)
            - 'bottom': gradient starts at the bottom of the figure
            - 'top': gradient starts at the top of the figure
            - 'zero': gradient fills both above and below the curve
    N_sampling_points : int, optional
        Number of points used to sample the gradient. Higher values
        improve visual quality at the cost of performance.
    """
    choices = ["min", "max", "top", "bottom", "zero"]
    if gradient_start not in choices:
        raise ValueError(f"key must be one of {choices}")
    if isinstance(alpha_gradientglow, float):
        alpha_gradientglow = (0.0, alpha_gradientglow)
    if not (
        isinstance(alpha_gradientglow, tuple)
        and len(alpha_gradientglow) == 2
        and all(isinstance(bound, float) for bound in alpha_gradientglow)
    ):
        raise ValueError(
            "alpha_gradientglow must be a float or a tuple of two "
            f"floats but is {alpha_gradientglow}"
        )
    if not ax:
        ax = plt.gca()

    # because ax.imshow changes axis limits, save current xy-limits to
    # restore them later:
    xlims, ylims = ax.get_xlim(), ax.get_ylim()

    for line in ax.get_lines():
        # don't add gradient fill for glow effect lines:
        if hasattr(line, "is_glow_line") and line.is_glow_line:
            continue

        fill_color = line.get_color()
        zorder = line.get_zorder()
        alpha = line.get_alpha()
        alpha = 1.0 if alpha is None else alpha
        rgb = mcolors.colorConverter.to_rgb(fill_color)
        z = np.empty((N_sampling_points, 1, 4), dtype=float)
        z[:, :, :3] = rgb

        # find the visual extend of the gradient
        x, y = line.get_data(orig=False)
        x, y = np.array(x), np.array(y)  # enforce x,y as numpy arrays
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()
        Ay = {
            "min": ymin,
            "max": ymax,
            "top": ylims[1],
            "bottom": ylims[0],
            "zero": 0,
        }[gradient_start]
        extent = [xmin, xmax, min(ymin, Ay), max(ymax, Ay)]

        # alpha will be linearly interpolated on scaler(y)
        # {"linear","symlog","logit",...} are currentlty treated the same
        if ax.get_yscale() == "log":
            if gradient_start == "zero":
                raise ValueError("key cannot be 'zero' on log plots")
            scaler = np.log
        else:
            scaler = _identity

        a, b = alpha_gradientglow
        ya, yb = extent[2], extent[3]
        ys = np.linspace(ya, yb, N_sampling_points)

        # 'zero' ramps outward from y=0 and never divides by the span, so the
        # moment is computed only on the branches that actually need it.
        if gradient_start == "zero":
            abs_ys = np.abs(ys)
            k = abs_ys / np.max(abs_ys)
        else:
            moment = (scaler(ys) - scaler(ya)) / (scaler(yb) - scaler(ya))
            k = moment if gradient_start in ("min", "bottom") else 1 - moment

        alphas = k * b + (1 - k) * a
        z[:, :, -1] = alphas[:, None]

        im = ax.imshow(
            z,
            aspect="auto",
            extent=extent,
            alpha=alpha,
            interpolation="bilinear",
            origin="lower",
            zorder=zorder,
        )

        path = line.get_path()
        extras = Path([[xmax, Ay], [xmin, Ay]], np.full(2, Path.MOVETO))
        extras.codes[:] = Path.LINETO
        path = path.make_compound_path(path, extras)
        im.set_clip_path(path, line._transform)

    ax.set(xlim=xlims, ylim=ylims)


def add_glow_and_grad_fill(
    ax: Optional[plt.Axes] = None,
):
    """Add glow and gradient to line plots.

    Parameters
    ----------
    ax : Optional[plt.Axes], optional
        The Matplotlib axes to draw on. Defaults to the current global
        figure. Default is None.
    """
    make_lines_glow(ax)
    add_gradient_fill(ax)


def make_scatter_glow(
    ax: Optional[plt.Axes] = None,
    n_glow_lines: int = 20,
    diff_dotwidth: float = 1.2,
    alpha: float = 0.45,
) -> None:
    """
    Add a glow effect to dots in a scatter plot.

    Each scatter plot is redrawn multiple times with increasing point
    sizes to create a glowing appearance around the dots.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        The Matplotlib axes containing the scatter plot. Defaults to the
        current global figure.
    n_glow_lines : int, optional
        Number of additional scatter layers to draw for the glow effect.
        Default is 10.
    diff_dotwidth : float, optional
        Multiplicative factor by which each successive layer increases
        in size. Default is 1.2.
    alpha : float, optional
        Overall transparency of the glow effect. Default is 0.45. The
        alpha is divided among the glow layers.
    """
    if ax is None:
        ax = plt.gca()

    scatterpoints = ax.collections[-1]
    x, y = scatterpoints.get_offsets().data.T
    dot_color = scatterpoints.get_array()
    dot_size = scatterpoints.get_sizes()

    alpha = alpha / n_glow_lines

    for i in range(1, n_glow_lines):
        ax.scatter(
            x, y, s=dot_size * (diff_dotwidth**i), c=dot_color, alpha=alpha
        )


def add_bar_gradient(
    bars: mpl.container.BarContainer,
    ax: Optional[plt.Axes] = None,
    horizontal: bool = False,
) -> None:
    """
    Replace each bar in a bar plot with a rectangle filled with gradient.

    The gradient smoothly transitions from fully transparent to the
    bar's original color, creating a glowing or fading effect.

    Parameters
    ----------
    bars : matplotlib.container.BarContainer
        The bars to apply the gradient to, typically returned by
        `ax.bar()` or `ax.barh()`.
    ax : matplotlib.axes.Axes, optional
        The Matplotlib axes containing the bars. Defaults to the current
        global figure.
    horizontal : bool, optional
        If True, the gradient is applied horizontally. Otherwise, it is
        applied vertically. Default is False.
    """
    if not ax:
        ax = plt.gca()

    X = [[0, 1], [0, 1]] if horizontal else [[1, 1], [0, 0]]

    # freeze axis limits before calling imshow
    ax.axis()
    ax.autoscale(False)

    for bar in bars:
        # get properties of existing bar
        x, y = bar.get_xy()
        width, height = bar.get_width(), bar.get_height()
        zorder = bar.zorder
        color = bar.get_facecolor()

        cmap = mcolors.LinearSegmentedColormap.from_list(
            "gradient_cmap", [(color[0], color[1], color[2], 0), color]
        )

        ax.imshow(
            X=X,  # pseudo-image
            extent=[x, x + width, y, y + height],
            cmap=cmap,
            zorder=zorder,
            interpolation="bicubic",
            aspect="auto",  # to prevent mpl from auto-scaling axes equally
        )

        bar.remove()


def add_hist_gradient(
    hist_container: mpl.container.BarContainer,
    ax: Optional[plt.Axes] = None,
    horizontal: bool = False,
) -> None:
    """
    Replace each histogram bar with a rectangle filled with a gradient.

    The gradient transitions smoothly from fully transparent to the
    bar's original color, enhancing the visual appeal of the histogram.
    Works with the output of `plt.hist`.

    Parameters
    ----------
    hist_container : matplotlib.container.BarContainer
        The container of bars returned by `plt.hist(...)`.
    ax : matplotlib.axes.Axes, optional
        The Matplotlib axes to draw on. Defaults to the current global
        figure.
    horizontal : bool, optional
        If True, the gradient is applied horizontally instead of
        vertically. Default is False.
    """
    if ax is None:
        ax = plt.gca()

    # gradient orientation (pseudo-image)
    X = [[0, 1], [0, 1]] if horizontal else [[1, 1], [0, 0]]

    # freeze axis limits before overlaying
    ax.axis()
    ax.autoscale(False)

    for bar in hist_container.patches:
        # bar geometry
        x, y = bar.get_xy()
        width, height = bar.get_width(), bar.get_height()
        zorder = bar.zorder
        color = bar.get_facecolor()

        # build cmap: transparent → solid color
        cmap = mcolors.LinearSegmentedColormap.from_list(
            "gradient_cmap", [(color[0], color[1], color[2], 0), color]
        )

        ax.imshow(
            X,
            extent=[x, x + width, y, y + height],
            cmap=cmap,
            zorder=zorder,
            interpolation="bicubic",
            aspect="auto",
        )

        # remove the original solid bar
        bar.remove()


def fancy_plot(func, *args, **kwargs):
    """
    Take fig, apply glow and gradient to all lines.

    This function:
        - Applies a predefined Matplotlib style.
        - Calls the given plotting function with its arguments.
        - Adds glow to lines and gradient fills under curves.

    Parameters
    ----------
    func : callable
        The plotting function to call. Must return a Matplotlib figure.
    *args : tuple
        Positional arguments passed to the plotting function.
    **kwargs : dict
        Keyword arguments passed to the plotting function.

    Returns
    -------
    matplotlib.figure.Figure
        The figure returned by the plotting function, with glow and
        gradient effects applied.
    """
    plt.style.use("night_wave")

    fig = func(*args, show_fig=False, **kwargs)  # call original function
    ax = fig.get_axes()[0]

    # Run the functions for adding glow and gradient
    make_lines_glow(ax)
    add_gradient_fill(ax)

    return fig
