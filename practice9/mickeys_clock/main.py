import os
import pygame
from clock import MickeyClock

pygame.init()

base_dir = os.path.dirname(os.path.abspath(__file__))
clock_img = os.path.join(base_dir, "images", "mickeyclock.jpeg")

WIDTH = 720
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()
left_arm_img = os.path.join(base_dir, "images", "leftarm.png")
right_arm_img = os.path.join(base_dir, "images", "rightarm.png")

mickey = MickeyClock(
    clock_img,
    left_arm_img,
    right_arm_img
)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  
    mickey.draw(screen)
    pygame.display.flip()
    clock.tick(1)

pygame.quit()