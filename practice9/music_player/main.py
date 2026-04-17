import os
import pygame
from player import MusicPlayer
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)
clock = pygame.time.Clock()
base_dir = os.path.dirname(os.path.abspath(__file__))
music_folder = os.path.join(base_dir, "music", "sample_tracks")
player = MusicPlayer(music_folder)
running = True
while running:
    screen.fill((240, 240, 240))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_q:
                running = False
    title_text = font.render("Music Player", True, (0, 0, 0))
    track_text = small_font.render(
        f"Current track: {player.get_current_track_name()}",
        True,
        (0, 0, 0)
    )
    pos_text = small_font.render(
        f"Position: {player.get_position_seconds()} sec",
        True,
        (0, 0, 0)
    )
    controls_text = small_font.render(
        "P = Play   S = Stop   N = Next   B = Back   Q = Quit",
        True,
        (0, 0, 0)
    )
    screen.blit(title_text, (300, 50))
    screen.blit(track_text, (160, 150))
    screen.blit(pos_text, (160, 200))
    screen.blit(controls_text, (80, 280))
    pygame.display.flip()
    clock.tick(10)
pygame.quit()