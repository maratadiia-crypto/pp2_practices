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
WALL_COLOR = (100, 100, 100)
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
bg_surface.fill((50, 50, 50, 180))  # semi transparent background

font = pygame.font.SysFont("arial", 24)  # create font

# snake block class
class SnakeBlock:
    def __init__(self, x, y):
        self.x = x  # row position
        self.y = y  # column position


# food class
class Food:
    def __init__(self, x, y, weight):
        self.x = x  # row position
        self.y = y  # column position
        self.weight = weight  # food weight
        self.spawn_time = pygame.time.get_ticks()  # spawn time


# starting snake
snake_block = [SnakeBlock(13, 13)]  # initial snake
dx, dy = 1, 0  # start moving right

clock = pygame.time.Clock()  # create clock
speed = 6  # starting speed

move_event = pygame.USEREVENT + 1  # movement event
pygame.time.set_timer(move_event, 150)  # movement interval

score = 0  # score counter
level = 1  # level counter
food_life_time = 5000  # food life time in milliseconds


# create walls depending on level
def get_walls(level):
    walls = []  # list of walls

    if level >= 2:  # level 2 wall
        for i in range(10, 20):
            walls.append((15, i))

    if level >= 3:  # level 3 walls
        for i in range(5, 15):
            walls.append((10, i))
            walls.append((20, i))

    if level >= 4:  # level 4 rectangle
        for i in range(8, 22):
            walls.append((i, 8))
            walls.append((i, 21))
        for i in range(9, 21):
            walls.append((8, i))
            walls.append((21, i))

    return walls


walls = get_walls(level)  # initial walls


# draw block
def draw_block(color, row, column):
    x = start_x + column * BLOCK + MARGIN * (column + 1)
    y = start_y + row * BLOCK + MARGIN * (row + 1)
    pygame.draw.rect(screen, color, [x, y, BLOCK, BLOCK])


# generate food not on snake and not on walls
def generate_food():
    while True:
        x = random.randint(0, GRID_ROWS - 1)
        y = random.randint(0, GRID_COLS - 1)

        occupied = any(
            block.x == x and block.y == y for block in snake_block
        )

        wall_hit = any(
            wall[0] == x and wall[1] == y for wall in walls
        )

        if not occupied and not wall_hit:
            weight = random.choice([1, 2, 3])  # random food weight
            return Food(x, y, weight)


# draw food with different size
def draw_food(food):
    if food.weight == 1:  # small food
        color = (200, 50, 50)
    elif food.weight == 2:  # medium food
        color = (255, 140, 0)
    else:  # big food
        color = (160, 0, 200)

    draw_block(color, food.x, food.y)  # draw food

    text = font.render(str(food.weight), True, WHITE)  # weight text
    x = start_x + food.y * BLOCK + MARGIN * (food.y + 1)
    y = start_y + food.x * BLOCK + MARGIN * (food.x + 1)
    screen.blit(text, (x + 4, y - 3))  # draw weight


food = generate_food()  # first food
running = True  # game loop


def show_game_over():  # game over screen
    global snake_block, dx, dy, score, level, speed, walls, food

    while True:
        screen.fill(BLACK)  # clear screen

        text1 = font.render("GAME OVER", True, (255, 0, 0))  # title
        text2 = font.render(f"Score: {score}", True, WHITE)  # score text
        text3 = font.render(f"Level: {level}", True, WHITE)  # level text
        text4 = font.render("Press R to restart or Q to quit", True, WHITE)  # help text

        screen.blit(text1, (320, 250))  # draw title
        screen.blit(text2, (330, 290))  # draw score
        screen.blit(text3, (330, 320))  # draw level
        screen.blit(text4, (200, 370))  # draw help

        pygame.display.flip()  # update screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restart game
                    snake_block = [SnakeBlock(13, 13)]  # reset snake
                    dx, dy = 1, 0  # reset direction
                    score = 0  # reset score
                    level = 1  # reset level
                    speed = 6  # reset speed
                    walls = get_walls(level)  # reset walls
                    food = generate_food()  # new food
                    return

                if event.key == pygame.K_q:  # quit game
                    pygame.quit()
                    exit()


while running:
    clock.tick(speed)  # control speed

    # food disappears after some time
    current_time = pygame.time.get_ticks()  # current time
    if current_time - food.spawn_time > food_life_time:
        food = generate_food()  # create new food

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:

            # arrow key controls
            if event.key == pygame.K_LEFT and dy == 0:
                dx, dy = 0, -1

            elif event.key == pygame.K_RIGHT and dy == 0:
                dx, dy = 0, 1

            elif event.key == pygame.K_UP and dx == 0:
                dx, dy = -1, 0

            elif event.key == pygame.K_DOWN and dx == 0:
                dx, dy = 1, 0

        elif event.type == move_event:

            head = snake_block[-1]  # current head

            new_x = head.x + dx  # new row
            new_y = head.y + dy  # new column

            # border collision
            if not (0 <= new_x < GRID_ROWS and 0 <= new_y < GRID_COLS):
                show_game_over()
                break

            # self collision
            if any(
                block.x == new_x and block.y == new_y
                for block in snake_block
            ):
                show_game_over()
                break

            # wall collision
            if any(
                wall[0] == new_x and wall[1] == new_y
                for wall in walls
            ):
                show_game_over()
                break

            new_head = SnakeBlock(new_x, new_y)
            snake_block.append(new_head)

            # food collision
            if new_x == food.x and new_y == food.y:
                score += food.weight  # add food weight to score

                # level change
                if score // 5 + 1 > level:
                    level += 1
                    speed += 2
                    walls = get_walls(level)

                food = generate_food()  # new food

            else:
                snake_block.pop(0)  # remove tail

    screen.fill(BLACK)

    screen.blit(
        bg_surface,
        (start_x - BG_PADDING, start_y - BG_PADDING)
    )

    # draw grid
    for row in range(GRID_ROWS):
        for column in range(GRID_COLS):
            color = GRAY if (row + column) % 2 == 0 else WHITE
            draw_block(color, row, column)

    # draw walls
    for wall in walls:
        draw_block(WALL_COLOR, wall[0], wall[1])

    # draw food
    draw_food(food)

    # draw snake
    for block in snake_block:
        draw_block(SNAKE, block.x, block.y)

    # draw score and level
    text = font.render(
        f"Score: {score}  Level: {level}",
        True,
        WHITE
    )
    screen.blit(text, (10, 10))

    # draw timer
    time_left = max(0, (food_life_time - (pygame.time.get_ticks() - food.spawn_time)) // 1000)
    timer_text = font.render(f"Food time: {time_left}", True, WHITE)
    screen.blit(timer_text, (10, 40))

    pygame.display.flip()

pygame.quit()