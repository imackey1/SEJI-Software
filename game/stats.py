"""
stats.py
--------
PLACEHOLDER combat numbers, so the UI has real HP / ATK / Speed to show
for scanned files. Nobody on the team has designed balance yet. These
exist only so the pieces connect, and every number in this file is meant
to be changed.

Each class gets a base stat line. Each individual file then gets a small,
repeatable variation (up to +/-10%, derived from its filename), so two
Barbarians aren't identical twins but the same file always gets the same
stats.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from classes_loot_equipment import FighterClass

# Variation applied per file, as a fraction of the base stat.
STAT_VARIATION = 0.10

BASE_STATS = {
    #                      hp   atk  speed
    FighterClass.BARBARIAN: (90, 14, 30),   # tanky, slow
    FighterClass.MAGE:      (60, 20, 45),   # fragile, hits hardest
    FighterClass.ROGUE:     (55, 12, 70),   # fragile, fastest
}

CLASS_DESCRIPTIONS = {
    FighterClass.BARBARIAN: "A powerful fighter with high health.",
    FighterClass.MAGE: "A careful and strategic fighter.",
    FighterClass.ROGUE: "A fast and unpredictable fighter.",
}


@dataclass(frozen=True)
class Stats:
    hp: int
    atk: int
    speed: int


def _variation(seed: str, stat_name: str) -> float:
    """A repeatable number between -STAT_VARIATION and +STAT_VARIATION."""
    digest = hashlib.sha1(f"{seed}|{stat_name}".encode("utf-8")).digest()
    unit = int.from_bytes(digest[:4], "big") / 0xFFFFFFFF  # 0.0 .. 1.0
    return (unit * 2 - 1) * STAT_VARIATION


def base_stats(fighter_class: FighterClass, seed: str = "") -> Stats:
    hp, atk, speed = BASE_STATS[FighterClass(fighter_class)]
    if not seed:
        return Stats(hp, atk, speed)
    return Stats(
        hp=max(1, round(hp * (1 + _variation(seed, "hp")))),
        atk=max(1, round(atk * (1 + _variation(seed, "atk")))),
        speed=max(1, round(speed * (1 + _variation(seed, "speed")))),
    )
