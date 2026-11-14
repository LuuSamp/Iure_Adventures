"""Resolve asset paths for development and frozen (PyInstaller) builds."""

import os
import sys


def base_path() -> str:
    """Return the app root: sys._MEIPASS when frozen, else the repo root."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def resource_path(*parts: str) -> str:
    """Join path parts onto the app root for media/level assets."""
    return os.path.join(base_path(), *parts)
