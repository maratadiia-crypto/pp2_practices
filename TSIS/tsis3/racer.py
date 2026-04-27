import pygame
import random
from persistence import save_score

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 180, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 0, 200)
GRAY = (120, 120, 120)

LANES = [70, 160, 250, 330]


class RacerGame:
    def __init__(self, screen, username, settings):
        self.screen = screen
        self.username = username
        self.settings = settings

        self.font = pygame.font.SysFont("Verdana", 18)
        self.big_font = pygame.font.SysFont("Verdana", 40)

        self.running = True
        self.game_over = False

        self.base_speed = self.get_start_speed()
        self.speed = self.base_speed

        self.score = 0
        self.coins = 0
        self.distance = 0
        self.finish_distance = 3000

        self.player = pygame.Rect(170, 500, 45, 75)

        self.traffic = []
        self.obstacles = []
        self.coins_list = []
        self.powerups = []

        self.shield = False
        self.active_power = None
        self.power_end_time = 0

        self.spawn_timer = 0
        self.event_timer = 0

        self.player_color = self.get_car_color()

    def get_start_speed(self):
        if self.settings["difficulty"] == "easy":
            return 4
        elif self.settings["difficulty"] == "hard":
            return 7
        return 5

    def get_car_color(self):
        if self.settings["car_color"] == "red":
            return RED
        elif self.settings["car_color"] == "green":
            return GREEN
        return BLUE

    def safe_x(self):
        while True:
            x = random.choice(LANES)
            if abs(x - self.player.centerx) > 60:
                return x

    def spawn_traffic(self):
        rect = pygame.Rect(self.safe_x(), -90, 45, 75)
        self.traffic.append(rect)

    def spawn_obstacle(self):
        kind = random.choice(["barrier", "oil", "bump"])
        rect = pygame.Rect(self.safe_x(), -40, 45, 35)
        self.obstacles.append([rect, kind])

    def spawn_coin(self):
        value = random.choice([1, 2, 3])

        if value == 1:
            size = 24
        elif value == 2:
            size = 34
        else:
            size = 44

        rect = pygame.Rect(self.safe_x(), -50, size, size)
        self.coins_list.append([rect, value])

    def spawn_powerup(self):
        kind = random.choice(["nitro", "shield", "repair"])
        rect = pygame.Rect(self.safe_x(), -60, 35, 35)
        spawn_time = pygame.time.get_ticks()
        self.powerups.append([rect, kind, spawn_time])

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.player.left > 45:
            self.player.x -= 6

        if keys[pygame.K_RIGHT] and self.player.right < SCREEN_WIDTH - 35:
            self.player.x += 6

    def update_active_power(self):
        now = pygame.time.get_ticks()

        if self.active_power == "nitro":
            if now < self.power_end_time:
                self.speed = self.base_speed + 4
            else:
                self.active_power = None
                self.speed = self.base_speed

        if self.active_power == "shield":
            if now >= self.power_end_time:
                self.active_power = None
                self.shield = False

    def update_spawning(self):
        self.spawn_timer += 1
        self.event_timer += 1

        difficulty_bonus = self.distance // 700

        if self.spawn_timer > max(25, 70 - difficulty_bonus * 7):
            choice = random.choice(["traffic", "obstacle", "coin", "coin", "powerup"])

            if choice == "traffic":
                self.spawn_traffic()
            elif choice == "obstacle":
                self.spawn_obstacle()
            elif choice == "coin":
                self.spawn_coin()
            elif choice == "powerup":
                self.spawn_powerup()

            self.spawn_timer = 0

        if self.event_timer > 350:
            self.spawn_obstacle()
            self.spawn_powerup()
            self.event_timer = 0

    def move_objects(self):
        for car in self.traffic:
            car.y += self.speed

        for obstacle in self.obstacles:
            obstacle[0].y += self.speed

        for coin in self.coins_list:
            coin[0].y += self.speed

        for power in self.powerups:
            power[0].y += self.speed

        self.traffic = [car for car in self.traffic if car.top < SCREEN_HEIGHT]
        self.obstacles = [ob for ob in self.obstacles if ob[0].top < SCREEN_HEIGHT]
        self.coins_list = [coin for coin in self.coins_list if coin[0].top < SCREEN_HEIGHT]

        now = pygame.time.get_ticks()
        self.powerups = [
            power for power in self.powerups
            if power[0].top < SCREEN_HEIGHT and now - power[2] < 6000
        ]

    def check_collisions(self):
        for car in self.traffic[:]:
            if self.player.colliderect(car):
                if self.shield:
                    self.shield = False
                    self.active_power = None
                    self.traffic.remove(car)
                else:
                    self.finish_game()

        for obstacle in self.obstacles[:]:
            if self.player.colliderect(obstacle[0]):
                if obstacle[1] == "oil":
                    self.speed = max(2, self.speed - 1)
                    self.obstacles.remove(obstacle)
                elif self.shield:
                    self.shield = False
                    self.active_power = None
                    self.obstacles.remove(obstacle)
                else:
                    self.finish_game()

        for coin in self.coins_list[:]:
            if self.player.colliderect(coin[0]):
                self.coins += coin[1]
                self.score += coin[1] * 10
                self.coins_list.remove(coin)

                if self.coins % 6 == 0:
                    self.base_speed += 1

        for power in self.powerups[:]:
            if self.player.colliderect(power[0]):
                kind = power[1]
                self.powerups.remove(power)

                if kind == "nitro":
                    self.active_power = "nitro"
                    self.power_end_time = pygame.time.get_ticks() + 4000

                elif kind == "shield":
                    self.active_power = "shield"
                    self.shield = True
                    self.power_end_time = pygame.time.get_ticks() + 7000

                elif kind == "repair":
                    if self.obstacles:
                        self.obstacles.clear()
                    else:
                        self.score += 50

    def finish_game(self):
        self.game_over = True
        total_score = self.score + self.distance // 10 + self.coins * 5
        save_score(self.username, total_score, self.distance)

    def draw_road(self):
        self.screen.fill((40, 160, 40))
        pygame.draw.rect(self.screen, (70, 70, 70), (40, 0, 320, SCREEN_HEIGHT))

        for x in [120, 210, 300]:
            for y in range(0, SCREEN_HEIGHT, 60):
                pygame.draw.rect(self.screen, WHITE, (x, y, 5, 30))

    def draw_objects(self):
        pygame.draw.rect(self.screen, self.player_color, self.player)

        if self.shield:
            pygame.draw.circle(self.screen, BLUE, self.player.center, 48, 3)

        for car in self.traffic:
            pygame.draw.rect(self.screen, RED, car)

        for obstacle, kind in self.obstacles:
            if kind == "barrier":
                pygame.draw.rect(self.screen, ORANGE, obstacle)
            elif kind == "oil":
                pygame.draw.ellipse(self.screen, BLACK, obstacle)
            else:
                pygame.draw.rect(self.screen, GRAY, obstacle)

        for coin, value in self.coins_list:
            pygame.draw.ellipse(self.screen, YELLOW, coin)
            text = self.font.render(str(value), True, BLACK)
            self.screen.blit(text, text.get_rect(center=coin.center))

        for power, kind, spawn_time in self.powerups:
            if kind == "nitro":
                color = ORANGE
                label = "N"
            elif kind == "shield":
                color = BLUE
                label = "S"
            else:
                color = GREEN
                label = "R"

            pygame.draw.rect(self.screen, color, power)
            text = self.font.render(label, True, WHITE)
            self.screen.blit(text, text.get_rect(center=power.center))

    def draw_ui(self):
        total_score = self.score + self.distance // 10 + self.coins * 5
        remaining = max(0, self.finish_distance - self.distance)

        self.screen.blit(self.font.render(f"Score: {total_score}", True, BLACK), (10, 10))
        self.screen.blit(self.font.render(f"Coins: {self.coins}", True, BLACK), (10, 35))
        self.screen.blit(self.font.render(f"Distance: {self.distance}", True, BLACK), (10, 60))
        self.screen.blit(self.font.render(f"Left: {remaining}", True, BLACK), (10, 85))
        self.screen.blit(self.font.render(f"Speed: {self.speed}", True, BLACK), (10, 110))

        if self.active_power:
            left = max(0, (self.power_end_time - pygame.time.get_ticks()) // 1000)
            self.screen.blit(self.font.render(f"Power: {self.active_power} {left}s", True, BLACK), (10, 135))

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
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

            if not self.game_over:
                self.handle_input()
                self.update_active_power()
                self.update_spawning()
                self.move_objects()
                self.check_collisions()

                self.distance += 1
                if self.distance >= self.finish_distance:
                    self.finish_game()

            self.draw_road()
            self.draw_objects()
            self.draw_ui()

            if self.game_over:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(RED)
                self.screen.blit(overlay, (0, 0))

                total_score = self.score + self.distance // 10 + self.coins * 5

                text1 = self.big_font.render("GAME OVER", True, BLACK)
                text2 = self.font.render(f"Score: {total_score}", True, BLACK)
                text3 = self.font.render(f"Distance: {self.distance}", True, BLACK)
                text4 = self.font.render(f"Coins: {self.coins}", True, BLACK)
                text5 = self.font.render("R - Retry   M - Main Menu", True, BLACK)

                self.screen.blit(text1, (65, 210))
                self.screen.blit(text2, (120, 285))
                self.screen.blit(text3, (120, 315))
                self.screen.blit(text4, (120, 345))
                self.screen.blit(text5, (70, 390))

            pygame.display.update()