# python -m pytest tests -v

import sys
from pathlib import Path

# let the tests find the scanner folder
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scanner.windows_scanner import scan_folder


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
