import pygame, sys, random, time
from pygame.locals import *

# --- System Initialization ---
pygame.init()

# Display settings and screen constants
WIDTH, HEIGHT = 600, 850
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Pro: Ultra Edition")
clock = pygame.time.Clock()

# Modern UI Color Palette (RGB)
COLOR_ASPHALT = (35, 35, 40)
COLOR_GRASS   = (34, 139, 34)
COLOR_GOLD    = (255, 215, 0)
COLOR_WHITE   = (245, 245, 245)
COLOR_RED     = (220, 20, 60)
COLOR_BLUE    = (0, 150, 255)
COLOR_HUD     = (20, 20, 25, 180) # Semi-transparent background for UI

# Global Game Variables
FPS = 60
SPEED = 6
SCORE = 0
COINS = 0
OFFSET = 0  # Used for the scrolling road animation

# Font initializations
font_huge = pygame.font.SysFont("Impact", 80)
font_med  = pygame.font.SysFont("Verdana", 28, bold=True)
font_coin = pygame.font.SysFont("Arial", 22, bold=True)

# --- Advanced Graphic Generators ---
def create_car_model(color, w, h):
    """
    Creates a detailed procedural car sprite if PNG files are missing.
    Includes body, windows, lights, and bumpers.
    """
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    # Main car body
    pygame.draw.rect(surf, color, (5, 10, w-10, h-20), border_radius=15)
    # Windshield and windows
    pygame.draw.rect(surf, (30, 30, 30), (12, 30, w-24, 25), border_radius=5)
    # Rear bumper/spoiler
    pygame.draw.rect(surf, (10, 10, 10), (5, h-15, w-10, 10), border_radius=3)
    # Headlights
    pygame.draw.circle(surf, (255, 255, 200), (20, 15), 5)
    pygame.draw.circle(surf, (255, 255, 200), (w-20, 15), 5)
    return surf

def create_coin_model():
    """Generates a gold coin sprite with a border and a shine effect."""
    surf = pygame.Surface((45, 45), pygame.SRCALPHA)
    pygame.draw.circle(surf, COLOR_GOLD, (22, 22), 22)
    pygame.draw.circle(surf, (184, 134, 11), (22, 22), 22, 3) # Coin border
    pygame.draw.circle(surf, (255, 255, 255, 150), (15, 15), 5) # Shine effect
    return surf

# Initialize Graphics
P_IMG = create_car_model(COLOR_BLUE, 75, 140)
E_IMG = create_car_model(COLOR_RED, 75, 140)
C_IMG = create_coin_model()

# --- Game Object Classes ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = E_IMG
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        """Resets the enemy to a random position above the screen."""
        self.rect.center = (random.randint(100, WIDTH-100), -150)
        
    def move(self):
        """Moves enemy down. Increments global SCORE when avoided."""
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            SCORE += 1
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = P_IMG
        self.rect = self.image.get_rect()
        # Initial starting position at the bottom center
        self.rect.center = (WIDTH // 2, HEIGHT - 150)

    def move(self):
        """Handles horizontal movement with boundary checks."""
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 40:
            self.rect.move_ip(-9, 0)
        if keys[K_RIGHT] and self.rect.right < WIDTH - 40:
            self.rect.move_ip(9, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = C_IMG
        self.rect = self.image.get_rect()
        self.weight = 1
        self.spawn()

    def spawn(self):
        """Assigns a random value to the coin and teleports it to the top."""
        self.weight = random.choice([1, 5, 10])
        self.rect.center = (random.randint(100, WIDTH-100), -200)

    def move(self):
        """Moves the coin down the screen."""
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self.spawn()

# --- Environment Rendering ---
def draw_world():
    """Renders the moving road, grass, and lane markings."""
    global OFFSET
    # Fill background with grass color
    DISPLAYSURF.fill(COLOR_GRASS)
    # Draw the main asphalt road
    pygame.draw.rect(DISPLAYSURF, COLOR_ASPHALT, (60, 0, WIDTH-120, HEIGHT))
    
    # Animated lane markings (scrolling effect)
    OFFSET = (OFFSET + SPEED) % 100
    for y in range(-100, HEIGHT + 100, 100):
        pygame.draw.rect(DISPLAYSURF, COLOR_WHITE, (WIDTH//2 - 5, y + OFFSET, 10, 50))
    
    # Side road borders (shoulder lines)
    pygame.draw.rect(DISPLAYSURF, (200, 200, 200), (60, 0, 5, HEIGHT))
    pygame.draw.rect(DISPLAYSURF, (200, 200, 200), (WIDTH-65, 0, 5, HEIGHT))

# Initialize Sprite Objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Create Sprite Groups for efficient management
enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

# --- Main Game Loop ---
while True:
    # 1. Event Handling (Window closing)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 2. Render Background
    draw_world()

    # 3. Update and Draw Sprites
    for sprite in all_sprites:
        sprite.move()
        DISPLAYSURF.blit(sprite.image, sprite.rect)
        
        # Overlay the coin's value as text on top of the sprite
        if isinstance(sprite, Coin):
            val_txt = font_coin.render(str(sprite.weight), True, (50, 50, 0))
            DISPLAYSURF.blit(val_txt, val_txt.get_rect(center=sprite.rect.center))

    # 4. User Interface (HUD)
    # Draw a semi-transparent panel for stats
    hud_bg = pygame.Surface((WIDTH, 70), pygame.SRCALPHA)
    hud_bg.fill(COLOR_HUD)
    DISPLAYSURF.blit(hud_bg, (0, 0))
    
    score_surf = font_med.render(f"DISTANCE: {SCORE}m", True, COLOR_WHITE)
    coin_surf  = font_med.render(f"GOLD: {COINS}", True, COLOR_GOLD)
    DISPLAYSURF.blit(score_surf, (20, 15))
    DISPLAYSURF.blit(coin_surf, (WIDTH - 180, 15))

    # 5. Collision Detection (Coins)
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += C1.weight
        # Increase game speed every 10 gold collected
        if COINS % 10 == 0: SPEED += 1 
        C1.spawn()

    # 6. Collision Detection (Game Over)
    if pygame.sprite.spritecollideany(P1, enemies):
        # Create a red-tinted game over overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        DISPLAYSURF.blit(overlay, (0, 0))
        
        text = font_huge.render("WASTED", True, (255, 0, 0))
        DISPLAYSURF.blit(text, (WIDTH//2 - 140, HEIGHT//2 - 100))
        
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Final screen update and frame rate capping
    pygame.display.update()
    clock.tick(FPS)