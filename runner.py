import pygame
import time
import sys

from game_of_life import GameOfLife
from templates import template_map

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
LIGHTBLUE = (173, 216, 230)
LIGHTGREEN = (144, 238, 144)
PURPLE = (128, 0, 128)
SPRINGGREEN = (0, 255, 127)
PINK = (255, 192, 203)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
# preset display size
# size = width, height = 800, 600
# fullscreen display
size = screen_size = width, height = pygame.display.get_desktop_sizes()[0]
# print(screen_size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game of Life")

clock = pygame.time.Clock()

# initialize fonts
small_font = pygame.font.SysFont("calibri", 20)
medium_font = pygame.font.SysFont("calibri", 26)
large_font = pygame.font.SysFont("calibri", 36)
title_font = pygame.font.SysFont("calibri", 70)

# cell size and cell counts
cell_size = 15  # modify cell size to zoom in or out
n_cells_width = (width - cell_size * 2) // cell_size
n_cells_height = (height - cell_size * 2) // cell_size
n_cells = n_cells_height * n_cells_width
board_origin = cell_size, cell_size

# screens and states
splash = True
game_completed = False
home = False
main_menu = False
custom = False
custom_instructions = False
template_scr = False

highlight = None
pause = True
grid = False  # whether to display grid lines

# options for main menu
options = ["Random", "Template", "Custom"]

# create cell rectangles
board_rect = pygame.Rect(
    board_origin[0],
    board_origin[1],
    n_cells_width * cell_size,
    n_cells_height * cell_size,
)

cells = []
for i in range(n_cells_height):
    row = []
    for j in range(n_cells_width):
        cell_rect = pygame.Rect(
            board_origin[0] + cell_size * j,
            board_origin[1] + cell_size * i,
            cell_size,
            cell_size,
        )

        row.append(cell_rect)

    cells.append(row)

# game instance
game = None


def make_shadow(text, center, color, shadow_color, font, screen, shadow=True):
    """Render text and make shadow effect for a given text."""

    if shadow:
        shadow_text = font.render(text, True, shadow_color)
        shadow_text_rect = shadow_text.get_rect()
        shadow_text_rect.center = (center[0] + 1, center[1] + 1)
        screen.blit(shadow_text, shadow_text_rect)

    fore_text = font.render(text, True, color)
    fore_text_rect = fore_text.get_rect()
    fore_text_rect.center = center
    screen.blit(fore_text, fore_text_rect)
    return


def set_mode(mode="random", values=None):
    """creates game instance with given game mode.

    Args:
        mode (str, optional): options include 'random', 'template', 'custom', 'custom_values'. Defaults to "random".
        values (int or iterable[tuple(int, int)], optional: values to start game instance.
            int required if mode is template, iterable[tuple(int, int)] is required
            if mode is custom_values. Defaults to None.

    Returns:
        game: GameOfLife instance
    """

    if mode == "random":
        game = GameOfLife(n_cells_width, n_cells_height, 90, PURPLE, RED)
    elif mode == "template":
        game = GameOfLife(
            n_cells_width,
            n_cells_height,
            30,
            PURPLE,
            RED,
            coords=template_map.get(list(template_map.keys())[values], "glider"),
        )
    elif mode == "custom":
        game = GameOfLife(n_cells_width, n_cells_height, 30, PURPLE, RED, custom=True)
    elif mode == "custom_values" and values:
        game = GameOfLife(n_cells_width, n_cells_height, 30, PURPLE, RED, coords=values)
    else:
        game = GameOfLife(n_cells_width, n_cells_height, 30, PURPLE, RED)
    return game


while True:
    # game loop.
    for event in pygame.event.get():
        # Quit event.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # if escape pressed go to home from other
                # screens and quit if current screen is home.
                if home:
                    pygame.quit()
                    sys.exit()
                else:
                    splash = False
                    game_completed = False
                    home = True
                    main_menu = False
                    custom = False
                    custom_instructions = False
                    template_scr = False
                    pause = True
                    break

            if home:
                home = False
                main_menu = True
                highlight = 0
                break

            if main_menu:
                if event.key == pygame.K_1 or (
                    event.key == pygame.K_RETURN and highlight == 0
                ):
                    game = set_mode("random")
                    main_menu = False
                    highlight = None
                    break

                elif event.key == pygame.K_2 or (
                    event.key == pygame.K_RETURN and highlight == 1
                ):
                    # game = set_mode("template")
                    template_scr = True
                    main_menu = False
                    highlight = 0
                    break

                elif event.key == pygame.K_3 or (
                    event.key == pygame.K_RETURN and highlight == 2
                ):
                    game = set_mode("custom")
                    custom_instructions = True
                    main_menu = False
                    highlight = None
                    break

                if event.key == pygame.K_UP:
                    highlight = (highlight - 1) % 3
                elif event.key == pygame.K_DOWN:
                    highlight = (highlight + 1) % 3

            if custom_instructions:
                if event.key == pygame.K_ESCAPE:
                    custom_instructions = False
                    main_menu = True
                    break
                else:
                    custom = True
                    custom_instructions = False
                    break

            if custom:
                if event.key == pygame.K_RETURN:
                    custom = False
                    pause = False
                    # create a new game instance from obtained coordinates.
                    game = set_mode("custom_values", game.get_coords())
                    break

            if event.key == pygame.K_SPACE:
                pause = not pause

            if template_scr:
                if event.key == pygame.K_UP:
                    highlight = (highlight - 1) % len(templates)
                elif event.key == pygame.K_DOWN:
                    highlight = (highlight + 1) % len(templates)

                if event.key == pygame.K_RETURN:
                    game = set_mode("template", highlight)
                    highlight = None
                    template_scr = False

            if game_completed:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if highlight == "Restart":
                        highlight = "Home"
                    else:
                        highlight = "Restart"
                if event.key == pygame.K_RETURN:
                    if highlight == "Restart":
                        game.restart()
                    else:
                        home = True
                    pause = True
                    highlight = None
                    game_completed = False

    screen.fill(BLACK)

    if splash:
        splash = False
        title = title_font.render("Game of Life", True, BLUE)
        title_rect = title.get_rect()
        title_rect.center = (width / 2), (height / 2)
        screen.blit(title, title_rect)
        pygame.display.flip()
        time.sleep(1)
        home = True
        continue

    if game_completed:
        make_shadow(
            "Restart",
            ((width / 2), (height / 2) - 35),
            BLUE,
            SPRINGGREEN,
            large_font,
            screen,
            shadow=highlight == "Restart",
        )

        make_shadow(
            "Home",
            ((width / 2), (height / 2) + 35),
            BLUE,
            SPRINGGREEN,
            large_font,
            screen,
            shadow=highlight == "Home",
        )

        pygame.display.flip()
        continue

    if home:
        welcome = large_font.render("Welcome to Game of Life!", True, BLUE)
        welcome_rect = welcome.get_rect()
        welcome_rect.center = (width / 2), (height / 3)
        screen.blit(welcome, welcome_rect)

        msgs = [
            "Its a finite grid simulation of Conway's Game Of Life.",
            "You can choose random or from preset templates",
            " or make your own configuration.",
            "Press ANY key to continue....",
            "Press SPACE to pause simulation....",
            "Press ESC to exit....",
        ]

        for index, msg in enumerate(msgs):
            welcome_msg = medium_font.render(msg, True, LIGHTBLUE)
            welcome_msg_rect = welcome_msg.get_rect()
            welcome_msg_rect.center = (width / 2), (height / 2) + 45 * index
            screen.blit(welcome_msg, welcome_msg_rect)

        pygame.display.flip()
        continue

    if template_scr:
        template_title = large_font.render("Choose a Template", True, BLUE)
        template_title_rect = template_title.get_rect()
        template_title_rect.center = (width / 2), (height / 6)
        screen.blit(template_title, template_title_rect)

        templates = template_map.keys()

        for index, template in enumerate(templates):
            make_shadow(
                template,
                ((width / 2), (height / 4) + 25 * index),
                LIGHTBLUE,
                SPRINGGREEN,
                small_font,
                screen,
                highlight == index,
            )

        pygame.display.flip()
        continue

    if custom_instructions:
        custom_title = large_font.render("Custom", True, BLUE)
        custom_title_rect = custom_title.get_rect()
        custom_title_rect.center = (width / 2), (height / 3)
        screen.blit(custom_title, custom_title_rect)

        msgs = [
            "Select a cell to toggle its alive state.",
            "Press ENTER once done to start simulation.",
            "Press ANY key to continue....",
            "Press SPACE key to pause simulation....",
            "Press ESC to exit....",
        ]

        for index, msg in enumerate(msgs):
            instruction_msg = medium_font.render(msg, True, LIGHTBLUE)
            instruction_msg_rect = instruction_msg.get_rect()
            instruction_msg_rect.center = (width / 2), (height / 2) + 45 * index
            screen.blit(instruction_msg, instruction_msg_rect)

        pygame.display.flip()
        continue

    if main_menu:
        menu = large_font.render("Choose Game", True, BLUE)
        menu_rect = menu.get_rect()
        menu_rect.center = (width / 2), (height / 3)
        screen.blit(menu, menu_rect)

        for index, option in enumerate(options):
            make_shadow(
                option,
                ((width / 2), (height / 2) + 60 * index),
                LIGHTBLUE,
                BLUE,
                medium_font,
                screen,
                highlight == index,
            )

        pygame.display.flip()
        continue

    # draw borders
    pygame.draw.rect(screen, PURPLE, board_rect, 3)

    # draw cells
    for i, row in enumerate(cells):
        for j, rect in enumerate(row):
            if grid:
                pygame.draw.rect(screen, BLUE, rect, 1)
            if game.get(j, i).alive:
                pygame.draw.rect(screen, game.get(j, i).color, rect)

    if custom:
        # get toggle events for custom mode.
        left, _, _ = pygame.mouse.get_pressed()
        if left:
            mouse = pygame.mouse.get_pos()
            for i, row in enumerate(cells):
                for j, rect in enumerate(row):
                    pygame.draw.rect(screen, BLUE, rect, 1)
                    if rect.collidepoint(mouse):
                        game.toggle_cell(j, i)
                        break
    # fps
    clock.tick(60)
    pygame.display.flip()
    if not custom and not pause:
        # slow down update rate
        time.sleep(0.15)
        # progress game step
        if not game.update():
            # mark completed if no progress step made
            game_completed = True
            highlight = "Restart"
