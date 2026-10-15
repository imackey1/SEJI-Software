
import pygame
from battle_screen import BattleScreen

pygame.init()

# Window settings
WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desktop Warfare")

# Colors
BG_COLOR = (20, 24, 35)
BUTTON_COLOR = (45, 55, 75)
HOVER_COLOR = (70, 90, 125)
SELECTED_COLOR = (60, 100, 150)
TEXT_COLOR = (255, 255, 255)
SECONDARY_TEXT = (180, 190, 205)

# Fonts
title_font = pygame.font.SysFont("arial", 54, bold=True)
heading_font = pygame.font.SysFont("arial", 32, bold=True)
button_font = pygame.font.SysFont("arial", 25)
small_font = pygame.font.SysFont("arial", 20)
file_font = pygame.font.SysFont("arial", 15)

# Temporary character data
characters = [
    {
        "name": "quarterly_report.docx",
        "class": "Scholar",
        "hp": 54,
        "speed": 35,
        "description": "A careful and strategic fighter."
    },
    {
        "name": "vacation_clip.mp4",
        "class": "Brute",
        "hp": 85,
        "speed": 20,
        "description": "A powerful fighter with high health."
    },
    {
        "name": "sketchy_installer.exe",
        "class": "Rogue",
        "hp": 61,
        "speed": 70,
        "description": "A fast and unpredictable fighter."
    }
]

# Screen navigation
current_screen = "menu"
selected_character = 0
battle = None

# Main menu buttons
start_button = pygame.Rect(300, 280, 300, 65)
settings_button = pygame.Rect(300, 370, 300, 65)
exit_button = pygame.Rect(300, 460, 300, 65)

# Character selection buttons
character_buttons = [
    pygame.Rect(70, 200, 240, 110),
    pygame.Rect(330, 200, 240, 110),
    pygame.Rect(590, 200, 240, 110)
]

back_button = pygame.Rect(70, 600, 180, 55)
confirm_button = pygame.Rect(650, 600, 180, 55)

clock = pygame.time.Clock()
running = True


def draw_centered_text(text, font, color, center):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    screen.blit(rendered, rect)


def draw_button(rect, label, mouse_pos, selected=False):
    if selected:
        color = SELECTED_COLOR
    elif rect.collidepoint(mouse_pos):
        color = HOVER_COLOR
    else:
        color = BUTTON_COLOR

    pygame.draw.rect(
        screen, color, rect, border_radius=10
    )

    draw_centered_text(
        label, button_font, TEXT_COLOR, rect.center
    )


def draw_main_menu(mouse_pos):
    draw_centered_text(
        "DESKTOP WARFARE",
        title_font,
        TEXT_COLOR,
        (WIDTH // 2, 150)
    )

    draw_button(start_button, "START GAME", mouse_pos)
    draw_button(settings_button, "SETTINGS", mouse_pos)
    draw_button(exit_button, "EXIT", mouse_pos)


def draw_character_selection(mouse_pos):
    draw_centered_text(
        "CHOOSE YOUR FILE",
        heading_font,
        TEXT_COLOR,
        (WIDTH // 2, 90)
    )

    # Character cards
    for i, character in enumerate(characters):
        rect = character_buttons[i]
        selected = (i == selected_character)

        color = SELECTED_COLOR if selected else BUTTON_COLOR

        if rect.collidepoint(mouse_pos) and not selected:
            color = HOVER_COLOR

        pygame.draw.rect(
            screen, color, rect, border_radius=10
        )

        draw_centered_text(
            character["class"],
            button_font,
            TEXT_COLOR,
            (rect.centerx, rect.y + 35)
        )

        draw_centered_text(
            character["name"],
            file_font,
            SECONDARY_TEXT,
            (rect.centerx, rect.y + 75)
        )

    # Selected character details
    character = characters[selected_character]

    pygame.draw.rect(
        screen,
        BUTTON_COLOR,
        pygame.Rect(180, 365, 540, 190),
        border_radius=12
    )

    draw_centered_text(
        character["name"],
        button_font,
        TEXT_COLOR,
        (WIDTH // 2, 405)
    )

    draw_centered_text(
        "Class: " + character["class"],
        small_font,
        SECONDARY_TEXT,
        (WIDTH // 2, 445)
    )

    draw_centered_text(
        "HP: " + str(character["hp"]) +
        "       Speed: " + str(character["speed"]),
        small_font,
        TEXT_COLOR,
        (WIDTH // 2, 480)
    )

    draw_centered_text(
        character["description"],
        small_font,
        SECONDARY_TEXT,
        (WIDTH // 2, 520)
    )

    draw_button(back_button, "BACK", mouse_pos)
    draw_button(confirm_button, "CONFIRM", mouse_pos)


# Main game loop
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif current_screen == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if start_button.collidepoint(event.pos):
                        current_screen = "character_select"

                    elif settings_button.collidepoint(event.pos):
                        print("Settings clicked!")

                    elif exit_button.collidepoint(event.pos):
                        running = False

        elif current_screen == "character_select":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    for i, rect in enumerate(character_buttons):
                        if rect.collidepoint(event.pos):
                            selected_character = i

                    if back_button.collidepoint(event.pos):
                        current_screen = "menu"

                    elif confirm_button.collidepoint(event.pos):
                        # Create battle using selected character
                        battle = BattleScreen(
                            characters[selected_character]
                        )

                        current_screen = "battle"

        elif current_screen == "battle":
            # Pass mouse events to battle screen
            if battle.handle_event(event):
                current_screen = "character_select"

    # Draw current screen
    screen.fill(BG_COLOR)

    if current_screen == "menu":
        draw_main_menu(mouse_pos)

    elif current_screen == "character_select":
        draw_character_selection(mouse_pos)

    elif current_screen == "battle":
        battle.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
