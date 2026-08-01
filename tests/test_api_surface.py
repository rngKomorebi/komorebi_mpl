"""Structural guards on the package's public API.

These tests check nothing about how a plot *looks* - they check that the
*shape* of the package holds as it grows. Three failure modes are guarded:

    1. A public function gets added (or renamed) without being declared in
       ``__all__``, so the declared surface silently drifts from the real one.

    2. A helper module stops being reachable under ``komorebi_mpl.functions``,
       which is the import path the README documents.

    3. The subpackages lose their ``__init__.py`` and become implicit
       namespace packages, which ``[tool.setuptools.packages.find]
       namespaces = false`` then quietly drops from the built wheel.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

PACKAGE_DIR = (
    pathlib.Path(__file__).resolve().parents[1] / "src" / "komorebi_mpl"
)
FUNCTIONS_DIR = PACKAGE_DIR / "functions"

# The optional plotting helpers, by module name. Add new ones here and to
# 'komorebi_mpl/functions/__init__.py' at the same time - the reexport test
# below fails if the two lists drift apart.
HELPER_MODULES = ["night_wave_func"]


def _parse(path: pathlib.Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"))


def _declared(tree: ast.Module) -> list[str]:
    """Return the module's ``__all__`` entries."""
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            getattr(t, "id", None) == "__all__" for t in node.targets
        ):
            return [e.value for e in node.value.elts]
    return []


def _defined_public_functions(tree: ast.Module) -> set[str]:
    """Public functions *defined in this module* (not imported into it)."""
    return {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    }


def test_top_level_all_declares_every_public_function() -> None:
    """``komorebi_mpl.__all__`` must list exactly the functions it defines."""
    tree = _parse(PACKAGE_DIR / "__init__.py")
    declared = set(_declared(tree))
    defined = _defined_public_functions(tree)

    assert declared, "komorebi_mpl has no __all__"
    assert not (defined - declared), (
        f"public but missing from __all__: {sorted(defined - declared)}. "
        f"Add them, or make them private with a leading underscore."
    )
    assert not (declared - defined), (
        f"in __all__ but not defined here: {sorted(declared - defined)}. "
        f"Re-exporting another module's name hides where it really lives."
    )


def test_documented_entry_points_are_importable() -> None:
    """The names the README tells people to call must actually be there."""
    import komorebi_mpl

    for name in ("apply", "apply_default", "style_path", "unlock", "use"):
        assert callable(getattr(komorebi_mpl, name, None)), (
            f"komorebi_mpl.{name} is documented but not callable"
        )


def test_version_is_exposed() -> None:
    """setuptools_scm supplies the version; the package must surface it."""
    import komorebi_mpl

    assert isinstance(komorebi_mpl.__version__, str)
    assert komorebi_mpl.__version__


@pytest.mark.parametrize("subpackage", ["", "functions"])
def test_every_subpackage_is_a_real_package(subpackage: str) -> None:
    """An implicit namespace package is silently dropped from the wheel.

    ``[tool.setuptools.packages.find] namespaces = false`` only collects
    directories carrying an ``__init__.py``, so a missing one ships a wheel
    that imports fine from the source tree and fails once installed.
    """
    init = PACKAGE_DIR / subpackage / "__init__.py"
    assert init.is_file(), f"{init.parent} has no __init__.py"


def test_functions_package_reexports_every_helper() -> None:
    """``komorebi_mpl.functions.__all__`` must list every helper module."""
    from komorebi_mpl import functions

    assert set(functions.__all__) == set(HELPER_MODULES), (
        f"komorebi_mpl.functions.__all__ is {sorted(functions.__all__)}, "
        f"expected {sorted(HELPER_MODULES)}"
    )
    for module in functions.__all__:
        assert hasattr(functions, module), f"{module} is declared but not imported"


def test_helper_modules_on_disk_match_the_declared_list() -> None:
    """A helper dropped into 'functions/' without being declared is invisible."""
    on_disk = {
        path.stem
        for path in FUNCTIONS_DIR.glob("*.py")
        if not path.stem.startswith("_")
    }
    assert on_disk == set(HELPER_MODULES), (
        f"'functions/' holds {sorted(on_disk)}, but HELPER_MODULES says "
        f"{sorted(HELPER_MODULES)}. Keep the two in step."
    )


@pytest.mark.parametrize("module", HELPER_MODULES)
def test_helpers_do_not_reach_into_private_names(module: str) -> None:
    """A helper must not import another module's private names.

    Reaching for someone else's ``_helper`` means the helper is really shared
    API and belongs somewhere both modules can import it from.
    """
    tree = _parse(FUNCTIONS_DIR / f"{module}.py")
    offenders = [
        f"{node.module}.{alias.name}"
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and (node.module or "").startswith("komorebi_mpl")
        for alias in node.names
        if alias.name.startswith("_")
    ]
    assert not offenders, (
        f"{module} imports private names from other modules: {offenders}."
    )
