import sys
import zipfile
from pathlib import Path

# let the tests find the scanner folder
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scanner.word_count import count_words


def _write_docx(path: Path, paragraphs: list[str]) -> None:
    # is enough to check the counting without needing Word or python-docx.
    body = "".join(f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>" for text in paragraphs)
    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", xml)


def test_counts_words_in_a_text_file(tmp_path):
    file = tmp_path / "notes.txt"
    file.write_text("one two three four")

    assert count_words(file, ".txt") == 4


def test_counts_visible_words_in_html_and_ignores_code(tmp_path):
    page = tmp_path / "page.html"
    page.write_text(
        "<html><head>"
        "<style>.a { color: red; }</style>"
        "<script>var ignored = 1;</script>"
        "</head><body><h1>hello there</h1></body></html>"
    )

    # only "hello there" counts, the script and style are not prose
    assert count_words(page, ".html") == 2


def test_counts_words_in_a_word_document(tmp_path):
    docx = tmp_path / "report.docx"
    _write_docx(docx, ["one two", "three four"])

    assert count_words(docx, ".docx") == 4


def test_bad_files_return_zero_instead_of_crashing(tmp_path):
    # a file that doesn't exist
    assert count_words(tmp_path / "missing.txt", ".txt") == 0

    # a "Word file" that is really just junk
    broken = tmp_path / "broken.docx"
    broken.write_bytes(b"this is not a real docx")
    assert count_words(broken, ".docx") == 0

    # a type we do not support at all
    assert count_words(tmp_path / "missing.zip", ".zip") == 0