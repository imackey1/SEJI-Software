
import pygame

# Colors
BG_COLOR = (20, 24, 35)
PANEL_COLOR = (45, 55, 75)
HOVER_COLOR = (70, 90, 125)
TEXT_COLOR = (255, 255, 255)
SECONDARY_TEXT = (180, 190, 205)
GREEN = (60, 190, 110)
RED = (210, 75, 75)

# Dialogue situations. These match nlg.situations; they're spelled out
# here so the UI doesn't need the NLG installed to run on its own.
ENEMY_INTRO = "enemy_intro"
ATTACK = "attack"
DAMAGE = "damage"
LOW_HEALTH = "low_health"
VICTORY = "victory"

# Below this share of max HP, the enemy uses its low-health lines.
LOW_HEALTH_FRACTION = 0.3

# Used when nobody passes in an enemy (UI-only runs).
DEFAULT_ENEMY = {
    "name": "enemy_file.exe",
    "class": "Rogue",
    "hp": 80,
    "atk": 12,
    "speed": 40
}

DEFAULT_DAMAGE = 15
MESSAGE_WIDTH = 760
MAX_MESSAGE_LINES = 3


def fit_text(text, font, max_width):
    """Shorten text with '...' until it fits in max_width pixels."""
    if font.size(text)[0] <= max_width:
        return text
    while text and font.size(text + "...")[0] > max_width:
        text = text[:-1]
    return text + "..."


def wrap_text(text, font, max_width):
    """Split text into lines that each fit in max_width pixels."""
    lines = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = fit_text(word, font, max_width)
    if current:
        lines.append(current)
    return lines


class BattleScreen:
    def __init__(self, player, enemy=None, dialogue=None):
        # Store the selected character's information
        self.player = player.copy()

        # The opponent; falls back to a stand-in when none is given
        self.enemy = (enemy or DEFAULT_ENEMY).copy()

        # dialogue(situation, fighter_dict) -> str, or None for no dialogue
        self.dialogue = dialogue

        # Keep track of maximum and current health
        self.player_max_hp = max(1, self.player["hp"])
        self.enemy_max_hp = max(1, self.enemy["hp"])

        self.player_hp = self.player_max_hp
        self.enemy_hp = self.enemy_max_hp

        # Fonts
        self.title_font = pygame.font.SysFont(
            "arial", 36, bold=True
        )
        self.text_font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 18)

        # Buttons
        self.attack_button = pygame.Rect(340, 550, 220, 60)
        self.back_button = pygame.Rect(40, 625, 150, 45)

        taunt = self.say(ENEMY_INTRO, self.enemy)
        if taunt:
            self.message = f'{self.enemy["name"]}: "{taunt}"'
        else:
            self.message = "Battle started!"

    def say(self, situation, fighter):
        """One line of dialogue for this fighter, or "" if there's no dialogue source."""
        if self.dialogue is None:
            return ""
        try:
            return self.dialogue(situation, fighter) or ""
        except Exception as error:  # a dialogue bug shouldn't crash the battle
            print(f"Dialogue error ({situation}): {error}")
            return ""

    def draw_text(self, screen, text, font, color, center, max_width=None):
        if max_width is not None:
            text = fit_text(text, font, max_width)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)

    def draw_hp_bar(self, screen, x, y, current_hp, max_hp):
        # Draw the empty health bar
        pygame.draw.rect(
            screen,
            PANEL_COLOR,
            (x, y, 250, 25),
            border_radius=6
        )

        # Calculate remaining health percentage
        health_percentage = max(
            0, min(1, current_hp / max_hp)
        )

        # Draw remaining health
        if health_percentage > 0:
            pygame.draw.rect(
                screen,
                GREEN,
                (x, y, int(250 * health_percentage), 25),
                border_radius=6
            )

        # Display HP numbers
        self.draw_text(
            screen,
            f"{current_hp}/{max_hp} HP",
            self.small_font,
            TEXT_COLOR,
            (x + 125, y + 12)
        )

    def draw_button(self, screen, rect, label, mouse_pos):
        color = (
            HOVER_COLOR
            if rect.collidepoint(mouse_pos)
            else PANEL_COLOR
        )

        pygame.draw.rect(
            screen, color, rect, border_radius=10
        )

        self.draw_text(
            screen,
            label,
            self.text_font,
            TEXT_COLOR,
            rect.center
        )

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BG_COLOR)

        # Battle title
        self.draw_text(
            screen,
            "DESKTOP WARFARE - BATTLE",
            self.title_font,
            TEXT_COLOR,
            (450, 85)
        )

        # Player information
        self.draw_text(
            screen,
            self.player["name"],
            self.text_font,
            TEXT_COLOR,
            (225, 230),
            max_width=300
        )

        self.draw_text(
            screen,
            self.player["class"],
            self.small_font,
            SECONDARY_TEXT,
            (225, 270)
        )

        # Enemy information
        self.draw_text(
            screen,
            self.enemy["name"],
            self.text_font,
            TEXT_COLOR,
            (675, 230),
            max_width=300
        )

        self.draw_text(
            screen,
            self.enemy["class"],
            self.small_font,
            SECONDARY_TEXT,
            (675, 270)
        )

        # Health bars
        self.draw_hp_bar(
            screen, 100, 315,
            self.player_hp, self.player_max_hp
        )

        self.draw_hp_bar(
            screen, 550, 315,
            self.enemy_hp, self.enemy_max_hp
        )

        # VS label
        self.draw_text(
            screen,
            "VS",
            self.title_font,
            RED,
            (450, 330)
        )

        # Battle message (wrapped, since dialogue lines can be long)
        lines = wrap_text(self.message, self.text_font, MESSAGE_WIDTH)
        lines = lines[:MAX_MESSAGE_LINES]
        line_height = 30
        first_y = 465 - (len(lines) - 1) * line_height // 2
        for i, line in enumerate(lines):
            self.draw_text(
                screen,
                line,
                self.text_font,
                TEXT_COLOR,
                (450, first_y + i * line_height)
            )

        # Buttons
        self.draw_button(
            screen,
            self.attack_button,
            "ATTACK",
            mouse_pos
        )

        self.draw_button(
            screen,
            self.back_button,
            "BACK",
            mouse_pos
        )

    def attack(self):
        """Player attacks once. Updates enemy HP and the battle message."""
        if self.enemy_hp <= 0:
            return

        damage = self.player.get("atk", DEFAULT_DAMAGE)

        self.enemy_hp = max(
            0, self.enemy_hp - damage
        )

        shout = self.say(ATTACK, self.player)
        parts = [f'"{shout}"'] if shout else []

        if self.enemy_hp == 0:
            parts.append("Enemy defeated!")
            victory = self.say(VICTORY, self.player)
            if victory:
                parts.append(victory)
        else:
            parts.append(f"You dealt {damage} damage!")
            low = self.enemy_hp <= self.enemy_max_hp * LOW_HEALTH_FRACTION
            reply = self.say(LOW_HEALTH if low else DAMAGE, self.enemy)
            if reply:
                parts.append(f'{self.enemy["name"]}: "{reply}"')

        self.message = " ".join(parts)

    def handle_event(self, event):
        # Return True when the user wants to go back
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return False

            if self.back_button.collidepoint(event.pos):
                return True

            if self.attack_button.collidepoint(event.pos):
                self.attack()

        return False
