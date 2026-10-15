
import pygame

# Colors
BG_COLOR = (20, 24, 35)
PANEL_COLOR = (45, 55, 75)
HOVER_COLOR = (70, 90, 125)
TEXT_COLOR = (255, 255, 255)
SECONDARY_TEXT = (180, 190, 205)
GREEN = (60, 190, 110)
RED = (210, 75, 75)


class BattleScreen:
    def __init__(self, player):
        # Store the selected character's information
        self.player = player.copy()

        # Temporary enemy data
        self.enemy = {
            "name": "enemy_file.exe",
            "class": "Rogue",
            "hp": 80,
            "speed": 40
        }

        # Keep track of maximum and current health
        self.player_max_hp = max(1, self.player["hp"])
        self.enemy_max_hp = self.enemy["hp"]

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

        self.message = "Battle started!"

    def draw_text(self, screen, text, font, color, center):
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
            (225, 230)
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
            (675, 230)
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

        # Battle message
        self.draw_text(
            screen,
            self.message,
            self.text_font,
            TEXT_COLOR,
            (450, 465)
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

    def handle_event(self, event):
        # Return True when the user wants to go back
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return False

            if self.back_button.collidepoint(event.pos):
                return True

            if self.attack_button.collidepoint(event.pos):
                if self.enemy_hp > 0:
                    damage = 15

                    self.enemy_hp = max(
                        0, self.enemy_hp - damage
                    )

                    if self.enemy_hp == 0:
                        self.message = "Enemy defeated!"
                    else:
                        self.message = (
                            f"You dealt {damage} damage!"
                        )

        return False
