# Desktop Warfare

The software developed by SEJI for GSU's Software Engineering class. Desktop Warfare is a roguelike that turns the files on your Windows desktop into fighters and items. A big video becomes a Barbarian, a long essay becomes a Mage, a hidden file becomes a Rogue, and they talk trash to each other while they fight.

## How the pieces connect

```
scanner  ->  classes_loot_equipment  ->  game (stats + glue)  ->  ui
                                              |
                                             nlg (dialogue)
```

| Folder | What it does | Branch / owner |
|---|---|---|
| `scanner/` | Reads the desktop: names, sizes, flags, dates, icons, word counts. Never changes anything. | `metadata-reader` |
| `classes_loot_equipment/` | Decides fighter (Barbarian / Mage / Rogue) or item (Equipment / Grenade / Heal / Junk). | `classes-loot-equipment` |
| `nlg/` | Generates dialogue from a file's metadata and the battle situation. | `natural-language-generator` |
| `ui/` | pygame screens: main menu, character select, battle. | `ui-ux` |
| `game/` + `run_game.py` | Glue that connects the four modules, plus placeholder stats. | `main` |

There's one record type for the whole project: `scanner.DesktopItem`. Every module reads it directly, so nobody needs to convert between file-record classes.

## Setup

Python 3.10 or newer.

```
pip install -r requirements.txt
```

## Run

From this folder (the project root):

```
python run_game.py                          # scans your real desktop
python run_game.py --folder "C:\some\folder"  # scans a test folder instead
python run_game.py --demo                   # no scan, demo characters
```

Each module can also run by itself:

```
python -m scanner.preview                 # scanner icon preview window
python -m classes_loot_equipment.demo     # prints what every desktop file becomes
python -m ui.main                         # UI with demo characters
```

Always run from the project root with `python -m ...`. Running a file directly from inside its folder breaks the imports.

## Tests

No extra install needed:

```
python -m unittest discover -v
```

## Ground rules for keeping it compatible

- Classification rules live only in `classes_loot_equipment/classification.py`.
- Every line of dialogue lives only in `nlg/dialogue_library.py`.
- Combat numbers live only in `game/stats.py`. They're placeholders until we design balance.
- The UI only draws the dicts it's handed (shape documented in `game/roster.py`). It never imports the scanner or the classifier.
- Nothing ever writes to, moves, or deletes a file on the player's desktop.
