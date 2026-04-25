import pygame, sys
from pygame.locals import *
import random, time

# Initialize Pygame
pygame.init()

# Game Constants and Parameters
FPS = 60
FramePerSec = pygame.time.Clock()

# Color Definitions (RGB)
BLUE  = (50, 50, 200)  
RED   = (200, 50, 50)  
YELLOW = (230, 200, 0) 
BLACK = (0, 0, 0)     
ROAD_GREY = (80, 80, 80)
WHITE = (255, 255, 255) 

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5        # Initial movement speed for obstacles and coins
SCORE = 0
COIN_SCORE = 0 
N = 10           # Threshold of coins collected to increase difficulty (SPEED)

# Font initializations for UI and labels
font_small = pygame.font.SysFont("Verdana", 20)
font_main = pygame.font.SysFont("Verdana", 40, bold=True)
font_coin = pygame.font.SysFont("Arial", 15, bold=True) # Used to display weight on coins

# Create the display surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game - Fixed Graphics")

def generate_game_asset(path, width, height, color):
    """
    Attempts to load an image asset. If the file is missing, 
    it generates a procedural geometric shape as a placeholder.
    """
    try:
        img = pygame.image.load(path).convert_alpha()
        print(f"[LOADED]: {path}")
        return pygame.transform.scale(img, (width, height))
    except FileNotFoundError:
        print(f"[MISSING/AUTO-GENERATING]: {path}")
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        if color == YELLOW: 
            # Draw a gold coin with a border and shine effect
            pygame.draw.circle(surf, color, (width // 2, height // 2), width // 2)
            pygame.draw.circle(surf, BLACK, (width // 2, height // 2), width // 2, 2) 
            shine = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.circle(shine, (255, 255, 255, 180), (width // 3, height // 3), width // 5) 
            surf.blit(shine, (0, 0))
        else: 
            # Draw a simple colored rectangle for cars
            pygame.draw.rect(surf, color, (0, 0, width, height), border_radius=10)
        return surf

# Initialize Graphics
p_img = generate_game_asset("images/player.png", 50, 90, BLUE)
e_img = generate_game_asset("images/enemy.png", 50, 90, RED)
c_img = generate_game_asset("images/coin.png", 30, 30, YELLOW)

def draw_background():
    """Renders the grey road and moving white lane markings."""
    DISPLAYSURF.fill(ROAD_GREY)
    line_width = 10
    line_height = 50
    line_spacing = 30
    for y in range(0, SCREEN_HEIGHT, line_height + line_spacing):
        # Center lane lines and side borders
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
        """Moves the enemy down. If it leaves the screen, it resets to the top."""
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
        """Handles horizontal movement based on arrow key inputs."""
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
        self.weight = random.choice([1, 5, 10]) # Assign random value/weight to coin
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        """Moves the coin down the screen."""
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.reset() 

    def reset(self):
        """Resets coin position and re-randomizes its weight value."""
        self.weight = random.choice([1, 5, 10])
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Sprite Setup
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

# --- MAIN GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    draw_background()
    
    # Render coin score UI
    coin_scores_surface = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(coin_scores_surface, (SCREEN_WIDTH - 110, 10))

    # Update and Render all entities
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        
        # If the entity is a Coin, overlay its weight value as text
        if isinstance(entity, Coin):
            val_surf = font_coin.render(str(entity.weight), True, BLACK)
            val_rect = val_surf.get_rect(center=entity.rect.center)
            DISPLAYSURF.blit(val_surf, val_rect)
            
        entity.move()

    # Coin Collection Logic
    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += C1.weight # Add the specific coin's value to total score
        
        # Difficulty Adjustment: Increase game speed every N coins
        if COIN_SCORE > 0 and COIN_SCORE % N == 0:
            SPEED += 1
            
        C1.reset()     

    # Collision with Enemy Logic
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)
        # Red semi-transparent overlay for Game Over
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((255, 0, 0))
        overlay.set_alpha(150)
        DISPLAYSURF.blit(overlay, (0, 0))
        
        # Display Final Result
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