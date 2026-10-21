# Scans the Windows desktop and returns a DesktopItem for each file or folder.#

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

SKIP_NAMES = {"desktop.ini", "thumbs.db"}  # Windows clutter, not real files
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".ico"}
NAME_STRIP_EXTENSIONS = {".lnk", ".url", ".exe"}  # Explorer hides these, so we do too
ICON_CACHE_DIR = Path(tempfile.gettempdir()) / "desktop_warfare_icons"

FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_SYSTEM = 0x4
# OneDrive "online-only" files show up as one of these. Opening them downloads them.
ONLINE_ONLY_FLAGS = 0x1000 | 0x40000 | 0x400000

# The desktop you see is two folders merged: yours and the shared Public Desktop
FOLDERID_DESKTOP = "{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}"
FOLDERID_PUBLIC_DESKTOP = "{C4AA340D-F20F-4863-AFEF-F87EF2E6BA25}"


@dataclass
class DesktopItem:
    path: Path
    name: str  # display name: "Chrome" for "Chrome.lnk"
    filename: str  # real name on disk: "Chrome.lnk"
    extension: str  # lowercase with the dot, "" for folders
    is_folder: bool
    size_bytes: int
    created: float  # seconds since 1970
    modified: float
    is_hidden: bool
    is_system: bool
    is_online_only: bool
    icon_path: Optional[Path] = None
    word_count: int = 0

    @property
    def is_obscured(self) -> bool:
        return self.is_hidden or self.is_system

    def to_dict(self) -> dict:
        return asdict(self)


def _known_folder_path(folder_id: str) -> Optional[Path]:
    # Asks Windows where a folder really is. Plain ~/Desktop is wrong when
    # OneDrive has moved the desktop.
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
        ole32.CoTaskMemFree(path_ptr)  # Windows owns this memory until we free it
        return Path(path) if path else None
    except (OSError, AttributeError):
        return None


def get_desktop_folders() -> list[Path]:
    folders = []
    for folder_id in (FOLDERID_DESKTOP, FOLDERID_PUBLIC_DESKTOP):
        path = _known_folder_path(folder_id)
        if path is not None and path.is_dir() and path not in folders:
            folders.append(path)

    if not folders:  # not Windows, or Windows didn't answer
        fallback = Path.home() / "Desktop"
        if fallback.is_dir():
            folders.append(fallback)
    return folders


_shell = None  # created the first time we need it


def _resolve_shortcut(lnk_path: Path) -> Optional[Path]:
    # Reads where a .lnk shortcut points, using Windows' scripting COM object
    global _shell
    try:
        if _shell is None:
            import win32com.client  # from pywin32

            _shell = win32com.client.Dispatch("WScript.Shell")
        target = _shell.CreateShortCut(str(lnk_path)).Targetpath
    except Exception:  # pywin32 missing, broken shortcut, COM error
        return None
    return Path(target) if target else None


def _extract_exe_icon(exe_path: Path) -> Optional[Path]:
    # Saves the icon inside an .exe as a .ico file, once per exe
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
    except Exception:  # exe has no icon, isn't a real exe, library missing
        return None


def _find_icon(path: Path, extension: str) -> Optional[Path]:
    if extension in IMAGE_EXTENSIONS:
        return path
    if extension == ".exe":
        return _extract_exe_icon(path)
    if extension == ".lnk":
        target = _resolve_shortcut(path)
        if target is None or not target.exists():
            return None
        if target.suffix.lower() == ".exe":
            return _extract_exe_icon(target)
        if target.suffix.lower() in IMAGE_EXTENSIONS:
            return target
    return None


def icon_to_pygame_surface(icon_path, size: tuple[int, int]):
    """Fit an icon inside `size` and return a pygame Surface. Raises if the image can't be read."""
    import pygame
    from PIL import Image, ImageOps

    with Image.open(icon_path) as img:
        img = ImageOps.contain(img.convert("RGBA"), size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        canvas.paste(img, ((size[0] - img.width) // 2, (size[1] - img.height) // 2), img)

    surface = pygame.image.frombytes(canvas.tobytes(), canvas.size, "RGBA")
    try:
        return surface.convert_alpha()
    except pygame.error:  # no window open yet
        return surface


def _display_name(filename: str, extension: str, is_folder: bool) -> str:
    if not is_folder and extension in NAME_STRIP_EXTENSIONS:
        return filename[: -len(extension)]
    return filename


def _read_item(entry, extract_icons: bool, read_word_counts: bool = True) -> Optional[DesktopItem]:
    filename = entry.name
    if filename.lower() in SKIP_NAMES:
        return None

    try:
        stat = entry.stat()
        is_folder = entry.is_dir()
    except OSError:  # file vanished, locked, or no permission
        return None

    attrs = getattr(stat, "st_file_attributes", 0)  # only exists on Windows
    if sys.platform == "win32":
        is_hidden = bool(attrs & FILE_ATTRIBUTE_HIDDEN)
        is_system = bool(attrs & FILE_ATTRIBUTE_SYSTEM)
    else:  # so the code can still be tested on Mac/Linux
        is_hidden = filename.startswith(".")
        is_system = False
    is_online_only = bool(attrs & ONLINE_ONLY_FLAGS)

    path = Path(entry.path)
    extension = "" if is_folder else path.suffix.lower()
    can_open = not (is_folder or is_online_only or is_hidden or is_system)

    icon_path = None
    if extract_icons and not is_folder and not is_online_only:
        icon_path = _find_icon(path, extension)

    # Never open folders, hidden/system files, or online-only files
    word_count = 0
    if read_word_counts and can_open and extension in WORD_COUNT_EXTENSIONS:
        word_count = _count_words(path, extension)

    return DesktopItem(
        path=path,
        name=_display_name(filename, extension, is_folder),
        filename=filename,
        extension=extension,
        is_folder=is_folder,
        size_bytes=0 if is_folder else stat.st_size,
        created=getattr(stat, "st_birthtime", stat.st_ctime),  # st_birthtime needs Python 3.12+
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
    # Scan one folder (not its subfolders). Returns [] if it can't be read
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
    return sorted(items, key=lambda item: item.name.lower())


def scan_desktop(extract_icons: bool = True, read_word_counts: bool = True) -> list[DesktopItem]:
    items = []
    for folder in get_desktop_folders():
        items.extend(scan_folder(folder, extract_icons, read_word_counts))
    return sorted(items, key=lambda item: item.name.lower())


def scan_apps() -> list[dict]:
    # Same as scan_desktop() but as plain dicts, without word counts. Used by preview.py.
    return [item.to_dict() for item in scan_desktop(read_word_counts=False)]
