import pygame
import sys
from racer import RacerGame
from ui import Button, draw_text
from persistence import load_settings, save_settings, load_leaderboard

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TSIS3 Racer")

font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 42)

settings = load_settings()


def ask_username():
    name = ""
    active = True

    while active:
        screen.fill((230, 230, 230))
        draw_text(screen, "Enter username:", font, (0, 0, 0), 90, 180)
        draw_text(screen, name, big_font, (0, 0, 0), 90, 230)
        draw_text(screen, "Press Enter to start", font, (0, 0, 0), 70, 320)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode


def main_menu():
    buttons = [
        Button("Play", 100, 170, 200, 50),
        Button("Leaderboard", 100, 240, 200, 50),
        Button("Settings", 100, 310, 200, 50),
        Button("Quit", 100, 380, 200, 50)
    ]

    while True:
        screen.fill((220, 220, 220))
        title = big_font.render("RACER", True, (0, 0, 0))
        screen.blit(title, (120, 80))

        for button in buttons:
            button.draw(screen, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons[0].clicked(pos):
                    return "play"
                if buttons[1].clicked(pos):
                    return "leaderboard"
                if buttons[2].clicked(pos):
                    return "settings"
                if buttons[3].clicked(pos):
                    return "quit"


def leaderboard_screen():
    back = Button("Back", 100, 520, 200, 45)

    while True:
        screen.fill((240, 240, 240))
        draw_text(screen, "TOP 10", big_font, (0, 0, 0), 120, 40)

        leaderboard = load_leaderboard()

        y = 120
        for i, item in enumerate(leaderboard):
            text = f"{i + 1}. {item['name']}  {item['score']}  dist:{item['distance']}"
            draw_text(screen, text, font, (0, 0, 0), 30, y)
            y += 35

        back.draw(screen, font)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked(pygame.mouse.get_pos()):
                    return "menu"


def settings_screen():
    global settings

    back = Button("Back", 100, 520, 200, 45)

    while True:
        screen.fill((235, 235, 235))

        draw_text(screen, "SETTINGS", big_font, (0, 0, 0), 80, 50)
        draw_text(screen, f"Sound: {settings['sound']}  press S", font, (0, 0, 0), 60, 160)
        draw_text(screen, f"Car color: {settings['car_color']}  press C", font, (0, 0, 0), 60, 210)
        draw_text(screen, f"Difficulty: {settings['difficulty']}  press D", font, (0, 0, 0), 60, 260)

        back.draw(screen, font)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                if event.key == pygame.K_c:
                    colors = ["blue", "red", "green"]
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]
                    save_settings(settings)

                if event.key == pygame.K_d:
                    levels = ["easy", "normal", "hard"]
                    index = levels.index(settings["difficulty"])
                    settings["difficulty"] = levels[(index + 1) % len(levels)]
                    save_settings(settings)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked(pygame.mouse.get_pos()):
                    return "menu"


while True:
    action = main_menu()

    if action == "quit":
        break

    elif action == "leaderboard":
        result = leaderboard_screen()
        if result == "quit":
            break

    elif action == "settings":
        result = settings_screen()
        if result == "quit":
            break

    elif action == "play":
        username = ask_username()
        game = RacerGame(screen, username, settings)
        result = game.run()

        while result == "retry":
            game = RacerGame(screen, username, settings)
            result = game.run()

        if result == "quit":
            break

pygame.quit()
sys.exit()