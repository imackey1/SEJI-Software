"""
Desktop Warfare - start the game.

    python run_game.py                     # scans your real desktop
    python run_game.py --folder "C:\\some\\folder"   # scans a folder instead (good for testing)
    python run_game.py --demo              # skip scanning, use the UI's demo characters

The scan only reads metadata. Nothing on the desktop is changed.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from game import choose_lineup, make_dialogue_provider, pick_enemy, scan_and_build_roster


def main() -> None:
    parser = argparse.ArgumentParser(description="Desktop Warfare")
    parser.add_argument("--folder", action="append", type=Path,
                        help="scan this folder instead of the desktop (can repeat)")
    parser.add_argument("--demo", action="store_true",
                        help="skip scanning and use demo characters")
    args = parser.parse_args()

    from ui.main import run  # imported here so --help works without pygame

    dialogue = make_dialogue_provider()

    if args.demo:
        run(dialogue=dialogue)
        return

    roster = scan_and_build_roster(args.folder)
    print(f"Scan found {len(roster.fighters)} fighter(s) and {len(roster.items)} item(s).")

    if len(roster.fighters) < 2:
        print("Need at least 2 fighters to battle - using demo characters instead.")
        run(dialogue=dialogue)
        return

    lineup = [fighter.to_ui_dict() for fighter in choose_lineup(roster.fighters)]
    rng = random.Random()

    run(
        characters=lineup,
        pick_enemy=lambda player: pick_enemy(roster.fighters, player, rng),
        dialogue=dialogue,
    )


if __name__ == "__main__":
    main()
