"""
roster.py
---------
Turns a scan into the fighter data the UI draws and battles with.

The UI only ever sees plain dicts, in the same shape it already used for
its demo characters:

    {
        "name": "quarterly_report.docx",
        "class": "Mage",                     # Barbarian / Mage / Rogue
        "hp": 61, "atk": 21, "speed": 44,
        "description": "A careful and strategic fighter.",
        "metadata": <scanner.DesktopItem>,   # what the NLG reads
    }

so the UI never has to import the scanner, the classifier, or the NLG.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Optional

import nlg
from classes_loot_equipment import ClassificationResult, FighterClass, classify_fighters
from scanner import DesktopItem, scan_desktop, scan_folder

from .stats import CLASS_DESCRIPTIONS, Stats, base_stats

# The order the character-select screen tries to fill, one of each first.
LINEUP_CLASS_ORDER = (FighterClass.BARBARIAN, FighterClass.MAGE, FighterClass.ROGUE)


@dataclass
class Fighter:
    item: DesktopItem
    fighter_class: FighterClass
    stats: Stats
    reason: str = ""

    def to_ui_dict(self) -> dict:
        return {
            "name": self.item.filename,
            "class": self.fighter_class.value,
            "hp": self.stats.hp,
            "atk": self.stats.atk,
            "speed": self.stats.speed,
            "description": CLASS_DESCRIPTIONS[self.fighter_class],
            "metadata": self.item,
        }


@dataclass
class Roster:
    fighters: list[Fighter] = field(default_factory=list)
    items: list[ClassificationResult] = field(default_factory=list)


def build_roster(desktop_items: Iterable[DesktopItem]) -> Roster:
    """Classify everything once (percentiles are per-scan) and attach stats."""
    results = classify_fighters(list(desktop_items))

    roster = Roster()
    for result in results.values():
        if result.role == "fighter":
            roster.fighters.append(Fighter(
                item=result.record,
                fighter_class=result.fighter_class,
                stats=base_stats(result.fighter_class, seed=result.record.filename),
                reason=result.reason,
            ))
        else:
            roster.items.append(result)

    roster.fighters.sort(key=lambda f: f.item.filename.lower())
    return roster


def scan_and_build_roster(folders: Optional[list[Path]] = None) -> Roster:
    """Scan the real desktop (or the given folders) and build a roster. Read-only."""
    if folders is None:
        items = scan_desktop()
    else:
        items = []
        for folder in folders:
            items.extend(scan_folder(Path(folder)))
    return build_roster(items)


def choose_lineup(fighters: list[Fighter], size: int = 3) -> list[Fighter]:
    """
    Pick the files offered on the character-select screen: one of each
    class if the desktop has them, biggest file first, then fill any
    leftover slots with the next-biggest files.
    """
    by_size = sorted(fighters, key=lambda f: f.item.size_bytes, reverse=True)

    lineup: list[Fighter] = []
    for fighter_class in LINEUP_CLASS_ORDER:
        match = next((f for f in by_size if f.fighter_class == fighter_class), None)
        if match is not None and len(lineup) < size:
            lineup.append(match)

    for fighter in by_size:
        if len(lineup) >= size:
            break
        if fighter not in lineup:
            lineup.append(fighter)

    return lineup


def pick_enemy(
    fighters: list[Fighter], player: dict, rng: random.Random = random
) -> Optional[dict]:
    """A random scanned fighter to battle, never the file the player picked."""
    player_item = player.get("metadata")
    player_path = getattr(player_item, "path", None)

    candidates = [f for f in fighters if f.item.path != player_path]
    if not candidates:
        return None
    return rng.choice(candidates).to_ui_dict()


def make_dialogue_provider() -> Callable[[str, dict], str]:
    """
    The function the UI calls for every line of dialogue:
        provider(situation, fighter_dict) -> str
    `situation` is one of the strings in nlg.situations.
    """
    def provide(situation: str, fighter: dict) -> str:
        metadata = fighter.get("metadata") or {
            "name": fighter.get("name", ""),
            "extension": Path(fighter.get("name", "")).suffix,
        }
        return nlg.generate_dialogue(metadata, situation, fighter.get("class"))

    return provide
