"""
demo.py
-------
Quick manual test: scan a real folder (defaults to the current user's
real Desktop - including the Public Desktop and a OneDrive-moved Desktop)
and print what everything on it would become in-game.

Run from the project root:
    python -m classes_loot_equipment.demo                   # scans your real Desktop
    python -m classes_loot_equipment.demo "C:\\some\\folder"  # scans a specific folder
"""

from __future__ import annotations

import sys
from pathlib import Path

from scanner import scan_desktop, scan_folder

from .classification import classify_fighters


def main() -> None:
    if len(sys.argv) > 1:
        folder = Path(sys.argv[1])
        if not folder.is_dir():
            print(f"Folder not found: {folder}")
            return
        items = scan_folder(folder, extract_icons=False)
        where = str(folder)
    else:
        items = scan_desktop(extract_icons=False)
        where = "your Desktop"

    results = classify_fighters(items)

    print(f"\nScanned {len(items)} item(s) in {where}\n")
    for result in results.values():
        if result.role == "fighter":
            label = f"Fighter - {result.fighter_class.value}"
        else:
            label = f"Item - {result.item_role.value}"
        print(f"  {result.record.filename:<40} {label:<22} ({result.reason})")

    skipped = len(items) - len(results)
    if skipped:
        print(f"\n  ({skipped} folder(s) skipped - folders aren't fighters or items)")


if __name__ == "__main__":
    main()
