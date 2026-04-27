import pygame
from datetime import datetime
from tools import flood_fill, draw_equilateral_triangle, draw_right_triangle, draw_rhombus

pygame.init()

WIDTH, HEIGHT = 900, 700
TOOLBAR_WIDTH = 220

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (102, 204, 0)
BLUE = (51, 51, 255)
PINK = (255, 0, 255)
GRAY = (230, 230, 230)

color = BLACK
tool = "pencil"
brush_size = 2
draw_on = False
last_pos = None
start_pos = None
text_mode = False
text_pos = None
typed_text = ""

font = pygame.font.SysFont("arial", 18)
text_font = pygame.font.SysFont("arial", 28)
clock = pygame.time.Clock()


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, TOOLBAR_WIDTH, HEIGHT))

    pygame.draw.rect(screen, RED, (10, 40, 25, 25))
    pygame.draw.rect(screen, YELLOW, (45, 40, 25, 25))
    pygame.draw.rect(screen, GREEN, (80, 40, 25, 25))
    pygame.draw.rect(screen, BLUE, (115, 40, 25, 25))
    pygame.draw.rect(screen, BLACK, (150, 40, 25, 25))
    pygame.draw.rect(screen, PINK, (185, 40, 25, 25))

    instructions = [
        "P - pencil",
        "O - eraser",
        "L - line with preview",
        "F - flood fill",
        "X - text tool",
        "R - rectangle",
        "S - square",
        "C - circle",
        "T - right triangle",
        "E - equilateral triangle",
        "H - rhombus",
        "1 - small 2px",
        "2 - medium 5px",
        "3 - large 10px",
        "Ctrl+S - save",
        "",
        f"Tool: {tool}",
        f"Size: {brush_size}px"
    ]

    y = 90
    for text in instructions:
        label = font.render(text, True, BLACK)
        screen.blit(label, (10, y))
        y += 25


def choose_color(pos):
    global color

    x, y = pos

    if 10 <= x <= 35 and 40 <= y <= 65:
        color = RED
    elif 45 <= x <= 70 and 40 <= y <= 65:
        color = YELLOW
    elif 80 <= x <= 105 and 40 <= y <= 65:
        color = GREEN
    elif 115 <= x <= 140 and 40 <= y <= 65:
        color = BLUE
    elif 150 <= x <= 175 and 40 <= y <= 65:
        color = BLACK
    elif 185 <= x <= 210 and 40 <= y <= 65:
        color = PINK


def save_canvas():
    time_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{time_name}.png"
    pygame.image.save(canvas, filename)
    print("Saved as", filename)


running = True

while running:
    clock.tick(60)

    preview = canvas.copy()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and text_mode:
            if event.key == pygame.K_RETURN:
                text_surface = text_font.render(typed_text, True, color)
                canvas.blit(text_surface, text_pos)
                text_mode = False
                typed_text = ""

            elif event.key == pygame.K_ESCAPE:
                text_mode = False
                typed_text = ""

            elif event.key == pygame.K_BACKSPACE:
                typed_text = typed_text[:-1]

            else:
                typed_text += event.unicode

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            elif event.key == pygame.K_p:
                tool = "pencil"

            elif event.key == pygame.K_o:
                tool = "eraser"

            elif event.key == pygame.K_l:
                tool = "line"

            elif event.key == pygame.K_f:
                tool = "fill"

            elif event.key == pygame.K_x:
                tool = "text"

            elif event.key == pygame.K_1:
                brush_size = 2

            elif event.key == pygame.K_2:
                brush_size = 5

            elif event.key == pygame.K_3:
                brush_size = 10

            else:
                pos = pygame.mouse.get_pos()

                if pos[0] > TOOLBAR_WIDTH:
                    if event.key == pygame.K_r:
                        pygame.draw.rect(canvas, color, (pos[0], pos[1], 120, 80), brush_size)

                    elif event.key == pygame.K_s:
                        pygame.draw.rect(canvas, color, (pos[0], pos[1], 100, 100), brush_size)

                    elif event.key == pygame.K_c:
                        pygame.draw.circle(canvas, color, pos, 50, brush_size)

                    elif event.key == pygame.K_t:
                        draw_right_triangle(canvas, color, pos, brush_size)

                    elif event.key == pygame.K_e:
                        draw_equilateral_triangle(canvas, color, pos, brush_size)

                    elif event.key == pygame.K_h:
                        draw_rhombus(canvas, color, pos, brush_size)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if pos[0] <= TOOLBAR_WIDTH:
                choose_color(pos)

            else:
                if tool == "pencil":
                    draw_on = True
                    last_pos = pos

                elif tool == "eraser":
                    draw_on = True
                    last_pos = pos

                elif tool == "line":
                    start_pos = pos

                elif tool == "fill":
                    flood_fill(canvas, pos[0], pos[1], color)

                elif tool == "text":
                    text_mode = True
                    text_pos = pos
                    typed_text = ""

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if tool == "line" and start_pos is not None:
                pygame.draw.line(canvas, color, start_pos, pos, brush_size)
                start_pos = None

            draw_on = False
            last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()

            if draw_on and tool == "pencil" and pos[0] > TOOLBAR_WIDTH:
                pygame.draw.line(canvas, color, last_pos, pos, brush_size)
                last_pos = pos

            elif draw_on and tool == "eraser" and pos[0] > TOOLBAR_WIDTH:
                pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size)
                last_pos = pos

    if tool == "line" and start_pos is not None:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(preview, color, start_pos, mouse_pos, brush_size)

    screen.blit(preview, (0, 0))

    if text_mode and text_pos is not None:
        text_surface = text_font.render(typed_text, True, color)
        screen.blit(text_surface, text_pos)

    draw_toolbar()
    pygame.display.flip()

pygame.quit()