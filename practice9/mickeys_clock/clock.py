import pygame
from datetime import datetime

class MickeyClock:
    def __init__(self, clock_img, left_arm_img, right_arm_img):
        full_clock = pygame.image.load(clock_img).convert()
        self.clock = pygame.Surface((720, 720)).convert()
        self.clock.blit(full_clock, (0, 0), (0, 280, 720, 720))
        self.left_arm = pygame.image.load(left_arm_img).convert_alpha()
        self.right_arm = pygame.image.load(right_arm_img).convert_alpha()
        self.left_arm.set_colorkey((255, 255, 255))
        self.right_arm.set_colorkey((255, 255, 255))
        self.left_arm = pygame.transform.scale(self.left_arm, (200, 260))
        self.right_arm = pygame.transform.scale(self.right_arm, (230, 300))
        self.center = (360, 430)
        self.left_pivot = (180, 200)
        self.right_pivot = (150, 250)
    def blit_rotate(self, screen, image, pivot, angle, pos):
        rect = image.get_rect(
            topleft=(pos[0] - pivot[0], pos[1] - pivot[1])
        )
        offset = pygame.math.Vector2(pos) - rect.center
        rotated_offset = offset.rotate(-angle)
        rotated_center = (
            pos[0] - rotated_offset.x,
            pos[1] - rotated_offset.y
        )
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(
            center=rotated_center
        )

        screen.blit(rotated_image, rotated_rect)
    def draw(self, screen):
        screen.blit(self.clock, (0, 0))
        now = datetime.now()
        seconds = now.second
        minutes = now.minute
        second_angle = -(seconds * 6)
        minute_angle = -(minutes * 6)
        self.blit_rotate(
            screen,
            self.left_arm,
            self.left_pivot,
            second_angle,
            self.center
        )
        self.blit_rotate(
            screen,
            self.right_arm,
            self.right_pivot,
            minute_angle,
            self.center
        )