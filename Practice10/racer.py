import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (50, 50, 200)  
RED   = (200, 50, 50)  
YELLOW = (230, 200, 0) 
BLACK = (0, 0, 0)     
ROAD_GREY = (80, 80, 80)
WHITE = (255, 255, 255) 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0 

font_small = pygame.font.SysFont("Verdana", 20)
font_main = pygame.font.SysFont("Verdana", 40, bold=True)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game - Universal Graphics")

def generate_game_asset(path, width, height, color):
    try:
        img = pygame.image.load(path).convert_alpha()
        print(f"[LOADED]: {path}")
        return pygame.transform.scale(img, (width, height))
    except FileNotFoundError:
        print(f"[MISSING/AUTO-GENERATING]: {path}")
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        
        
        if color == YELLOW: 
            pygame.draw.circle(surf, color, (width // 2, height // 2), width // 2)
            pygame.draw.circle(surf, BLACK, (width // 2, height // 2), width // 2, 2) 
            shine = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.circle(shine, (255, 255, 255, 180), (width // 3, height // 3), width // 5) 
            surf.blit(shine, (0, 0))
        else: 
            pygame.draw.rect(surf, color, (0, 0, width, height), border_radius=10)
            win_color = (150, 150, 150)
            pygame.draw.rect(surf, win_color, (5, 5, width-10, height//2), border_radius=8) 
            pygame.draw.rect(surf, (0, 0, 0, 100), (8, 8, width-16, (height//2)-6), border_radius=5) 
            light_color = (255, 255, 100) if color == BLUE else (255, 50, 50) 
            pygame.draw.ellipse(surf, light_color, (5, height-15, width//4, 10))
            pygame.draw.ellipse(surf, light_color, (width-(width//4)-5, height-15, width//4, 10))
            pygame.draw.rect(surf, BLACK, (0, 0, width, height), 2, border_radius=10) 

        return surf

p_img = generate_game_asset("images/player.png", 50, 90, BLUE)
e_img = generate_game_asset("images/enemy.png", 50, 90, RED)
c_img = generate_game_asset("images/coin.png", 30, 30, YELLOW)

def draw_background():
    DISPLAYSURF.fill(ROAD_GREY)
    line_width = 10
    line_height = 50
    line_spacing = 30
    for y in range(0, SCREEN_HEIGHT, line_height + line_spacing):
        pygame.draw.rect(DISPLAYSURF, WHITE, (SCREEN_WIDTH//2 - line_width//2, y, line_width, line_height))
        pygame.draw.rect(DISPLAYSURF, WHITE, (10, y, 5, line_height))
        pygame.draw.rect(DISPLAYSURF, WHITE, (SCREEN_WIDTH - 15, y, 5, line_height))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = e_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1 
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = p_img
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = c_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.reset() 

    def reset(self):
        """Helper to move the coin back to the top in a new random lane."""
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

P1 = Player()
E1 = Enemy()
C1 = Coin() 

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group() 
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1) 


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    
    draw_background()
    
    
    coin_scores_surface = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(coin_scores_surface, (SCREEN_WIDTH - 110, 10))

    
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        
        entity.move()


    if pygame.sprite.spritecollideany(P1, coins):
       
        COIN_SCORE += 1 
        C1.reset()     
    if pygame.sprite.spritecollideany(P1, enemies):
        
        time.sleep(0.5)
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((255, 0, 0))
        overlay.set_alpha(150)
        DISPLAYSURF.blit(overlay, (0, 0))
        
        game_over_surface = font_main.render("GAME OVER", True, BLACK)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        DISPLAYSURF.blit(game_over_surface, game_over_rect)
        
        final_score_surface = font_small.render(f"Final Coins: {COIN_SCORE}", True, BLACK)
        DISPLAYSURF.blit(final_score_surface, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.update()
        time.sleep(2) 
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)