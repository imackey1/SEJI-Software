# End-to-end check that every module connects:
# scanner -> classes_loot_equipment -> stats -> nlg -> the dicts the UI draws.
#
# Run from the project root:
#     python -m unittest discover -v

import random
import tempfile
import unittest
from pathlib import Path

import nlg
from game import base_stats, build_roster, choose_lineup, make_dialogue_provider, pick_enemy
from game.stats import BASE_STATS, STAT_VARIATION
from classes_loot_equipment import FighterClass
from scanner import scan_folder

UI_KEYS = {"name", "class", "hp", "atk", "speed", "description", "metadata"}
VALID_CLASSES = {"Barbarian", "Mage", "Rogue"}


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        folder = Path(self._tmp.name)
        (folder / "novel.txt").write_text("word " * 4000)
        (folder / "short_note.txt").write_text("hi")
        (folder / "movie.mp4").write_bytes(b"\0" * 300_000)
        (folder / "logo.ico").write_bytes(b"\0" * 100)
        (folder / "settings.ini").write_text("[a]")
        (folder / "cleanup.bat").write_text("echo hi")
        (folder / "Old Stuff").mkdir()
        self.items = scan_folder(folder, extract_icons=False)
        self.roster = build_roster(self.items)

    def tearDown(self):
        self._tmp.cleanup()

    def test_fighters_and_items_are_split(self):
        fighter_names = {f.item.filename for f in self.roster.fighters}
        item_names = {r.record.filename for r in self.roster.items}
        self.assertEqual(fighter_names, {"novel.txt", "short_note.txt", "movie.mp4", "logo.ico"})
        self.assertEqual(item_names, {"settings.ini", "cleanup.bat"})

    def test_ui_dicts_have_everything_the_ui_reads(self):
        for fighter in self.roster.fighters:
            data = fighter.to_ui_dict()
            self.assertEqual(set(data), UI_KEYS)
            self.assertIn(data["class"], VALID_CLASSES)
            self.assertGreater(data["hp"], 0)

    def test_lineup_offers_one_of_each_class_when_possible(self):
        lineup = choose_lineup(self.roster.fighters)
        self.assertEqual(len(lineup), 3)
        self.assertEqual({f.fighter_class for f in lineup}, set(FighterClass))

    def test_enemy_is_never_the_players_own_file(self):
        player = self.roster.fighters[0].to_ui_dict()
        rng = random.Random(1)
        for _ in range(50):
            enemy = pick_enemy(self.roster.fighters, player, rng)
            self.assertNotEqual(enemy["metadata"].path, player["metadata"].path)

    def test_dialogue_provider_answers_every_battle_situation(self):
        provide = make_dialogue_provider()
        fighter = self.roster.fighters[0].to_ui_dict()
        for situation in (nlg.situations.ENEMY_INTRO, nlg.situations.INTRO, nlg.situations.ATTACK,
                          nlg.situations.DAMAGE, nlg.situations.LOW_HEALTH, nlg.situations.DODGE,
                          nlg.situations.VICTORY, nlg.situations.DEFEAT):
            with self.subTest(situation=situation):
                line = provide(situation, fighter)
                self.assertIsInstance(line, str)
                self.assertTrue(line.strip())

    def test_dialogue_provider_handles_demo_dicts_without_metadata(self):
        provide = make_dialogue_provider()
        line = provide(nlg.situations.ENEMY_INTRO, {"name": "enemy_file.exe", "class": "Rogue"})
        self.assertTrue(line.strip())


class TestStats(unittest.TestCase):
    def test_same_file_always_gets_same_stats(self):
        self.assertEqual(base_stats(FighterClass.MAGE, "a.txt"), base_stats(FighterClass.MAGE, "a.txt"))

    def test_variation_stays_in_range(self):
        for i in range(200):
            stats = base_stats(FighterClass.BARBARIAN, f"file{i}.mp4")
            hp, atk, speed = BASE_STATS[FighterClass.BARBARIAN]
            self.assertLessEqual(abs(stats.hp - hp), hp * STAT_VARIATION + 1)
            self.assertLessEqual(abs(stats.speed - speed), speed * STAT_VARIATION + 1)


if __name__ == "__main__":
    unittest.main()
