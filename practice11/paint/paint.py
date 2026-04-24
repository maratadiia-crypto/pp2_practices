import pygame
import math

pygame.init()

# screen settings
screen = pygame.display.set_mode((900, 700))
screen.fill((255, 255, 255))
pygame.display.set_caption('GFG Paint')

draw_on = False  # drawing state
last_pos = (0, 0)  # last mouse position
radius = 5  # brush size
color = (0, 0, 0)  # default color

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (102, 204, 0)
BLUE = (51, 51, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 255)

# draw color palette
pygame.draw.rect(screen, RED, (0, 50, 20, 20))
pygame.draw.rect(screen, YELLOW, (0, 70, 20, 20))
pygame.draw.rect(screen, GREEN, (20, 50, 20, 20))
pygame.draw.rect(screen, BLUE, (20, 70, 20, 20))
pygame.draw.rect(screen, BLACK, (0, 90, 20, 20))
pygame.draw.rect(screen, PINK, (20, 90, 20, 20))

erasor = pygame.transform.scale(
    pygame.image.load('practice10/paint/eraser.png'), (40, 40)
)  # load and resize eraser

screen.blit(erasor, [0, 110])  # draw eraser icon


def roundline(canvas, color, start, end, radius=1):  # smooth line drawing
    Xaxis = end[0] - start[0]  # difference in x
    Yaxis = end[1] - start[1]  # difference in y
    dist = max(abs(Xaxis), abs(Yaxis))  # calculate distance

    if dist == 0:  # avoid division by zero
        pygame.draw.circle(canvas, color, start, radius)
        return

    for i in range(dist):  # draw small circles
        x = int(start[0] + float(i) / dist * Xaxis)  # x position
        y = int(start[1] + float(i) / dist * Yaxis)  # y position
        pygame.draw.circle(canvas, color, (x, y), radius)  # draw point


try:
    while True:  # main loop

        e = pygame.event.wait()  # wait for event

        if e.type == pygame.QUIT:  # close window
            raise StopIteration

        if e.type == pygame.MOUSEBUTTONDOWN:  # mouse click

            spot = pygame.mouse.get_pos()  # get mouse position

            if spot[0] < 20 and spot[1] < 70 and spot[1] > 50:
                color = RED  # choose red
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 70 and spot[1] > 50:
                color = GREEN  # choose green
            elif spot[0] < 20 and spot[1] < 90 and spot[1] > 70:
                color = YELLOW  # choose yellow
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 90 and spot[1] > 70:
                color = BLUE  # choose blue
            elif spot[0] < 20 and spot[1] < 110 and spot[1] > 90:
                color = BLACK  # choose black
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 110 and spot[1] > 90:
                color = PINK  # choose pink
            elif spot[0] < 40 and spot[1] < 150 and spot[1] > 110:
                color = WHITE  # choose eraser

            if spot[0] > 60:  # draw only on canvas
                pygame.draw.circle(screen, color, e.pos, radius)

            draw_on = True  # enable drawing

        if e.type == pygame.MOUSEBUTTONUP:  # mouse released
            draw_on = False  # disable drawing

        if e.type == pygame.MOUSEMOTION:  # mouse movement

            spot = pygame.mouse.get_pos()  # get position

            if draw_on and spot[0] > 60:  # draw only on canvas
                pygame.draw.circle(screen, color, e.pos, radius)  # draw point
                roundline(screen, color, e.pos, last_pos, radius)  # smooth line

            last_pos = e.pos  # save last position

        if e.type == pygame.KEYDOWN:  # keyboard control

            spot = pygame.mouse.get_pos()  # get mouse position

            if e.key == pygame.K_r:  # draw rectangle
                pygame.draw.rect(screen, color, (spot[0], spot[1], 120, 80))

            elif e.key == pygame.K_s:  # draw square
                pygame.draw.rect(screen, color, (spot[0], spot[1], 100, 100))

            elif e.key == pygame.K_c:  # draw circle
                pygame.draw.circle(screen, color, (spot[0], spot[1]), 50)

            elif e.key == pygame.K_t:  # draw right triangle
                points = [
                    (spot[0], spot[1]),
                    (spot[0], spot[1] + 120),
                    (spot[0] + 120, spot[1] + 120)
                ]
                pygame.draw.polygon(screen, color, points)

            elif e.key == pygame.K_e:  # draw equilateral triangle
                side = 120  # triangle side
                height = int(side * math.sqrt(3) / 2)  # triangle height
                points = [
                    (spot[0], spot[1]),
                    (spot[0] - side // 2, spot[1] + height),
                    (spot[0] + side // 2, spot[1] + height)
                ]
                pygame.draw.polygon(screen, color, points)

            elif e.key == pygame.K_h:  # draw rhombus
                points = [
                    (spot[0], spot[1] - 70),
                    (spot[0] + 90, spot[1]),
                    (spot[0], spot[1] + 70),
                    (spot[0] - 90, spot[1])
                ]
                pygame.draw.polygon(screen, color, points)

        pygame.display.flip()  # update screen

except StopIteration:
    pass

pygame.quit()