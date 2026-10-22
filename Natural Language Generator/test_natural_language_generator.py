
import unittest
from types import SimpleNamespace

import dialogue_library as library
import dialogue_situations as situations
import metadata_interpreter as interpreter
import natural_language_generator as nlg


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


if __name__ == "__main__":
    unittest.main()
