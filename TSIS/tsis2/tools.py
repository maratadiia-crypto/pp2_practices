import pygame
from collections import deque


def flood_fill(surface, x, y, new_color):  
    width, height = surface.get_size()
    old_color = surface.get_at((x, y))[:3]

    if old_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 220 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py))[:3] != old_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def draw_equilateral_triangle(surface, color, pos, width):  
    x, y = pos
    points = [
        (x, y),
        (x - 60, y + 100),
        (x + 60, y + 100)
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_right_triangle(surface, color, pos, width):  
    x, y = pos
    points = [
        (x, y),
        (x, y + 120),
        (x + 120, y + 120)
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, pos, width):  
    x, y = pos
    points = [
        (x, y - 70),
        (x + 90, y),
        (x, y + 70),
        (x - 90, y)
    ]
    pygame.draw.polygon(surface, color, points, width)