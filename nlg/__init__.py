"""
nlg - Natural Language Generator
--------------------------------
Turns a file's metadata (a scanner.DesktopItem, or a plain dict) plus a
battle situation into a line of dialogue.

    from nlg import generate_dialogue, situations
    line = generate_dialogue(item, situations.ATTACK, character_class="Mage")

`character_class` accepts the plain string ("Barbarian" / "Mage" /
"Rogue") or classes_loot_equipment.FighterClass.
"""

from . import dialogue_situations as situations
from .metadata_interpreter import interpret_metadata
from .natural_language_generator import (
    generate_dialogue,
    generate_enemy_dialogue,
    generate_intro,
)

__all__ = [
    "generate_dialogue",
    "generate_enemy_dialogue",
    "generate_intro",
    "interpret_metadata",
    "situations",
]
