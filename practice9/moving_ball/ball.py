import pygame
class Ball:
    def __init__(self, x, y, radius=25, step=20, width=800, height=600):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step
        self.width = width
        self.height = height
        self.color = (255, 0, 0)
    def move_up(self):
        if self.y - self.step - self.radius >= 0:
            self.y -= self.step
    def move_down(self):
        if self.y + self.step + self.radius <= self.height:
            self.y += self.step
    def move_left(self):
        if self.x - self.step - self.radius >= 0:
            self.x -= self.step
    def move_right(self):
        if self.x + self.step + self.radius <= self.width:
            self.x += self.step
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)