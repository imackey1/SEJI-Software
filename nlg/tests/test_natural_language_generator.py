# Run from the project root:
#     python -m unittest discover -v

import time
import unittest
from types import SimpleNamespace

from nlg import dialogue_library as library
from nlg import dialogue_situations as situations
from nlg import metadata_interpreter as interpreter
from nlg import natural_language_generator as nlg


class TestMetadataInterpreter(unittest.TestCase):

    def test_dictionary_metadata(self):
        metadata = {
            "file_type": ".exe",
            "file_size": 150_000_000,
            "created": "2020-01-01",
            "modified": "2026-01-01",
        }

        traits = interpreter.interpret_metadata(metadata)

        self.assertIn("large", traits)
        self.assertIn("application", traits)
        self.assertIn("old", traits)

    def test_file_record_metadata(self):
        metadata = SimpleNamespace(
            name="Hidden_Backup.txt",
            extension=".txt",
            size_bytes=500_000,
            is_hidden=True,
            is_system=False,
            word_count=2500,
        )

        traits = interpreter.interpret_metadata(metadata)

        expected_traits = {
            "small",
            "document",
            "text_heavy",
            "hidden",
            "backup",
        }

        self.assertTrue(expected_traits.issubset(set(traits)))

    def test_system_file_trait(self):
        metadata = SimpleNamespace(
            name="system.exe",
            extension=".exe",
            size_bytes=500_000,
            is_hidden=False,
            is_system=True,
            word_count=0,
        )

        traits = interpreter.interpret_metadata(metadata)

        self.assertIn("system", traits)
        self.assertIn("executable", traits)


class TestDialogueGeneration(unittest.TestCase):

    def test_intro_generates_text(self):
        metadata = SimpleNamespace(
            name="enemy.txt",
            extension=".txt",
            size_bytes=500_000,
            is_hidden=False,
            is_system=False,
            word_count=1500,
        )

        dialogue = nlg.generate_dialogue(
            metadata,
            situations.INTRO,
        )

        self.assertIsInstance(dialogue, str)
        self.assertTrue(dialogue.strip())

    def test_enemy_dialogue_generates_text(self):
        metadata = SimpleNamespace(
            name="enemy.exe",
            extension=".exe",
            size_bytes=500_000,
            is_hidden=False,
            is_system=False,
            word_count=0,
        )

        dialogue = nlg.generate_enemy_dialogue(metadata)

        self.assertIsInstance(dialogue, str)
        self.assertTrue(dialogue.strip())

    def test_combat_situations_generate_text(self):
        combat_situations = [
            situations.ATTACK,
            situations.DAMAGE,
            situations.LOW_HEALTH,
            situations.DODGE,
            situations.VICTORY,
            situations.DEFEAT,
        ]

        for situation in combat_situations:
            with self.subTest(situation=situation):
                dialogue = nlg.generate_dialogue(
                    {},
                    situation,
                    character_class="Mage",
                )

                self.assertIsInstance(dialogue, str)
                self.assertTrue(dialogue.strip())
 
class TestMetadataEdgeCases(unittest.TestCase):

    def test_missing_metadata(self):
        self.assertEqual(interpreter.interpret_metadata(None), [])

    def test_empty_dictionary(self):
        traits = interpreter.interpret_metadata({})
        self.assertIn("small", traits)

    def test_unknown_extension(self):
        metadata = {
            "name": "mystery.xyz",
            "extension": ".xyz",
            "size_bytes": 500,
        }

        traits = interpreter.interpret_metadata(metadata)

        self.assertIn("small", traits)
        self.assertNotIn("document", traits)
        self.assertNotIn("application", traits)

    def test_invalid_size_and_word_count(self):
        metadata = {
            "name": "test.txt",
            "extension": ".txt",
            "size_bytes": "invalid",
            "word_count": None,
        }

        traits = interpreter.interpret_metadata(metadata)

        self.assertIn("small", traits)
        self.assertIn("document", traits)
        self.assertNotIn("text_heavy", traits)

    def test_invalid_dates_are_ignored(self):
        metadata = {
            "name": "test.txt",
            "extension": ".txt",
            "size_bytes": 500,
            "created": "not-a-date",
            "modified": "invalid",
        }

        traits = interpreter.interpret_metadata(metadata)

        self.assertNotIn("new", traits)
        self.assertNotIn("old", traits)
        self.assertNotIn("recently_modified", traits)
        self.assertNotIn("stale", traits)



class TestWorksWithScannerAndClassifier(unittest.TestCase):
    """The shapes the rest of the project actually hands to the NLG."""

    def test_scanner_timestamps_produce_age_traits(self):
        # scanner.DesktopItem gives created/modified as seconds since 1970
        now = time.time()
        metadata = SimpleNamespace(
            name="Chrome",
            filename="Chrome_backup.lnk",
            extension=".lnk",
            size_bytes=2_000,
            is_hidden=False,
            is_system=False,
            word_count=0,
            created=now - 3 * 365 * 24 * 3600,
            modified=now - 2 * 24 * 3600,
        )

        traits = interpreter.interpret_metadata(metadata)

        self.assertIn("old", traits)
        self.assertIn("recently_modified", traits)
        self.assertIn("backup", traits)  # read from the real filename, not the display name

    def test_fighter_class_enum_gets_class_specific_lines(self):
        class FakeFighterClass:  # stands in for classes_loot_equipment.FighterClass.MAGE
            value = "Mage"

        for _ in range(20):
            line = nlg.generate_dialogue({}, situations.ATTACK, character_class=FakeFighterClass())
            self.assertIn(line, library.CLASS_ATTACKS["Mage"])


if __name__ == "__main__":
    unittest.main()
