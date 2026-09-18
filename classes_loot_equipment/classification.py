"""
classification.py
------------------
Turns FileRecords into game roles:

    Fighter classes  - Barbarian / Mage / Rogue
    Item roles        - Equipment / Grenade / Heal / Junk

Decision rules (agreed in #classes-loot-equipment):

Fighter class
    1. Hidden or system-flagged -> Rogue, always, regardless of size/text.
    2. Otherwise, rank the file against the rest of the same scan on two
       axes: size percentile (Barbarian) and word-count percentile (Mage).
       Whichever axis it clears FIGHTER_FLOOR_PERCENTILE on, and scores
       higher on, decides Barbarian vs Mage.
    3. If it clears neither floor, it's too small/lightweight to be a
       notable Barbarian or Mage - it defaults to Rogue. This is the
       "unassuming, easy to overlook" path, and it's what gives Rogue a
       real population instead of only ever being the rare hidden-flag
       catch.

Item role (checked BEFORE fighter classification - an item never enters
the percentile pool, and never gets scored as a fighter)
    - Equipment: passive gear, equips onto a fighter for a stat boost.
    - Grenade:   one-time-use action effect, consumed after use.
    - Heal:      restores HP / revives an ally.
    - Junk:      no combat use, sellable/flavor only.

Small-script carve-out: .py and .js are ambiguous by design. Below
SMALL_SCRIPT_SIZE_BYTES they're Grenades (quick one-off scripts). At or
above it, they skip the item check and go through fighter classification
instead - large enough to plausibly be a real Mage-class codebase file,
not just a utility script.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from .metadata import FileRecord

# ---------------------------------------------------------------------------
# Tunables - move these to a config file once combat-testing wants to tune
# them without touching code.
# ---------------------------------------------------------------------------

# A file must be at or above this percentile (0-100) on the size or
# word-count axis to be eligible as a Barbarian or Mage at all.
FIGHTER_FLOOR_PERCENTILE = 50.0

# .py / .js at or above this size are treated as real files (fighter
# classification) instead of automatically being small-script Grenades.
SMALL_SCRIPT_SIZE_BYTES = 20_000  # ~20 KB


class FighterClass(str, Enum):
    BARBARIAN = "Barbarian"
    MAGE = "Mage"
    ROGUE = "Rogue"


class ItemRole(str, Enum):
    EQUIPMENT = "Equipment"
    GRENADE = "Grenade"
    HEAL = "Heal"
    JUNK = "Junk"


# ---------------------------------------------------------------------------
# Extension tables - see the Channel Guide / #classes-loot-equipment notes
# for the reasoning behind each of these. Keep this the single source of
# truth rather than re-deciding any of it elsewhere in the codebase.
# ---------------------------------------------------------------------------

EQUIPMENT_EXTENSIONS = {".ini", ".cfg", ".json", ".xml", ".dll"}

GRENADE_EXTENSIONS = {".bat", ".cmd", ".ps1", ".sh", ".lnk"}
SMALL_SCRIPT_EXTENSIONS = {".py", ".js"}  # Grenade only below SMALL_SCRIPT_SIZE_BYTES

HEAL_EXTENSIONS = {".bak"}
HEAL_NAME_HINTS = ("backup", "copy", "old")  # substring match, case-insensitive

JUNK_EXTENSIONS = {".tmp", ".cache", ".log"}

# Extensions that are only ever eligible to be Rogue fighters (never
# Barbarian/Mage), on top of the hidden/system-flag and size-floor rules.
ROGUE_ONLY_EXTENSIONS = {
    ".url", ".dat", ".bin", ".ico", ".webp", ".gif", ".svg", ".css",
}


@dataclass
class ClassificationResult:
    record: FileRecord
    role: str  # "fighter" or "item"
    fighter_class: Optional[FighterClass] = None
    item_role: Optional[ItemRole] = None
    reason: str = ""  # short human-readable explanation - handy for QA/debugging


def _name_hints_backup(name: str) -> bool:
    lowered = name.lower()
    return any(hint in lowered for hint in HEAL_NAME_HINTS)


def classify_item_role(record: FileRecord) -> Optional[ItemRole]:
    """Return an ItemRole if this file's extension makes it an item, else None."""
    ext = record.extension

    if ext in EQUIPMENT_EXTENSIONS:
        return ItemRole.EQUIPMENT

    if ext in GRENADE_EXTENSIONS:
        return ItemRole.GRENADE

    if ext in SMALL_SCRIPT_EXTENSIONS and record.size_bytes < SMALL_SCRIPT_SIZE_BYTES:
        return ItemRole.GRENADE

    if ext in HEAL_EXTENSIONS or _name_hints_backup(record.name):
        return ItemRole.HEAL

    if ext in JUNK_EXTENSIONS:
        return ItemRole.JUNK

    return None


def _percentile_rank(value: float, all_values: list[float]) -> float:
    """What percentage of all_values this value is greater than or equal to."""
    if not all_values:
        return 0.0
    at_or_below = sum(1 for v in all_values if v <= value)
    return 100.0 * at_or_below / len(all_values)


def classify_fighters(records: list[FileRecord]) -> dict[Path, ClassificationResult]:
    """
    Classify a batch of FileRecords into fighters and items together, since
    the size/word-count percentiles are computed relative to this batch -
    call this once per scan (e.g. once per Desktop folder), not once per file.
    """
    results: dict[Path, ClassificationResult] = {}

    # First pass: pull out items. They never enter the percentile pool -
    # an Equipment or Grenade file shouldn't skew what "big" or
    # "text-heavy" means for the remaining fighters.
    fighter_candidates: list[FileRecord] = []
    for record in records:
        item_role = classify_item_role(record)
        if item_role is not None:
            results[record.path] = ClassificationResult(
                record=record,
                role="item",
                item_role=item_role,
                reason=f"extension '{record.extension}' matches {item_role.value}",
            )
        else:
            fighter_candidates.append(record)

    sizes = [r.size_bytes for r in fighter_candidates]
    word_counts = [r.word_count for r in fighter_candidates]

    for record in fighter_candidates:
        if record.is_obscured:
            results[record.path] = ClassificationResult(
                record=record,
                role="fighter",
                fighter_class=FighterClass.ROGUE,
                reason="hidden/system attribute flag set",
            )
            continue

        if record.extension in ROGUE_ONLY_EXTENSIONS:
            results[record.path] = ClassificationResult(
                record=record,
                role="fighter",
                fighter_class=FighterClass.ROGUE,
                reason=f"extension '{record.extension}' is Rogue-only",
            )
            continue

        size_pct = _percentile_rank(record.size_bytes, sizes)
        text_pct = _percentile_rank(record.word_count, word_counts)

        clears_barbarian = size_pct >= FIGHTER_FLOOR_PERCENTILE
        clears_mage = text_pct >= FIGHTER_FLOOR_PERCENTILE

        if not clears_barbarian and not clears_mage:
            fighter_class = FighterClass.ROGUE
            reason = (
                f"below the fighter floor on both axes "
                f"(size {size_pct:.0f}th pct, text {text_pct:.0f}th pct) "
                f"- too small/light to be notable"
            )
        elif size_pct >= text_pct:
            fighter_class = FighterClass.BARBARIAN
            reason = f"size {size_pct:.0f}th percentile (text {text_pct:.0f}th)"
        else:
            fighter_class = FighterClass.MAGE
            reason = f"text {text_pct:.0f}th percentile (size {size_pct:.0f}th)"

        results[record.path] = ClassificationResult(
            record=record,
            role="fighter",
            fighter_class=fighter_class,
            reason=reason,
        )

    return results
