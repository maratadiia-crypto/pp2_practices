import pygame
import sys
import json
import os
from db import create_tables, get_leaderboard
from game import SnakeGame, WIDTH, HEIGHT

pygame.init()

BASE_DIR = os.path.dirname(__file__)
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake")

font = pygame.font.SysFont("arial", 26)
big_font = pygame.font.SysFont("arial", 46)


def load_settings():
    default_settings = {
        "snake_color": [0, 200, 180],
        "grid": True,
        "sound": False
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)
    except:
        settings = default_settings

    for key in default_settings:
        if key not in settings:
            settings[key] = default_settings[key]

    save_settings(settings)
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def draw_button(text, rect):
    pygame.draw.rect(screen, (220, 220, 220), rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    label = font.render(text, True, (0, 0, 0))
    screen.blit(label, label.get_rect(center=rect.center))


def username_screen():
    username = ""

    while True:
        screen.fill((235, 235, 235))

        title = big_font.render("ENTER USERNAME", True, (0, 0, 0))
        screen.blit(title, (210, 160))

        box = pygame.Rect(220, 260, 360, 50)
        pygame.draw.rect(screen, (255, 255, 255), box)
        pygame.draw.rect(screen, (0, 0, 0), box, 2)

        text = font.render(username, True, (0, 0, 0))
        screen.blit(text, (235, 272))

        help_text = font.render("Press Enter to continue", True, (0, 0, 0))
        screen.blit(help_text, (260, 340))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 14:
                        username += event.unicode


def main_menu(username):
    play_btn = pygame.Rect(280, 190, 240, 55)
    leaderboard_btn = pygame.Rect(280, 265, 240, 55)
    settings_btn = pygame.Rect(280, 340, 240, 55)
    quit_btn = pygame.Rect(280, 415, 240, 55)

    while True:
        screen.fill((240, 240, 240))

        title = big_font.render("SNAKE", True, (0, 0, 0))
        screen.blit(title, (315, 90))

        user_text = font.render(f"Player: {username}", True, (0, 0, 0))
        screen.blit(user_text, (300, 145))

        draw_button("Play", play_btn)
        draw_button("Leaderboard", leaderboard_btn)
        draw_button("Settings", settings_btn)
        draw_button("Quit", quit_btn)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if play_btn.collidepoint(pos):
                    return "play"
                if leaderboard_btn.collidepoint(pos):
                    return "leaderboard"
                if settings_btn.collidepoint(pos):
                    return "settings"
                if quit_btn.collidepoint(pos):
                    return "quit"


def leaderboard_screen():
    back_btn = pygame.Rect(280, 590, 240, 50)

    while True:
        screen.fill((235, 235, 235))

        title = big_font.render("LEADERBOARD", True, (0, 0, 0))
        screen.blit(title, (220, 50))

        rows = get_leaderboard()

        y = 130
        if not rows:
            empty = font.render("No scores yet", True, (0, 0, 0))
            screen.blit(empty, (320, y))
        else:
            for i, row in enumerate(rows):
                name = row[0]
                score = row[1]
                level = row[2]
                text = font.render(
                    f"{i + 1}. {name}  Score: {score}  Level: {level}",
                    True,
                    (0, 0, 0)
                )
                screen.blit(text, (160, y))
                y += 40

        draw_button("Back", back_btn)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(pygame.mouse.get_pos()):
                    return "menu"


def settings_screen(settings):
    color_btn = pygame.Rect(250, 190, 300, 50)
    grid_btn = pygame.Rect(250, 265, 300, 50)
    sound_btn = pygame.Rect(250, 340, 300, 50)
    back_btn = pygame.Rect(250, 500, 300, 50)

    colors = [
        [0, 200, 180],
        [255, 0, 0],
        [0, 180, 0],
        [51, 51, 255],
        [160, 0, 200]
    ]

    while True:
        screen.fill((240, 240, 240))

        title = big_font.render("SETTINGS", True, (0, 0, 0))
        screen.blit(title, (270, 80))

        draw_button(f"Snake color: {settings['snake_color']}", color_btn)
        draw_button(f"Grid: {settings['grid']}", grid_btn)
        draw_button(f"Sound: {settings['sound']}", sound_btn)
        draw_button("Back", back_btn)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if color_btn.collidepoint(pos):
                    current = settings["snake_color"]
                    index = colors.index(current) if current in colors else 0
                    settings["snake_color"] = colors[(index + 1) % len(colors)]
                    save_settings(settings)

                elif grid_btn.collidepoint(pos):
                    settings["grid"] = not settings["grid"]
                    save_settings(settings)

                elif sound_btn.collidepoint(pos):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                elif back_btn.collidepoint(pos):
                    return "menu"


create_tables()
settings = load_settings()
username = username_screen()

while True:
    action = main_menu(username)

    if action == "quit":
        break

    elif action == "leaderboard":
        result = leaderboard_screen()
        if result == "quit":
            break

    elif action == "settings":
        result = settings_screen(settings)
        if result == "quit":
            break

    elif action == "play":
        game = SnakeGame(screen, username, settings)
        result = game.run()

        while result == "retry":
            game = SnakeGame(screen, username, settings)
            result = game.run()

        if result == "quit":
            break

pygame.quit()
sys.exit()