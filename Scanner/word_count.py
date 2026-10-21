# Rough word counts for text files. Only the number is kept and the text is thrown away.

from __future__ import annotations

import codecs
import re
import zipfile
from pathlib import Path

TEXT_EXTENSIONS = {".txt", ".md", ".csv"}
HTML_EXTENSIONS = {".html", ".htm"}
DOCX_EXTENSIONS = {".docx"}
# .log is left out on purpose: the classifier always makes .log files Junk
WORD_COUNT_EXTENSIONS = TEXT_EXTENSIONS | HTML_EXTENSIONS | DOCX_EXTENSIONS

MAX_READ_BYTES = 2_000_000  # never read more than ~2 MB of a text file
MAX_DOCX_XML_BYTES = 20_000_000

_SCRIPT_STYLE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.IGNORECASE | re.DOTALL)
_TAG = re.compile(r"<[^>]+>")
_DOCX_BREAKS = re.compile(r"<w:(?:tab|br|cr)\b[^>]*/>")


def _decode(data: bytes) -> str:
    # Notepad can save as UTF-16, which looks like garbage if read as UTF-8
    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return data.decode("utf-16", errors="ignore")
    return data.decode("utf-8-sig", errors="ignore")


def _count_text_file(path: Path, is_html: bool) -> int:
    with open(path, "rb") as f:
        data = f.read(MAX_READ_BYTES)
        more_follows = bool(f.read(1))

    text = _decode(data)
    if is_html:
        text = _SCRIPT_STYLE.sub(" ", text)  # code isn't prose
        text = _TAG.sub(" ", text)
    words = len(text.split())

    # For a huge file we only read the start, so scale up using the real size
    if more_follows and data:
        words = int(words * path.stat().st_size / len(data))
    return words


def _count_docx(path: Path) -> int:
    # A .docx is a zip file; the text is in word/document.xml
    with zipfile.ZipFile(path) as z:
        with z.open("word/document.xml") as part:
            xml = part.read(MAX_DOCX_XML_BYTES).decode("utf-8", errors="ignore")

    # Word often splits one word across several tags, so don't put a space
    # between tags. Only paragraph ends, tabs, and line breaks separate words.
    xml = _DOCX_BREAKS.sub(" ", xml).replace("</w:p>", " ")
    return len(_TAG.sub("", xml).split())


def count_words(path: Path, extension: str) -> int:
    # Rough word count. Returns 0 if the type is unsupported or the file can't be read.
    extension = extension.lower()
    try:
        if extension in TEXT_EXTENSIONS:
            return _count_text_file(path, is_html=False)
        if extension in HTML_EXTENSIONS:
            return _count_text_file(path, is_html=True)
        if extension in DOCX_EXTENSIONS:
            return _count_docx(path)
    except Exception:  # corrupt, locked, no permission, bad zip
        return 0
    return 0
