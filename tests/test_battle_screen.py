
import unittest
from unittest.mock import patch

from ui.battle_screen import BattleScreen


class TestBattleScreen(unittest.TestCase):

    def setUp(self):
        # Create sample characters for testing
        self.player = {
            "name": "quarterly_report.docx",
            "class": "Mage",
            "hp": 54,
            "atk": 20,
            "speed": 35
        }

        self.enemy = {
            "name": "enemy_file.exe",
            "class": "Rogue",
            "hp": 80,
            "atk": 12,
            "speed": 40
        }

        # Mock Pygame fonts so tests do not open a game window
        with patch("pygame.font.SysFont"):
            self.battle = BattleScreen(self.player, self.enemy)

    def test_attack_damage(self):
        # Verify that attack damage uses the player's ATK stat
        self.battle.attack()

        # Enemy starts with 80 HP and player has 20 ATK
        self.assertEqual(self.battle.enemy_hp, 60)

    def test_enemy_defeat(self):
        # Set enemy HP low enough to be defeated in one attack
        self.battle.enemy_hp = 10

        # Attack the enemy
        self.battle.attack()

        # Verify enemy HP does not go below zero
        self.assertEqual(self.battle.enemy_hp, 0)

        # Verify the victory message appears
        self.assertIn("Enemy defeated!", self.battle.message)


if __name__ == "__main__":
    unittest.main()
