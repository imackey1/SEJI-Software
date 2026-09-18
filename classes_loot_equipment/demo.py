"""
demo.py
-------
Quick manual test: scan a real folder (defaults to the current user's
Desktop) and print what everything on it would become in-game.

Usage:
    python -m classes_loot_equipment.demo                 # scans your real Desktop
    python -m classes_loot_equipment.demo "C:\\some\\folder"  # scans a specific folder
"""

from __future__ import annotations

import sys
from pathlib import Path

from .classification import classify_fighters
from .metadata import scan_folder


def default_desktop_path() -> Path:
    return Path.home() / "Desktop"


def main() -> None:
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else default_desktop_path()

    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    records = scan_folder(folder)
    results = classify_fighters(records)

    print(f"\nScanned {len(records)} file(s) in {folder}\n")
    for result in results.values():
        if result.role == "fighter":
            label = f"Fighter - {result.fighter_class.value}"
        else:
            label = f"Item - {result.item_role.value}"
        print(f"  {result.record.name:<40} {label:<22} ({result.reason})")


if __name__ == "__main__":
    main()
