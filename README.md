
Readme · MD
# Desktop Warfare: Scanner & Metadata Reader
 
Part of **Desktop Warfare** by SEJI Software (Shermara, Evan, Jason, and Ibrahim), a roguelike that uses the player's own Windows desktop as the battlefield. This module is the first stage of the pipeline: it looks at what is on the desktop and turns it into clean data the rest of the game can use.
 
> **Status:** early development. Windows only for now.
 
## What this module does
 
- Scans the desktop and collects the apps/files found there.
- Extracts each app's icon (including icons stored inside `.exe` files) so it can be drawn in the game.
- Provides a small preview window to check scanner output before it is wired into the game.
The scanner only reads metadata (names, sizes, flags, icons). It never modifies, moves, or deletes anything.
 
## Requirements
 
| Package | Why it is needed |
|---|---|
| `pygame` | Opens the game window and draws images, text, and shapes. |
| `Pillow` | Opens and resizes icon files, then hands pygame a format it understands. |
| `icoextract` | Pulls the icon out of a Windows `.exe` so Pillow can open it like a normal image. |
 
Install:
 
```
pip install pygame Pillow icoextract
```
 
Or, if the dependency list is saved as `requirements.txt`:
 
```
pip install -r requirements.txt
```
 
Optional: `pip install python-docx` lets the classification module count words in `.docx` files.
 
## Project layout
 
```
scanner/
    windows_scanner.py     # scan_apps(), icon_to_pygame_surface()
preview.py                 # standalone window that shows what the scanner found
requirements.txt           # dependencies
```
 
This module feeds the separate `classes_loot_equipment` package (`metadata.py`, `classification.py`), which decides whether each file becomes a fighter (Barbarian, Mage, Rogue) or an item (Equipment, Grenade, Heal, Junk).
 
## Running the preview
 
From the project root:
 
```
python preview.py
```
 
This opens a 900x700 window showing each app found by the scanner as an icon with its name underneath (names are cut to 10 characters). The console prints how many apps were found, plus a message for any icon that failed to load. Close the window to quit.
 
## Public functions
 
### `scan_apps()`
 
Runs the scanner once and returns a list of apps. Each app is a dictionary with at least:
 
| Key | Meaning |
|---|---|
| `name` | Display name of the app/file |
| `icon_path` | Path to the icon source, or empty if none was found |
 
### `icon_to_pygame_surface(icon_path, size)`
 
Loads an icon (using Pillow and, for `.exe` files, icoextract), resizes it to `size` (for example `(48, 48)`), and returns a `pygame.Surface` ready to draw. It can raise an exception if the icon cannot be read, so callers should wrap it in `try/except`, as `preview.py` does.
 

## Known limitations / TODO
 
- Windows only.
- Icons that cannot be extracted are skipped, so some entries may appear without a picture.
- Only the top level of the desktop is scanned (no recursion into folders yet).
- Created/modified dates are not collected yet.
## Privacy
 
Only metadata is read. File contents are never sent anywhere, and nothing on the user's desktop is changed.
