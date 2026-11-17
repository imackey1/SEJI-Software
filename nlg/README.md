# nlg: Natural Language Generator

Gives every file a voice. It takes a file's metadata plus a battle situation and returns one line of dialogue.

```python
from nlg import generate_dialogue, situations

generate_dialogue(item, situations.ENEMY_INTRO)                         # enemy's opening taunt
generate_dialogue(item, situations.ATTACK, character_class="Mage")      # class-specific attack shout
```

`item` can be a `scanner.DesktopItem` (what the game passes), any object with the same field names, or a plain dict. `character_class` takes `"Barbarian"` / `"Mage"` / `"Rogue"` or `classes_loot_equipment.FighterClass`.

## Files

- `dialogue_library.py` holds every line of dialogue, grouped by situation, class, and trait.
- `dialogue_situations.py` holds the situation names: `INTRO`, `ENEMY_INTRO`, `ATTACK`, `DAMAGE`, `LOW_HEALTH`, `DODGE`, `VICTORY`, `DEFEAT`.
- `metadata_interpreter.py` turns metadata into traits (`small`, `old`, `hidden`, `text_heavy`, ...).
- `natural_language_generator.py` picks the line.
- `tests/` has the unit tests.

## Tests

From the project root:

```
python -m unittest discover -v
```
