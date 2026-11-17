# python -m pytest Test -v

import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

# let the tests find the scanner folder
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scanner.windows_scanner import _read_item, scan_folder

RECALL_ON_OPEN = 0x00040000  # one of the OneDrive "online-only" flags


class _FakeEntry:
    """Stands in for an os.DirEntry carrying Windows attributes we cannot set here."""

    def __init__(self, path: Path, attrs: int = 0):
        self.path = str(path)
        self.name = path.name
        self._attrs = attrs

    def stat(self):
        real = os.stat(self.path)
        return SimpleNamespace(
            st_size=real.st_size,
            st_mtime=real.st_mtime,
            st_ctime=real.st_ctime,
            st_file_attributes=self._attrs,
        )

    def is_dir(self):
        return False


def test_scanner_reads_file_info_and_never_changes_the_file(tmp_path):
    file = tmp_path / "notes.txt"
    file.write_text("hello there friend")
    (tmp_path / "desktop.ini").write_text("Windows clutter")

    items = scan_folder(tmp_path, extract_icons=False)

    assert len(items) == 1  # desktop.ini was skipped
    item = items[0]
    assert item.name == "notes.txt"
    assert item.size_bytes == len("hello there friend")
    assert item.word_count == 3
    assert file.read_text() == "hello there friend"  # the file was not changed


def test_hidden_dot_file_is_flagged_and_never_read(tmp_path):
    if sys.platform == "win32":
        pytest.skip("dot-prefix is only the hidden check off Windows")
    hidden = tmp_path / ".secret.txt"
    hidden.write_text("this should never be counted")

    items = scan_folder(tmp_path, extract_icons=False)

    assert len(items) == 1
    assert items[0].is_hidden is True
    assert items[0].is_obscured is True
    assert items[0].word_count == 0


def test_shortcuts_and_exes_show_without_their_extension(tmp_path):
    (tmp_path / "Chrome.lnk").write_bytes(b"")
    (tmp_path / "Game.exe").write_bytes(b"")

    names = {item.name for item in scan_folder(tmp_path, extract_icons=False)}

    assert names == {"Chrome", "Game"}


def test_folders_are_listed_with_no_extension_and_zero_size(tmp_path):
    (tmp_path / "stuff").mkdir()

    items = scan_folder(tmp_path, extract_icons=False)

    assert len(items) == 1
    assert items[0].is_folder is True
    assert items[0].extension == ""
    assert items[0].size_bytes == 0


def test_online_only_file_is_flagged_and_never_opened(tmp_path):
    path = tmp_path / "cloud.txt"
    path.write_text("reading this would have downloaded it")

    item = _read_item(_FakeEntry(path, attrs=RECALL_ON_OPEN), extract_icons=False)

    assert item is not None
    assert item.is_online_only is True
    assert item.word_count == 0


def test_to_dict_is_safe_to_turn_into_json(tmp_path):
    (tmp_path / "notes.txt").write_text("one two")
    (tmp_path / "stuff").mkdir()

    items = scan_folder(tmp_path, extract_icons=False)
    assert len(items) == 2  # a file and a folder both have to survive json

    for item in items:
        data = item.to_dict()
        assert isinstance(data["path"], str)
        assert data["icon_path"] is None
        json.dumps(data)  # the whole point: this must not raise