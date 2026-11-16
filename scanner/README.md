# scanner

The shared desktop scanner for Desktop Warfare. It reads the desktop and hands
every other module the same record type, so no team keeps its own copy of this
logic.

```python
from scanner import DesktopItem, scan_desktop
```

## What you get

`DesktopItem` — one file, shortcut or folder on the desktop.

| Field | Type | Meaning |
|---|---|---|
| `path` | `Path` | Where the item really is. |
| `name` | `str` | Name to show: `Chrome` for `Chrome.lnk`. |
| `filename` | `str` | Name on disk: `Chrome.lnk`. |
| `extension` | `str` | Lowercase, with the dot. Empty for folders. |
| `is_folder` | `bool` | True for folders. |
| `size_bytes` | `int` | File size. Always `0` for folders. |
| `created` | `float` | Seconds since 1970. |
| `modified` | `float` | Seconds since 1970. |
| `is_hidden` | `bool` | Hidden flag (dot-prefix off Windows). |
| `is_system` | `bool` | System flag. |
| `is_online_only` | `bool` | OneDrive placeholder. Reading it would download it. |
| `is_obscured` | `bool` | Property: `is_hidden or is_system`. |
| `icon_path` | `Path \| None` | Where the extracted icon was saved, if any. |
| `word_count` | `int` | Rough word count for text-like files, else `0`. |
| `to_dict()` | `dict` | Plain dict of the fields above. |

Functions:

| Function | Returns |
|---|---|
| `scan_desktop(extract_icons=True, read_word_counts=True)` | Every item on the desktop, sorted by name. |
| `scan_folder(folder, extract_icons=True, read_word_counts=True)` | Every item in one folder, no recursion. |
| `scan_apps()` | Same as `scan_desktop` but as plain dicts, without word counts. |
| `get_desktop_folders()` | The desktop folders Windows actually uses. |
| `icon_to_pygame_surface(icon_path, size)` | A `pygame.Surface`. Raises if the image cannot be read. |
| `count_words(path, extension)` — imported from `scanner.word_count` | Word count, `0` if unsupported or unreadable. |

## What this package promises

- It never opens a folder, a hidden file, a system file, or an OneDrive
  online-only file. Opening the last one would download it.
- It never changes anything on the desktop. No writes, no moves, no deletes.
- Only metadata leaves the scanner: names, sizes, dates, flags, icons and word
  counts. File contents are thrown away after counting.

## Things worth knowing

- Only the top level of the desktop is scanned. Folders come back as one item
  each and their contents are not walked into.
- `icon_path` is `None` when an icon could not be extracted, so always check it.
- Word counts are rough: `.txt`, `.md`, `.csv`, `.html`, `.htm` and `.docx` are
  supported, and files over 2 MB are counted from the start of the file and
  scaled up.
- Extracted icons live in the temp folder and are shared between runs.
