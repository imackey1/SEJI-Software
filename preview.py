# Quick window that shows what the scanner found -- just to check it
# works before it's wired into the real game. Not part of the game
# itself.
import pygame
from scanner.windows_scanner import scan_apps, icon_to_pygame_surface

# --- window settings ---
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
BG_COLOR = (20, 20, 30)      # dark background
ICON_SIZE = (48, 48)         # how big each icon shows up
TILE_SIZE = 80               # space reserved for each icon + its name
PADDING = 20                 # gap between tiles
COLS = 9                     # icons per row before wrapping

# --- open the window ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Scanner Preview")
font = pygame.font.SysFont(None, 14)
clock = pygame.time.Clock()

# --- run the scanner once, up front ---
apps = scan_apps()
print(f"Found {len(apps)} apps")

# work out where each icon+label goes on screen, once, so we don't
# recalculate it 60 times a second in the loop below
tiles = []
for i, app in enumerate(apps):
    surface = None
    if app["icon_path"]:
        try:
            surface = icon_to_pygame_surface(app["icon_path"], ICON_SIZE)
        except Exception as e:
            print(f"Couldn't load icon for {app['name']}: {e}")
    col = i % COLS
    row = i // COLS
    x = PADDING + col * (TILE_SIZE + PADDING)
    y = PADDING + row * (TILE_SIZE + PADDING)
    tiles.append((app["name"], surface, x, y))

# --- the actual game loop: keeps the window open and redraws it ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:      # user clicked the X button
            running = False

    screen.fill(BG_COLOR)
    for name, surface, x, y in tiles:
        if surface:
            screen.blit(surface, (x + 16, y))
        label = font.render(name[:10], True, (230, 230, 230))
        screen.blit(label, (x, y + ICON_SIZE[1] + 10))
    pygame.display.flip()   # actually show the frame we just drew
    clock.tick(60)          # cap it at 60 frames per second

pygame.quit()
