import pygame
import random

pygame.init()

# screen
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# sizes and colors
BLOCK = 20
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
WHITE = (255, 255, 255)
SNAKE = (0, 200, 180)
FOOD_COLOR = (200, 50, 50)

MARGIN = 1
GRID_ROWS = 30
GRID_COLS = 30
BG_PADDING = 10

# grid coordinates
grid_width = GRID_COLS * BLOCK + (GRID_COLS + 1) * MARGIN
grid_height = GRID_ROWS * BLOCK + (GRID_ROWS + 1) * MARGIN
start_x = (WIDTH - grid_width) // 2
start_y = (HEIGHT - grid_height) // 2

# background surface
bg_surface = pygame.Surface(
    (grid_width + 2 * BG_PADDING, grid_height + 2 * BG_PADDING),
    pygame.SRCALPHA
)
bg_surface.fill((50, 50, 50, 180))

font = pygame.font.SysFont("arial", 24)

# snake block class
class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# starting snake
snake_block = [SnakeBlock(13, 13)]

dx, dy = 1, 0

clock = pygame.time.Clock()

speed = 2  # START SPEED = 2

move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 300)

score = 0
level = 1


# draw block
def draw_block(color, row, column):
    x = start_x + column * BLOCK + MARGIN * (column + 1)
    y = start_y + row * BLOCK + MARGIN * (row + 1)

    pygame.draw.rect(
        screen,
        color,
        [x, y, BLOCK, BLOCK]
    )


# generate food
def generate_food():
    while True:

        x = random.randint(0, GRID_ROWS - 1)
        y = random.randint(0, GRID_COLS - 1)

        occupied = any(
            block.x == x and block.y == y
            for block in snake_block
        )

        if not occupied:
            return SnakeBlock(x, y)


food = generate_food()

running = True


# game over screen
def show_game_over():

    global snake_block, dx, dy
    global score, level, speed, food

    while True:

        screen.fill(BLACK)

        text1 = font.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        text2 = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        text3 = font.render(
            f"Level: {level}",
            True,
            WHITE
        )

        text4 = font.render(
            "Press R to restart or Q to quit",
            True,
            WHITE
        )

        screen.blit(text1, (320, 250))
        screen.blit(text2, (330, 290))
        screen.blit(text3, (330, 320))
        screen.blit(text4, (200, 370))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    snake_block = [SnakeBlock(13, 13)]

                    dx, dy = 1, 0

                    score = 0
                    level = 1

                    speed = 2  # reset speed

                    food = generate_food()

                    return

                if event.key == pygame.K_q:

                    pygame.quit()
                    exit()


# main loop
while running:

    clock.tick(speed)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            show_game_over()
            break

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT and dy == 0:
                dx, dy = 0, -1

            elif event.key == pygame.K_RIGHT and dy == 0:
                dx, dy = 0, 1

            elif event.key == pygame.K_UP and dx == 0:
                dx, dy = -1, 0

            elif event.key == pygame.K_DOWN and dx == 0:
                dx, dy = 1, 0

        elif event.type == move_event:

            head = snake_block[-1]

            new_x = head.x + dx
            new_y = head.y + dy

            # border collision
            if not (
                0 <= new_x < GRID_ROWS
                and
                0 <= new_y < GRID_COLS
            ):
                show_game_over()
                break

            # self collision
            if any(
                block.x == new_x
                and
                block.y == new_y
                for block in snake_block
            ):
                show_game_over()
                break

            new_head = SnakeBlock(new_x, new_y)

            snake_block.append(new_head)

            # food collision
            if new_x == food.x and new_y == food.y:

                score += 1

                if score % 3 == 0:

                    level += 1
                    speed += 1  # increase speed slowly

                food = generate_food()

            else:

                snake_block.pop(0)

    screen.fill(BLACK)

    screen.blit(
        bg_surface,
        (start_x - BG_PADDING,
         start_y - BG_PADDING)
    )

    # draw grid
    for row in range(GRID_ROWS):
        for column in range(GRID_COLS):

            color = (
                GRAY
                if (row + column) % 2 == 0
                else WHITE
            )

            draw_block(
                color,
                row,
                column
            )

    # draw food
    draw_block(
        FOOD_COLOR,
        food.x,
        food.y
    )

    # draw snake
    for block in snake_block:

        draw_block(
            SNAKE,
            block.x,
            block.y
        )

    # draw score
    text = font.render(
        f"Score: {score}  Level: {level}",
        True,
        WHITE
    )

    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()