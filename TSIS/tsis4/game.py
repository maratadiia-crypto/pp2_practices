import pygame
import random
from db import save_session, get_personal_best

WIDTH, HEIGHT = 800, 700
BLOCK = 20
GRID_ROWS = 30
GRID_COLS = 30
MARGIN = 1
BG_PADDING = 10

BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
DARK_RED = (100, 0, 0)
WALL = (90, 90, 90)
BLUE = (50, 100, 255)
GREEN = (0, 180, 0)
PURPLE = (160, 0, 200)
ORANGE = (255, 140, 0)


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Food:
    def __init__(self, x, y, weight, poison=False):
        self.x = x
        self.y = y
        self.weight = weight
        self.poison = poison
        self.spawn_time = pygame.time.get_ticks()


class PowerUp:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.spawn_time = pygame.time.get_ticks()


class SnakeGame:
    def __init__(self, screen, username, settings):
        self.screen = screen
        self.username = username
        self.settings = settings

        self.font = pygame.font.SysFont("arial", 24)
        self.big_font = pygame.font.SysFont("arial", 42)

        self.grid_width = GRID_COLS * BLOCK + (GRID_COLS + 1) * MARGIN
        self.grid_height = GRID_ROWS * BLOCK + (GRID_ROWS + 1) * MARGIN
        self.start_x = (WIDTH - self.grid_width) // 2
        self.start_y = (HEIGHT - self.grid_height) // 2

        self.bg_surface = pygame.Surface(
            (self.grid_width + 2 * BG_PADDING, self.grid_height + 2 * BG_PADDING),
            pygame.SRCALPHA
        )
        self.bg_surface.fill((50, 50, 50, 180))

        self.snake_color = tuple(settings["snake_color"])
        self.snake = [Block(13, 13), Block(13, 14), Block(13, 15)]
        self.dx = 0
        self.dy = 1

        self.score = 0
        self.level = 1
        self.base_delay = 300
        self.move_delay = self.base_delay
        self.last_move = pygame.time.get_ticks()

        self.food_life_time = 5000
        self.power_life_time = 8000
        self.power_end_time = 0
        self.active_power = None
        self.shield = False

        self.personal_best = get_personal_best(username)

        self.obstacles = []
        self.food = None
        self.powerup = None

        self.game_over = False
        self.saved = False

        self.food = self.generate_food()

    def cell_to_rect(self, row, col):
        x = self.start_x + col * BLOCK + MARGIN * (col + 1)
        y = self.start_y + row * BLOCK + MARGIN * (row + 1)
        return pygame.Rect(x, y, BLOCK, BLOCK)

    def draw_block(self, color, row, col):
        pygame.draw.rect(self.screen, color, self.cell_to_rect(row, col))

    def occupied(self, x, y):
        for block in self.snake:
            if block.x == x and block.y == y:
                return True

        for wall in self.obstacles:
            if wall[0] == x and wall[1] == y:
                return True

        if self.food and self.food.x == x and self.food.y == y:
            return True

        if self.powerup and self.powerup.x == x and self.powerup.y == y:
            return True

        return False

    def generate_food(self):
        while True:
            x = random.randint(0, GRID_ROWS - 1)
            y = random.randint(0, GRID_COLS - 1)

            if not self.occupied(x, y):
                poison = random.randint(1, 6) == 1
                weight = random.choice([1, 2, 3])
                return Food(x, y, weight, poison)

    def generate_powerup(self):
        if self.powerup is not None:
            return

        if random.randint(1, 180) != 1:
            return

        while True:
            x = random.randint(0, GRID_ROWS - 1)
            y = random.randint(0, GRID_COLS - 1)

            if not self.occupied(x, y):
                kind = random.choice(["speed", "slow", "shield"])
                self.powerup = PowerUp(x, y, kind)
                return

    def generate_obstacles(self):
        self.obstacles = []

        if self.level < 3:
            return

        count = min(6 + self.level * 2, 25)

        while len(self.obstacles) < count:
            x = random.randint(2, GRID_ROWS - 3)
            y = random.randint(2, GRID_COLS - 3)
            head = self.snake[-1]

            if abs(head.x - x) <= 2 and abs(head.y - y) <= 2:
                continue

            if (x, y) in self.obstacles:
                continue

            if self.occupied(x, y):
                continue

            self.obstacles.append((x, y))

    def update_power_effects(self):
        now = pygame.time.get_ticks()

        if self.active_power == "speed":
            if now <= self.power_end_time:
                self.move_delay = max(100, self.base_delay - 100)
            else:
                self.active_power = None
                self.move_delay = self.base_delay

        elif self.active_power == "slow":
            if now <= self.power_end_time:
                self.move_delay = self.base_delay + 150
            else:
                self.active_power = None
                self.move_delay = self.base_delay

        elif self.active_power == "shield":
            if not self.shield:
                self.active_power = None

    def handle_powerup(self):
        if self.powerup is None:
            self.generate_powerup()
            return

        now = pygame.time.get_ticks()

        if now - self.powerup.spawn_time > self.power_life_time:
            self.powerup = None

    def shield_escape(self):
        if self.shield:
            self.shield = False
            self.active_power = None
            return True

        return False

    def end_game(self):
        self.game_over = True

        if not self.saved:
            save_session(self.username, self.score, self.level)
            self.saved = True

    def move_snake(self):
        now = pygame.time.get_ticks()

        if now - self.last_move < self.move_delay:
            return

        self.last_move = now

        head = self.snake[-1]
        new_x = head.x + self.dx
        new_y = head.y + self.dy

        if not (0 <= new_x < GRID_ROWS and 0 <= new_y < GRID_COLS):
            if not self.shield_escape():
                self.end_game()
            return

        if any(block.x == new_x and block.y == new_y for block in self.snake):
            if not self.shield_escape():
                self.end_game()
            return

        if (new_x, new_y) in self.obstacles:
            if not self.shield_escape():
                self.end_game()
            return

        self.snake.append(Block(new_x, new_y))

        if new_x == self.food.x and new_y == self.food.y:
            if self.food.poison:
                for _ in range(2):
                    if len(self.snake) > 0:
                        self.snake.pop(0)

                if len(self.snake) <= 1:
                    self.end_game()
                    return
            else:
                self.score += self.food.weight
                new_level = self.score // 5 + 1

                if new_level > self.level:
                    self.level = new_level
                    self.base_delay = max(110, self.base_delay - 25)
                    self.move_delay = self.base_delay
                    self.generate_obstacles()

            self.food = self.generate_food()
        else:
            self.snake.pop(0)

        if self.powerup and new_x == self.powerup.x and new_y == self.powerup.y:
            if self.powerup.kind == "speed":
                self.active_power = "speed"
                self.power_end_time = pygame.time.get_ticks() + 5000

            elif self.powerup.kind == "slow":
                self.active_power = "slow"
                self.power_end_time = pygame.time.get_ticks() + 5000

            elif self.powerup.kind == "shield":
                self.active_power = "shield"
                self.shield = True

            self.powerup = None

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.dy == 0:
            self.dx, self.dy = 0, -1

        elif keys[pygame.K_RIGHT] and self.dy == 0:
            self.dx, self.dy = 0, 1

        elif keys[pygame.K_UP] and self.dx == 0:
            self.dx, self.dy = -1, 0

        elif keys[pygame.K_DOWN] and self.dx == 0:
            self.dx, self.dy = 1, 0

    def update(self):
        if self.game_over:
            return

        now = pygame.time.get_ticks()

        if now - self.food.spawn_time > self.food_life_time:
            self.food = self.generate_food()

        self.update_power_effects()
        self.handle_powerup()
        self.handle_input()
        self.move_snake()

    def draw_food(self):
        if self.food.poison:
            self.draw_block(DARK_RED, self.food.x, self.food.y)
            text = self.font.render("P", True, WHITE)
        else:
            if self.food.weight == 1:
                color = RED
            elif self.food.weight == 2:
                color = ORANGE
            else:
                color = PURPLE

            self.draw_block(color, self.food.x, self.food.y)
            text = self.font.render(str(self.food.weight), True, WHITE)

        rect = self.cell_to_rect(self.food.x, self.food.y)
        self.screen.blit(text, text.get_rect(center=rect.center))

    def draw_powerup(self):
        if self.powerup is None:
            return

        if self.powerup.kind == "speed":
            color = BLUE
            label = "B"
        elif self.powerup.kind == "slow":
            color = GREEN
            label = "S"
        else:
            color = PURPLE
            label = "H"

        self.draw_block(color, self.powerup.x, self.powerup.y)
        text = self.font.render(label, True, WHITE)
        rect = self.cell_to_rect(self.powerup.x, self.powerup.y)
        self.screen.blit(text, text.get_rect(center=rect.center))

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_surface, (self.start_x - BG_PADDING, self.start_y - BG_PADDING))

        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                if self.settings["grid"]:
                    color = GRAY if (row + col) % 2 == 0 else WHITE
                else:
                    color = WHITE

                self.draw_block(color, row, col)

        for wall in self.obstacles:
            self.draw_block(WALL, wall[0], wall[1])

        self.draw_food()
        self.draw_powerup()

        for block in self.snake:
            self.draw_block(self.snake_color, block.x, block.y)

        self.screen.blit(self.font.render(f"Player: {self.username}", True, WHITE), (10, 10))
        self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (10, 40))
        self.screen.blit(self.font.render(f"Level: {self.level}", True, WHITE), (10, 70))
        self.screen.blit(self.font.render(f"Best: {self.personal_best}", True, WHITE), (10, 100))

        if self.active_power:

            remaining = max(
                0,
                (self.power_end_time - pygame.time.get_ticks()) // 1000
    )

            power_text = self.font.render(
                f"Power: {self.active_power}  Time: {remaining}s",
                True,
                WHITE
    )

            self.screen.blit(power_text, (10, 130))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return "retry"
                        if event.key == pygame.K_m:
                            return "menu"

            self.update()
            self.draw()

            if self.game_over:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(190)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))

                self.screen.blit(self.big_font.render("GAME OVER", True, RED), (270, 220))
                self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (320, 285))
                self.screen.blit(self.font.render(f"Level: {self.level}", True, WHITE), (320, 315))
                self.screen.blit(self.font.render(f"Best: {max(self.personal_best, self.score)}", True, WHITE), (320, 345))
                self.screen.blit(self.font.render("R - Retry   M - Main Menu", True, WHITE), (245, 395))

            pygame.display.flip()