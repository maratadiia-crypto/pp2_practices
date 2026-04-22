import pygame
import random
import sys
from pygame.locals import *

pygame.init()  # initialize pygame

#settings
SCREEN_WIDTH = 400  
SCREEN_HEIGHT = 600  
FPS = 60 
FramePerSec = pygame.time.Clock()  #fps controller

SPEED = 5 
SCORE = 0  
COINS_COLLECTED = 0  #collected coins counter

WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
RED = (255, 0, 0) 

font_small = pygame.font.SysFont("Verdana", 20) 
font_big = pygame.font.SysFont("Verdana", 50) 

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #create screen
pygame.display.set_caption("Racer Game") 
background = pygame.image.load('practice10/racer/AnimatedStreet.png') #load background
#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # initialize sprite

        self.image = pygame.image.load('practice10/racer/Player.png')  # load player image
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  #starting position

    def move(self):
        pressed_keys = pygame.key.get_pressed()  #get pressed keys

        if pressed_keys[K_LEFT] and self.rect.left > 0:  #move left
            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:  #move right
            self.rect.move_ip(5, 0)


#enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # initialize sprite

        self.image = pygame.image.load('practice10/racer/Enemy.png')  # load enemy image
        self.rect = self.image.get_rect()  
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  #random start

    def move(self):
        global SCORE

        self.rect.move_ip(0, SPEED)  #move enemy down

        if self.rect.top > SCREEN_HEIGHT:  # if enemy leaves screen
            SCORE += 1  #increase score
            self.rect.top = 0  # reset position
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


#coin
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  #initialize sprite

        self.image = pygame.image.load('practice10/racer/Coin.png')  # load coin image
        self.image = pygame.transform.scale(self.image, (40, 40))  # resize coin
        self.rect = self.image.get_rect()  

        self.reset_position()  #set random start

    def reset_position(self):
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),  #random x
            random.randint(-300, -50)  #random y 
        )

    def move(self):
        self.rect.move_ip(0, SPEED)  #move coin down

        if self.rect.top > SCREEN_HEIGHT:  # if coin leaves screen
            self.reset_position()  #create new position


#objects
P1 = Player()  
E1 = Enemy() 
C1 = Coin() 

enemies = pygame.sprite.Group()  #group for enemies
enemies.add(E1)
coins = pygame.sprite.Group()  #group for coins
coins.add(C1)
all_sprites = pygame.sprite.Group()  #group for all sprites
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)


#speed event
INC_SPEED = pygame.USEREVENT + 1  #create custom event
pygame.time.set_timer(INC_SPEED, 1000)  #trigger every second


#gamee over
def game_over():
    DISPLAYSURF.fill(RED)  #fill screen red

    game_over_text = font_big.render("Game Over", True, BLACK) 
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK) 
    coin_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)  

    DISPLAYSURF.blit(game_over_text, (70, 220))
    DISPLAYSURF.blit(score_text, (140, 300)) 
    DISPLAYSURF.blit(coin_text, (140, 330))  

    pygame.display.update()  #update screen
    pygame.time.delay(2000)  #pause 2 sec

    pygame.quit() 
    sys.exit()  


#main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:  #exit window
            pygame.quit()
            sys.exit()

        if event.type == INC_SPEED:  #increase speed
            SPEED += 0.2

    DISPLAYSURF.blit(background, (0, 0))  #draw background

    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)  #score text
    DISPLAYSURF.blit(score_text, (10, 10))  #draw score

    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)  
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - coins_text.get_width() - 10, 10))  # draw coins
    P1.move()  
    E1.move() 
    C1.move() 

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)  #draw sprites

    if pygame.sprite.spritecollideany(P1, coins):  #collision with coin
        COINS_COLLECTED += 1  
        C1.reset_position() 

    if pygame.sprite.spritecollideany(P1, enemies):  #collision with enemy
        game_over()  

    pygame.display.update() 
    FramePerSec.tick(FPS)  