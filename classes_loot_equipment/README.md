# classes_loot_equipment

Turns a folder of real files into Desktop Warfare game objects: fighters
(**Barbarian** / **Mage** / **Rogue**) and items (**Equipment** /
**Grenade** / **Heal** / **Junk**).

## Files

- `metadata.py` — reads the raw per-file data everything else runs on:
  size, the OS hidden/system attribute flags, and a rough word count for
  file types we know how to read (`.txt`, `.md`, `.csv`, `.log`, `.docx`,
  `.html`/`.htm`).
- `classification.py` — the actual class/item decision rules. All of the
  tunable numbers and the extension tables live at the top of this file.
- `demo.py` — run this to sanity-check the rules against a real folder.
- `__init__.py` — re-exports the public pieces so other modules can do
  `from classes_loot_equipment import classify_fighters, scan_folder`.

## Quick start

```bash
python -m classes_loot_equipment.demo                    # scans your real Desktop
python -m classes_loot_equipment.demo "C:\path\to\folder"  # scans anywhere else
```

Optional dependency: `pip install python-docx` if you want word counts
pulled from real `.docx` files. Without it, `.docx` files just get a word
count of 0 (they'll still get classified — Barbarian by size, most likely
— they just won't be eligible for Mage until that's installed).

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

**Item role** (checked first — items never enter the fighter percentile
pool at all)
- **Equipment**: `.ini` `.cfg` `.json` `.xml` `.dll`
- **Grenade**: `.bat` `.cmd` `.ps1` `.sh` `.lnk`, plus `.py`/`.js` **only**
  when smaller than `SMALL_SCRIPT_SIZE_BYTES` (20 KB by default) — a
  bigger script/code file skips this and goes through fighter
  classification instead, since it's plausibly a real Mage-class file.
- **Heal**: `.bak`, or any filename containing "backup", "copy", or "old"
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
change it here so metadata-reader, combat-testing, and UI/UX are all
still reading from the same source of truth.
