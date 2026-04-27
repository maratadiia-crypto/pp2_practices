import pygame

pygame.init()  # initialize pygame

# screen settings
screen = pygame.display.set_mode((900, 700))  # create screen
screen.fill((255, 255, 255))  # fill background white
pygame.display.set_caption('GFG Paint')  # set title

draw_on = False  # drawing state
last_pos = (0, 0)  # last mouse position
radius = 5  # brush size
color = (0, 0, 0)  # default color

# colors
WHITE = (255, 255, 255)  # white color
RED = (255, 0, 0)  # red color
YELLOW = (255, 255, 0)  # yellow color
GREEN = (102, 204, 0)  # green color
BLUE = (51, 51, 255)  # blue color
BLACK = (0, 0, 0)  # black color
PINK = (255, 0, 255)  # pink color

# draw color palette
pygame.draw.rect(screen, RED, (0, 50, 20, 20))  # red button
pygame.draw.rect(screen, YELLOW, (0, 70, 20, 20))  # yellow button
pygame.draw.rect(screen, GREEN, (20, 50, 20, 20))  # green button
pygame.draw.rect(screen, BLUE, (20, 70, 20, 20))  # blue button
pygame.draw.rect(screen, BLACK, (0, 90, 20, 20))  # black button
pygame.draw.rect(screen, PINK, (20, 90, 20, 20))  # pink button

# eraser icon
erasor = pygame.transform.scale(
    pygame.image.load('practice10/paint/eraser.png'), (40, 40)
)  # load and resize eraser
screen.blit(erasor, [0, 110])  # draw eraser icon

# instructions
font = pygame.font.SysFont("arial", 18)  # create font
instructions = [
    "R - rectangle",
    "S - square",
    "C - circle",
    "T - right triangle",
    "E - equilateral triangle",
    "H - rhombus",
    "click colors on the left",
    "click eraser icon to erase"
]

y_text = 10
for text in instructions:
    label = font.render(text, True, BLACK)  # create instruction text
    screen.blit(label, (60, y_text))  # draw instruction
    y_text += 22


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

            # color selection
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
                pygame.draw.circle(screen, color, e.pos, radius)  # draw point

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
                pygame.draw.rect(
                    screen,
                    color,
                    (spot[0], spot[1], 120, 80),
                    2  # outline only
                )

            elif e.key == pygame.K_s:  # draw square
                pygame.draw.rect(
                    screen,
                    color,
                    (spot[0], spot[1], 100, 100),
                    2  # outline only
                )

            elif e.key == pygame.K_c:  # draw circle
                pygame.draw.circle(
                    screen,
                    color,
                    (spot[0], spot[1]),
                    50,
                    2  # outline only
                )

            elif e.key == pygame.K_t:  # draw right triangle
                points = [
                    (spot[0], spot[1]),
                    (spot[0], spot[1] + 120),
                    (spot[0] + 120, spot[1] + 120)
                ]
                pygame.draw.polygon(screen, color, points, 2)  # outline only

            elif e.key == pygame.K_e:  # draw equilateral triangle
                points = [
                    (spot[0], spot[1]),
                    (spot[0] - 60, spot[1] + 100),
                    (spot[0] + 60, spot[1] + 100)
                ]
                pygame.draw.polygon(screen, color, points, 2)  # outline only

            elif e.key == pygame.K_h:  # draw rhombus
                points = [
                    (spot[0], spot[1] - 70),
                    (spot[0] + 90, spot[1]),
                    (spot[0], spot[1] + 70),
                    (spot[0] - 90, spot[1])
                ]
                pygame.draw.polygon(screen, color, points, 2)  # outline only

        pygame.display.flip()  # update screen

except StopIteration:
    pass

pygame.quit()  # close pygame