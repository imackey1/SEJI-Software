# Run from the project root:
#     python -m unittest discover -v

import tempfile
import unittest
from pathlib import Path

from classes_loot_equipment import (
    SMALL_SCRIPT_SIZE_BYTES,
    FighterClass,
    ItemRole,
    classify_fighters,
    classify_item_role,
)
from scanner import DesktopItem, scan_folder


def make_item(filename, size_bytes=1_000, word_count=0, hidden=False, system=False, folder=False):
    """A DesktopItem built by hand, so tests don't depend on the OS."""
    path = Path("C:/Users/test/Desktop") / filename
    extension = "" if folder else path.suffix.lower()
    return DesktopItem(
        path=path,
        name=filename,
        filename=filename,
        extension=extension,
        is_folder=folder,
        size_bytes=size_bytes,
        created=0.0,
        modified=0.0,
        is_hidden=hidden,
        is_system=system,
        is_online_only=False,
        word_count=word_count,
    )


class TestItemRoles(unittest.TestCase):
    def test_extension_tables(self):
        self.assertEqual(classify_item_role(make_item("settings.ini")), ItemRole.EQUIPMENT)
        self.assertEqual(classify_item_role(make_item("run.bat")), ItemRole.GRENADE)
        self.assertEqual(classify_item_role(make_item("report.bak")), ItemRole.HEAL)
        self.assertEqual(classify_item_role(make_item("debug.log")), ItemRole.JUNK)
        self.assertIsNone(classify_item_role(make_item("essay.docx")))

    def test_backup_name_hint_uses_real_filename(self):
        # Display name has no hint, but the real filename does.
        item = make_item("thesis_backup.docx")
        item.name = "thesis"
        self.assertEqual(classify_item_role(item), ItemRole.HEAL)

    def test_small_script_carve_out(self):
        small = make_item("tool.py", size_bytes=SMALL_SCRIPT_SIZE_BYTES - 1)
        big = make_item("engine.py", size_bytes=SMALL_SCRIPT_SIZE_BYTES)
        self.assertEqual(classify_item_role(small), ItemRole.GRENADE)
        self.assertIsNone(classify_item_role(big))


class TestFighterClasses(unittest.TestCase):
    def test_hidden_or_system_is_always_rogue(self):
        results = classify_fighters([
            make_item("huge.mp4", size_bytes=10**9, hidden=True),
            make_item("core.sys", size_bytes=10**9, system=True),
            make_item("small.png", size_bytes=10),
        ])
        by_name = {r.record.filename: r for r in results.values()}
        self.assertEqual(by_name["huge.mp4"].fighter_class, FighterClass.ROGUE)
        self.assertEqual(by_name["core.sys"].fighter_class, FighterClass.ROGUE)

    def test_size_vs_text_axes(self):
        results = classify_fighters([
            make_item("movie.mp4", size_bytes=900_000_000, word_count=0),
            make_item("novel.docx", size_bytes=40_000, word_count=90_000),
            make_item("tiny.png", size_bytes=10, word_count=0),
        ])
        by_name = {r.record.filename: r.fighter_class for r in results.values()}
        self.assertEqual(by_name["movie.mp4"], FighterClass.BARBARIAN)
        self.assertEqual(by_name["novel.docx"], FighterClass.MAGE)

    def test_items_and_folders_stay_out_of_fighters(self):
        results = classify_fighters([
            make_item("config.json"),
            make_item("Projects", folder=True),
            make_item("photo.jpg", size_bytes=5_000_000),
        ])
        roles = {r.record.filename: r.role for r in results.values()}
        self.assertEqual(roles, {"config.json": "item", "photo.jpg": "fighter"})


class TestWorksWithRealScanner(unittest.TestCase):
    def test_scanner_output_feeds_classifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "notes.txt").write_text("word " * 500)
            (folder / "clip.mp4").write_bytes(b"\0" * 50_000)
            (folder / "setup.cfg").write_text("[x]")
            (folder / "Subfolder").mkdir()

            items = scan_folder(folder, extract_icons=False)
            results = classify_fighters(items)

        by_name = {r.record.filename: r for r in results.values()}
        self.assertEqual(set(by_name), {"notes.txt", "clip.mp4", "setup.cfg"})
        self.assertEqual(by_name["setup.cfg"].item_role, ItemRole.EQUIPMENT)
        self.assertEqual(by_name["notes.txt"].fighter_class, FighterClass.MAGE)
        self.assertEqual(by_name["clip.mp4"].fighter_class, FighterClass.BARBARIAN)


if __name__ == "__main__":
    unittest.main()
