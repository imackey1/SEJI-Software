# classes_loot_equipment

Turns a folder of real files into Desktop Warfare game objects: fighters
(**Barbarian** / **Mage** / **Rogue**) and items (**Equipment** /
**Grenade** / **Heal** / **Junk**).

## Where it fits

```
scanner  ->  classes_loot_equipment  ->  nlg  ->  game  ->  ui
             (this)
```

Input is the `scanner` package's `DesktopItem` list. The whole project
shares that one record type, so there's no separate file-record class in here.

## Files

- `classification.py` — the actual class/item decision rules. All of the
  tunable numbers and the extension tables live at the top of this file.
- `metadata.py` — a thin compatibility layer over `scanner`. `FileRecord`
  is now just another name for `scanner.DesktopItem`, and `scan_folder()`
  calls the shared scanner. It no longer reads files itself.
- `demo.py` — run this to sanity-check the rules against a real folder.
- `tests/` — unit tests for the rules.
- `__init__.py` — re-exports the public pieces so other modules can do
  `from classes_loot_equipment import classify_fighters, scan_folder`.

## Quick start

From the project root:

```bash
python -m classes_loot_equipment.demo                         # scans your real Desktop
python -m classes_loot_equipment.demo "C:\path\to\folder"  # scans anywhere else
python -m unittest discover -v                                # runs every test in the project
```

Word counts for `.docx` come from the scanner, which reads them without
any extra library, so python-docx is no longer needed.

## The rules, short version

**Fighter class**
1. Hidden or system-flagged → **Rogue**, no matter what else is true.
2. Otherwise, rank the file's size and word count against every other
   fighter candidate found in the same scan. Whichever axis it clears
   `FIGHTER_FLOOR_PERCENTILE` on (default: 50th percentile), and scores
   higher on, wins: **Barbarian** (size) or **Mage** (text).
3. If it clears neither axis, it's too small/light to be a notable
   Barbarian or Mage, and defaults to **Rogue** — the "unassuming, easy
   to overlook" path. This is what gives Rogue a real population instead
   of only ever catching the rare hidden-flag files.

**Folders** are neither fighters nor items. They're skipped entirely.

**Item role** (checked first — items never enter the fighter percentile
pool at all)
- **Equipment**: `.ini` `.cfg` `.json` `.xml` `.dll`
- **Grenade**: `.bat` `.cmd` `.ps1` `.sh` `.lnk`, plus `.py`/`.js` **only**
  when smaller than `SMALL_SCRIPT_SIZE_BYTES` (20 KB by default) — a
  bigger script/code file skips this and goes through fighter
  classification instead, since it's plausibly a real Mage-class file.
- **Heal**: `.bak`, or any real filename (not the display name) containing
  "backup", "copy", or "old"
- **Junk**: `.tmp` `.cache` `.log`

**Rogue-only fighter extensions** — always Rogue if they end up in
fighter classification at all (they can still lose to the hidden-flag or
floor rules above, they just can never become Barbarian/Mage):
`.url` `.dat` `.bin` `.ico` `.webp` `.gif` `.svg` `.css`

`.html`/`.htm` are **not** in that list on purpose — a short template
page defaults to Rogue via the floor rule, but a genuinely long,
text-heavy HTML page can still score high enough to become a Mage.

## Changing the rules

Every extension table and both tunable numbers live at the top of
`classification.py` — that's the one file to touch. Please don't
re-decide any of this in a different module; if a rule needs to change,
change it here so metadata-reader, NLG, the game glue, and UI/UX are all
still reading from the same source of truth.
