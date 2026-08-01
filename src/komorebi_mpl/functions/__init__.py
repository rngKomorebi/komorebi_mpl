"""Optional plotting helpers that go with the bundled styles.

This is a real package rather than an implicit namespace one on purpose:
``[tool.setuptools.packages.find] namespaces = false`` skips any directory
without an ``__init__.py``, so without this file the helpers would import fine
from a source checkout and then be missing from the installed wheel.
"""

from . import night_wave_func

__all__ = ["night_wave_func"]
