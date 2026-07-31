import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.style as style
from matplotlib import rc_params_from_file

# Path to the 'styles' folder inside the package
_styles_dir = os.path.join(os.path.dirname(__file__), "styles")

# Read all .mplstyle files in the directory and register them
_stylesheets = {
    p.stem: rc_params_from_file(p, use_default_template=False)
    for p in Path(_styles_dir).glob("*.mplstyle")
}

# Update Matplotlib's style library with your styles
style.library.update(_stylesheets)

# Update available styles so they appear in style.available
style.available[:] = sorted(style.library.keys())

# Becomes True once the user explicitly picks a style via use(). Package
# defaults applied through apply_default() then step aside, so an explicit
# user choice wins no matter the package import order.
_user_locked = False


def _spec(style_name, reset):
    """Build the argument for plt.style.use.

    ``"default"`` resets rcParams to matplotlib's built-in defaults. Otherwise
    ``reset=True`` prepends ``"default"`` so a (possibly partial) style fully
    replaces the previous one instead of layering on top of leftover params.
    """
    if style_name == "default" or not reset:
        return style_name
    return ["default", style_name]


def apply(style_name: str = "komorebi", *, reset: bool = True) -> None:
    """Apply a style to the current rcParams *without* closing any figures.

    This is the library-safe entry point: unlike 'use', it never touches the
    caller's open figures, so packages can call it at import time.

    Parameters
    ----------
    style_name : str, optional
        A registered style name (see ``matplotlib.style.available``) or
        ``"default"`` to reset to matplotlib's built-in defaults. The default
        is ``"komorebi"``.
    reset : bool, optional
        Prepend ``"default"`` so the style replaces rather than layers on the
        previous one. The default is True.
    """
    plt.style.use(_spec(style_name, reset))


def use(style_name: str = "komorebi", *, reset: bool = True):
    """Apply a style, lock it as the user's explicit choice, and return pyplot.

    Closes all open figures for a clean start and marks the style as
    user-locked so any later 'apply_default' from a package is a no-op — your
    explicit choice always wins.

    Example
    -------
    import komorebi_mpl as kmpl
    plt = kmpl.use("sci_pure")
    plt.plot(...)
    """
    global _user_locked
    _user_locked = True
    plt.close("all")
    apply(style_name, reset=reset)
    return plt


def apply_default(style_name: str) -> None:
    """Set a package's default style at import time (guarded).

    A no-op once the user has explicitly chosen a style via 'use', so packages
    can each apply their own default on import without ever clobbering the
    user's selection — regardless of the order the packages are imported.

    Parameters
    ----------
    style_name : str
        The package's default registered style name.
    """
    if _user_locked:
        return
    apply(style_name)


def unlock() -> None:
    """Clear the user lock so 'apply_default' can apply a default again."""
    global _user_locked
    _user_locked = False


def style_path(style_name: str) -> str:
    """Return the on-disk path of a bundled style sheet.

    Useful for packages that want to expose their own style file location, or
    for passing a sheet straight to ``plt.style.use`` without registration.

    Parameters
    ----------
    style_name : str
        Name of a bundled style, without the ``.mplstyle`` suffix.

    Raises
    ------
    FileNotFoundError
        If no style sheet of that name is bundled with the package.
    """
    path = os.path.join(_styles_dir, f"{style_name}.mplstyle")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"no bundled style sheet named {style_name!r} in {_styles_dir}"
        )
    return path
