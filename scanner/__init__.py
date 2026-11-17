"""The shared desktop scanner.

Other modules should import from this package and not from the inner files,
so there is one place that says what the rest of the project can rely on.
"""

from .windows_scanner import (
    DesktopItem,
    get_desktop_folders,
    icon_to_pygame_surface,
    read_item,
    scan_apps,
    scan_desktop,
    scan_folder,
)
from .word_count import count_words

__all__ = [
    "DesktopItem",
    "count_words",
    "get_desktop_folders",
    "icon_to_pygame_surface",
    "read_item",
    "scan_apps",
    "scan_desktop",
    "scan_folder",
]