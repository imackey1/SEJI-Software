"""
game
----
Glue between the four modules. Nothing here re-decides anything another
module owns. It only connects them:

    scanner.scan_desktop()                      -> DesktopItems
    classes_loot_equipment.classify_fighters()  -> fighter / item roles
    game.stats.base_stats()                     -> hp / atk / speed  (placeholder numbers)
    nlg.generate_dialogue()                     -> battle lines
    ui.main.run()                               -> pygame screens
"""

from .roster import (
    Fighter,
    Roster,
    build_roster,
    choose_lineup,
    make_dialogue_provider,
    pick_enemy,
    scan_and_build_roster,
)
from .stats import Stats, base_stats

__all__ = [
    "Fighter",
    "Roster",
    "Stats",
    "base_stats",
    "build_roster",
    "choose_lineup",
    "make_dialogue_provider",
    "pick_enemy",
    "scan_and_build_roster",
]
