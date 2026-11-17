"""
metadata.py
-----------
Compatibility layer over the shared `scanner` package.

This module used to have its own FileRecord class and its own folder
scanner. The metadata-reader team's `scanner` package now does that job
for the whole project, and it does it better: it handles the OneDrive and
Public Desktop folders, never opens online-only files, and reads .docx
without needing python-docx. So this module no longer reads anything from
disk itself. It just points at the scanner, which leaves one record type
(`scanner.DesktopItem`) for every team to agree on.

`FileRecord`, `read_file_record`, and `scan_folder` are kept as names so
older code that imports them from here keeps working.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from scanner import DesktopItem
from scanner import scan_folder as _scanner_scan_folder
from scanner.windows_scanner import _read_item

# The one shared record type. Every field classification.py needs
# (path, name, filename, extension, size_bytes, word_count, is_obscured)
# lives on DesktopItem.
FileRecord = DesktopItem


def read_file_record(path: Path) -> Optional[DesktopItem]:
    """Build a DesktopItem for one file. Returns None if it can't be read."""
    path = Path(path)
    try:
        with os.scandir(path.parent) as entries:
            for entry in entries:
                if entry.name == path.name:
                    return _read_item(entry, extract_icons=False)
    except OSError:
        return None
    return None


def scan_folder(folder: Path) -> list[DesktopItem]:
    """Every file (not folder) directly inside `folder`, as DesktopItems."""
    items = _scanner_scan_folder(Path(folder), extract_icons=False)
    return [item for item in items if not item.is_folder]
