"""Frigate."""

import os.path

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates")
DOTFILE_NAME = ".frigate"
