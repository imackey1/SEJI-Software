"""
metadata.py
-----------
Pulls the raw, per-file metadata the classification system is built on:
size, hidden/system attribute flags, and a rough text-density measure
(word count) for file types we know how to read.

Everything here is a plain filesystem/content read - no elevated
permissions, no admin rights required. This only implements what
classification.py actually needs right now; extend `_count_words` as
metadata-reader adds support for more formats (PDF, PPTX, etc.).
"""

from __future__ import annotations

import ctypes
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Windows file attribute bit flags (kernel32 GetFileAttributesW).
FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_SYSTEM = 0x4
INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF

# File types we currently know how to pull a word count from.
TEXT_LIKE_EXTENSIONS = {".txt", ".md", ".csv", ".log"}


@dataclass
class FileRecord:
    """Everything the classifier needs to know about one desktop file."""

    path: Path
    name: str
    extension: str  # lowercase, includes the leading dot, e.g. ".docx"
    size_bytes: int
    is_hidden: bool
    is_system: bool
    word_count: int = 0

    @property
    def is_obscured(self) -> bool:
        """True if the OS itself hides this file from a normal folder view."""
        return self.is_hidden or self.is_system


def _get_windows_attributes(path: Path) -> tuple[bool, bool]:
    """Return (is_hidden, is_system) using the real Win32 attribute flags."""
    attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))  # type: ignore[attr-defined]
    if attrs == INVALID_FILE_ATTRIBUTES:
        return False, False
    return bool(attrs & FILE_ATTRIBUTE_HIDDEN), bool(attrs & FILE_ATTRIBUTE_SYSTEM)


def _get_posix_attributes(path: Path) -> tuple[bool, bool]:
    """
    Best-effort fallback for developing/testing on macOS or Linux, where
    there's no real equivalent of the Windows hidden/system bits.
    Dot-prefixed filenames are the closest analog to "hidden."
    """
    return path.name.startswith("."), False


def get_hidden_system_flags(path: Path) -> tuple[bool, bool]:
    if sys.platform.startswith("win"):
        return _get_windows_attributes(path)
    return _get_posix_attributes(path)


def _count_words(path: Path, extension: str) -> int:
    """
    Rough text-density measure. Returns 0 for anything we don't have a
    reader for yet - that's deliberate: a file with an unknown word
    count should never accidentally outscore a real text-heavy file on
    the Mage axis.
    """
    try:
        if extension in TEXT_LIKE_EXTENSIONS:
            content = path.read_text(errors="ignore")
            return len(content.split())

        if extension == ".docx":
            try:
                import docx  # python-docx, optional dependency
            except ImportError:
                return 0
            document = docx.Document(str(path))
            return sum(len(p.text.split()) for p in document.paragraphs)

        if extension in (".html", ".htm"):
            content = path.read_text(errors="ignore")
            # Rough tag strip - good enough for a relative ranking,
            # not meant to be a real HTML parser.
            text = re.sub(r"<[^>]+>", " ", content)
            return len(text.split())

    except (OSError, UnicodeDecodeError):
        return 0

    return 0


def read_file_record(path: Path) -> Optional[FileRecord]:
    """Build a FileRecord for one file. Returns None if it can't be read at all."""
    try:
        stat = path.stat()
    except OSError:
        return None

    extension = path.suffix.lower()
    is_hidden, is_system = get_hidden_system_flags(path)

    return FileRecord(
        path=path,
        name=path.name,
        extension=extension,
        size_bytes=stat.st_size,
        is_hidden=is_hidden,
        is_system=is_system,
        word_count=_count_words(path, extension),
    )


def scan_folder(folder: Path) -> list[FileRecord]:
    """Build FileRecords for every file directly inside `folder` (non-recursive)."""
    records: list[FileRecord] = []
    for entry in folder.iterdir():
        if entry.is_file():
            record = read_file_record(entry)
            if record is not None:
                records.append(record)
    return records
