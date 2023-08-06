"""
wbpNamespace
===============================================================================

Tree view to inspect the namespace of the application
"""

from .config import NameSpacePreferences
from .control import nameSpacePanel

__version__ = "0.1.8"


panels = [nameSpacePanel]
preferencepages = [NameSpacePreferences]
