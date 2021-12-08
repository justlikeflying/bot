import importlib
import inspect
import pkgutil
from typing import Iterator, NoReturn

from bot import exts


def unqualify(name: str) -> str:
    """Return an unqualified name given a qualified module/package `name`."""
    return name.rsplit(".", maxsplit=1)[-1]


def ignore_module(module) -> bool:
    """Return whether the module with name `name` should be ignored."""
    return any(name.startswith("_") for name in module.name.split("."))


def walk_extensions() -> Iterator[str]:
    """Yield extension names from the bot.exts subpackage."""

    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)  # pragma: no cover

    for module in pkgutil.walk_packages(exts.__path__, f"{exts.__name__}."):
        if ignore_module(module):
            # Ignore modules/packages that have a name starting with an underscore anywhere in their trees.
            continue

        if module.ispkg:
            imported = importlib.import_module(module.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
                # If it lacks a setup function, it's not an extension.
                continue

        yield module.name


EXTENSIONS = frozenset(walk_extensions())
