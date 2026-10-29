import sys
from pathlib import Path

# let the tests find the scanner folder
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scanner.word_count import count_words


def test_counts_words_in_a_text_file(tmp_path):
    file = tmp_path / "notes.txt"
    file.write_text("one two three four")

    assert count_words(file, ".txt") == 4


def test_bad_files_return_zero_instead_of_crashing(tmp_path):
    # a file that doesn't exist
    assert count_words(tmp_path / "missing.txt", ".txt") == 0

    # a "Word file" that is really just junk
    broken = tmp_path / "broken.docx"
    broken.write_bytes(b"this is not a real docx")
    assert count_words(broken, ".docx") == 0
  
  # pip install pytest, python -m pytest tests -v
