"""
windows_scanner.py
------------------
First stage of the Desktop Warfare pipeline: look at the user's desktop and
turn what is on it into plain data the rest of the game can use.

For every item on the desktop we collect:
    - name, extension, whether it is a folder
    - size, created and modified times
    - hidden / system flags and whether it is an online-only OneDrive file
    - a rough word count for text-like files (see word_count.py)
    - an icon image path (when we can find one)

Rules this module follows:
    - It never changes, moves or deletes the user's files. It reads file
      information, plus two small exceptions: it reads an .exe to pull its
      icon out, and it reads the text of a few document types only to count
      words (the text itself is thrown away; only the number is kept).
    - One bad file never breaks the scan. Anything unreadable is skipped.
    - Online-only OneDrive files are never opened, because opening them
      would make Windows download them. Hidden/system files and folders are
      never opened either.

Public pieces:
    get_desktop_folders()          -> which folders make up the desktop
    scan_folder(folder)            -> list[DesktopItem] for one folder
    scan_desktop()                 -> list[DesktopItem] for the whole desktop
    scan_apps()                    -> same as scan_desktop but as plain dicts
                                      (what preview.py uses)
    icon_to_pygame_surface(...)    -> turn an icon file into a pygame Surface

To hand results to the classifier, see file_records.py.
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from .word_count import WORD_COUNT_EXTENSIONS
from .word_count import count_words as _count_words

# ---------------------------------------------------------------------------
# Tunables - everything you might want to change lives up here.
# ---------------------------------------------------------------------------

# Windows puts these in every desktop. They are plumbing, not "files".
SKIP_NAMES = {"desktop.ini", "thumbs.db"}

# Files that can be used directly as their own icon picture.
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".ico"}

# Windows hides these extensions in Explorer, so we do too for display names.
NAME_STRIP_EXTENSIONS = {".lnk", ".url", ".exe"}

# Where extracted .exe icons are saved so we only extract each one once.
ICON_CACHE_DIR = Path(tempfile.gettempdir()) / "desktop_warfare_icons"

# ---------------------------------------------------------------------------
# Windows constants
# ---------------------------------------------------------------------------

FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_SYSTEM = 0x4
FILE_ATTRIBUTE_OFFLINE = 0x1000
FILE_ATTRIBUTE_RECALL_ON_OPEN = 0x40000
FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x400000

# Any of these means "the contents are not on this PC yet" (OneDrive etc.).
ONLINE_ONLY_FLAGS = (
    FILE_ATTRIBUTE_OFFLINE
    | FILE_ATTRIBUTE_RECALL_ON_OPEN
    | FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS
)

# Windows "known folder" IDs. The Desktop you see on screen is really two
# folders merged together: yours, and the Public Desktop shared by all users.
FOLDERID_DESKTOP = "{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}"
FOLDERID_PUBLIC_DESKTOP = "{C4AA340D-F20F-4863-AFEF-F87EF2E6BA25}"


@dataclass
class DesktopItem:
    """Everything we know about one item on the desktop."""

    path: Path
    name: str  # display name, e.g. "Chrome" for "Chrome.lnk"
    filename: str  # real name on disk, e.g. "Chrome.lnk"
    extension: str  # lowercase with leading dot, "" for folders
    is_folder: bool
    size_bytes: int  # 0 for folders
    created: float  # seconds since 1970 (same format as time.time())
    modified: float
    is_hidden: bool
    is_system: bool
    is_online_only: bool
    icon_path: Optional[Path] = None  # an image file Pillow can open, or None
    word_count: int = 0  # rough count for text-like files, 0 for everything else

    @property
    def is_obscured(self) -> bool:
        """True if the OS itself hides this item from a normal folder view."""
        return self.is_hidden or self.is_system

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Finding the desktop
# ---------------------------------------------------------------------------


def _known_folder_path(folder_id: str) -> Optional[Path]:
    """Ask Windows where a known folder really is (handles OneDrive moves)."""
    if sys.platform != "win32":
        return None

    import ctypes
    from ctypes import wintypes

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", ctypes.c_ubyte * 8),
        ]

    try:
        ole32 = ctypes.WinDLL("ole32")
        shell32 = ctypes.WinDLL("shell32")
        shell32.SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID),
            wintypes.DWORD,
            wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_wchar_p),
        ]
        shell32.SHGetKnownFolderPath.restype = ctypes.HRESULT
        ole32.CoTaskMemFree.argtypes = [ctypes.c_void_p]

        guid = GUID()
        if ole32.CLSIDFromString(folder_id, ctypes.byref(guid)) != 0:
            return None

        path_ptr = ctypes.c_wchar_p()
        shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None, ctypes.byref(path_ptr))
        path = path_ptr.value
        ole32.CoTaskMemFree(path_ptr)
        return Path(path) if path else None
    except (OSError, AttributeError):
        return None


def get_desktop_folders() -> list[Path]:
    """
    Return every folder that makes up the user's desktop.

    On Windows that is the user's Desktop plus the Public Desktop. If
    Windows can't tell us (or we're on another OS while developing), fall
    back to ~/Desktop.
    """
    folders: list[Path] = []
    for folder_id in (FOLDERID_DESKTOP, FOLDERID_PUBLIC_DESKTOP):
        path = _known_folder_path(folder_id)
        if path is not None and path.is_dir() and path not in folders:
            folders.append(path)

    if not folders:
        fallback = Path.home() / "Desktop"
        if fallback.is_dir():
            folders.append(fallback)
    return folders


# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------

_shell = None  # WScript.Shell COM object, created on first use


def _resolve_shortcut(lnk_path: Path) -> Optional[Path]:
    """Return the file a .lnk shortcut points to, or None if we can't tell."""
    global _shell
    try:
        if _shell is None:
            import win32com.client  # pywin32, Windows only

            _shell = win32com.client.Dispatch("WScript.Shell")
        target = _shell.CreateShortCut(str(lnk_path)).Targetpath
    except Exception:  # missing pywin32, broken shortcut, COM error...
        return None
    return Path(target) if target else None


def _extract_exe_icon(exe_path: Path) -> Optional[Path]:
    """Pull the icon out of an .exe and save it as a cached .ico file."""
    try:
        stat = exe_path.stat()
        key = f"{str(exe_path).lower()}|{stat.st_mtime_ns}|{stat.st_size}"
        cached = ICON_CACHE_DIR / (hashlib.sha1(key.encode("utf-8")).hexdigest() + ".ico")
        if cached.exists():
            return cached

        from icoextract import IconExtractor

        ICON_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        IconExtractor(str(exe_path)).export_icon(str(cached))
        return cached
    except Exception:  # no icon inside, not a real exe, library missing...
        return None


def _find_icon(path: Path, extension: str) -> Optional[Path]:
    """Work out which image file to use as the icon for this item."""
    if extension in IMAGE_EXTENSIONS:
        return path

    if extension == ".exe":
        return _extract_exe_icon(path)

    if extension == ".lnk":
        target = _resolve_shortcut(path)
        if target is None or not target.exists():
            return None
        target_ext = target.suffix.lower()
        if target_ext == ".exe":
            return _extract_exe_icon(target)
        if target_ext in IMAGE_EXTENSIONS:
            return target

    return None


def icon_to_pygame_surface(icon_path, size: tuple[int, int]):
    """
    Open an icon image, fit it into `size` (keeping its proportions) and
    return a pygame Surface ready to draw. Raises if the image can't be read,
    so callers should wrap it in try/except.
    """
    import pygame
    from PIL import Image, ImageOps

    with Image.open(icon_path) as img:
        img = ImageOps.contain(img.convert("RGBA"), size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        canvas.paste(img, ((size[0] - img.width) // 2, (size[1] - img.height) // 2), img)

    surface = pygame.image.frombytes(canvas.tobytes(), canvas.size, "RGBA")
    try:
        return surface.convert_alpha()  # faster to draw, needs a display
    except pygame.error:
        return surface


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------


def _display_name(filename: str, extension: str, is_folder: bool) -> str:
    if not is_folder and extension in NAME_STRIP_EXTENSIONS:
        return filename[: -len(extension)]
    return filename


def _read_item(
    entry: os.DirEntry, extract_icons: bool, read_word_counts: bool = True
) -> Optional[DesktopItem]:
    """Build a DesktopItem for one directory entry. None means 'skip it'."""
    filename = entry.name
    if filename.lower() in SKIP_NAMES:
        return None

    try:
        stat = entry.stat()
        is_folder = entry.is_dir()
    except OSError:  # vanished, locked, or permission denied
        return None

    attrs = getattr(stat, "st_file_attributes", 0)  # only exists on Windows
    if sys.platform == "win32":
        is_hidden = bool(attrs & FILE_ATTRIBUTE_HIDDEN)
        is_system = bool(attrs & FILE_ATTRIBUTE_SYSTEM)
    else:
        # Dev fallback for macOS/Linux: dot-files are the closest thing.
        is_hidden = filename.startswith(".")
        is_system = False
    is_online_only = bool(attrs & ONLINE_ONLY_FLAGS)

    path = Path(entry.path)
    extension = "" if is_folder else path.suffix.lower()

    icon_path = None
    if extract_icons and not is_folder and not is_online_only:
        icon_path = _find_icon(path, extension)

    # Only open a file's text if it is safe to: a real file that Windows is not
    # hiding and that is already on this PC. (Hidden/system files always become
    # Rogues in the classifier, so their word count is never needed.)
    word_count = 0
    if (
        read_word_counts
        and not is_folder
        and not is_online_only
        and not is_hidden
        and not is_system
        and extension in WORD_COUNT_EXTENSIONS
    ):
        word_count = _count_words(path, extension)

    return DesktopItem(
        path=path,
        name=_display_name(filename, extension, is_folder),
        filename=filename,
        extension=extension,
        is_folder=is_folder,
        size_bytes=0 if is_folder else stat.st_size,
        # On Windows, st_ctime is the creation time (st_birthtime on 3.12+).
        created=getattr(stat, "st_birthtime", stat.st_ctime),
        modified=stat.st_mtime,
        is_hidden=is_hidden,
        is_system=is_system,
        is_online_only=is_online_only,
        icon_path=icon_path,
        word_count=word_count,
    )


def scan_folder(
    folder: Path, extract_icons: bool = True, read_word_counts: bool = True
) -> list[DesktopItem]:
    """Scan one folder (non-recursive). Returns [] if it can't be read."""
    try:
        with os.scandir(folder) as entries:
            entry_list = list(entries)
    except OSError:
        return []

    items = []
    for entry in entry_list:
        item = _read_item(entry, extract_icons, read_word_counts)
        if item is not None:
            items.append(item)

    items.sort(key=lambda item: item.name.lower())
    return items


def scan_desktop(
    extract_icons: bool = True, read_word_counts: bool = True
) -> list[DesktopItem]:
    """Scan everything that shows on the user's desktop."""
    items: list[DesktopItem] = []
    for folder in get_desktop_folders():
        items.extend(scan_folder(folder, extract_icons, read_word_counts))
    items.sort(key=lambda item: item.name.lower())
    return items


def scan_apps() -> list[dict]:
    """
    Same as scan_desktop(), but each item is a plain dict. This keeps the
    shape preview.py was written against ("name", "icon_path", ...). The
    preview only draws pictures and names, so it skips word counting.
    """
    return [item.to_dict() for item in scan_desktop(read_word_counts=False)]
