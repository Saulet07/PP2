import pygame
import random
import time

pygame.init()

# --- Color Palette (Neon Theme) ---
BG_DARK = (5, 5, 15)
NEON_CYAN = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# --- Game Settings ---
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 25
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Ultra - Food Timer Edition')
clock = pygame.time.Clock()

font_score = pygame.font.SysFont("Fixedsys", 30)
font_menu = pygame.font.SysFont("Verdana", 40, bold=True)

# 1. Food Class: Manages weight, color, and expiration timer
class Food:
    def __init__(self):
        self.spawn_food()

    def spawn_food(self):
        # Random weight (1 to 3) - dictates growth and points
        self.weight = random.randint(1, 3)
        
        # Color coding based on weight
        if self.weight == 1: self.color = NEON_PINK
        elif self.weight == 2: self.color = NEON_YELLOW
        else: self.color = WHITE
        
        # Grid-snapped random coordinates
        self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE
        self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE
        
        # 2. Food Lifetime Management
        # Heavier food disappears faster (5-8 seconds)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(5000, 8000) 

    def draw(self, surface):
        # Check if food has expired; if so, respawn elsewhere
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.spawn_food()

        # Visual pulse effect for the food
        pulse = abs(int(pygame.time.get_ticks() / 100 % 10 - 5))
        pygame.draw.circle(surface, self.color, (self.x + BLOCK_SIZE//2, self.y + BLOCK_SIZE//2), 
                           (BLOCK_SIZE//2 - pulse) + (self.weight * 2))

# --- Particle System for "Eating" Effect ---
particles = []

def create_particles(x, y, color):
    """Creates a burst of particles when food is eaten."""
    for _ in range(15):
        particles.append([[x + BLOCK_SIZE//2, y + BLOCK_SIZE//2], 
                          [random.randint(-5, 5), random.randint(-5, 5)], 
                          random.randint(4, 7), color])

def draw_particles():
    """Updates and renders particles on the screen."""
    for p in particles[:]:
        p[0][0] += p[1][0] # Move X
        p[0][1] += p[1][1] # Move Y
        p[2] -= 0.2        # Shrink size
        if p[2] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(dis, p[3], (int(p[0][0]), int(p[0][1])), int(p[2]))

def draw_snake_pro(snake_list):
    """Draws the snake with a gradient size effect (head is larger)."""
    for i, seg in enumerate(snake_list):
        size_factor = 0.5 + (i / len(snake_list)) * 0.5
        current_size = int((BLOCK_SIZE // 2) * size_factor)
        center_x = seg[0] + BLOCK_SIZE // 2
        center_y = seg[1] + BLOCK_SIZE // 2
        
        # Head is Cyan, body is Blue
        color = NEON_CYAN if i == len(snake_list)-1 else (0, 150, 255)
        pygame.draw.circle(dis, color, (center_x, center_y), current_size)

# --- Main Game Loop ---
def game_loop():
    game_over = False
    game_close = False
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0
    snake_list = []
    snake_len = 1
    score, level, speed = 0, 1, 12

    # Initialize the first food object
    current_food = Food()

    while not game_over:
        # Game Over Screen Logic
        while game_close:
            dis.fill(BG_DARK)
            msg = font_score.render("GAME OVER! C-Restart, Q-Quit", True, NEON_PINK)
            dis.blit(msg, [WIDTH // 4, HEIGHT // 2])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        game_loop()

        # Input Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Prevent 180-degree turns (cannot go left if moving right)
                if event.key == pygame.K_LEFT and dx == 0: dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0: dy, dx = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and dy == 0: dy, dx = BLOCK_SIZE, 0

        # Boundary Collision Detection
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += dx
        y += dy
        dis.fill(BG_DARK)

        # Background Grid (Visual Only)
        for i in range(0, WIDTH, BLOCK_SIZE * 2):
            pygame.draw.line(dis, (15, 15, 40), (i, 0), (i, HEIGHT))
        for i in range(0, HEIGHT, BLOCK_SIZE * 2):
            pygame.draw.line(dis, (15, 15, 40), (0, i), (WIDTH, i))

        # Update and Draw Food
        current_food.draw(dis)
        
        # Snake Movement Logic (adding head, removing tail)
        head = [x, y]
        snake_list.append(head)
        if len(snake_list) > snake_len:
            del snake_list[0]

        # Self-Collision Detection
        for seg in snake_list[:-1]:
            if seg == head:
                game_close = True

        # Render Particles and Snake
        draw_particles()
        draw_snake_pro(snake_list)
        
        # Display Score and Level
        score_txt = font_score.render(f"SCORE: {score} | LVL: {level}", True, NEON_CYAN)
        dis.blit(score_txt, [20, 20])

        pygame.display.update()

        # Food Collision (Eating)
        if x == current_food.x and y == current_food.y:
            create_particles(current_food.x, current_food.y, current_food.color)
            
            # Increase score and length based on food's weight
            score += current_food.weight
            snake_len += current_food.weight
            
            # Respawn new food
            current_food.spawn_food()
            
            # Leveling System: Increase speed every 10 points
            if score // 10 >= level:
                level += 1
                speed += 1

        clock.tick(speed)

    pygame.quit()
    quit()

# --- Start Screen ---
def welcome_screen():
    menu = True
    while menu:
        dis.fill(BG_DARK)
        title = font_menu.render("SNAKE ULTRA NEON", True, NEON_CYAN)
        start_msg = font_score.render("Press SPACE to Start", True, WHITE)
        dis.blit(title, [WIDTH // 4, HEIGHT // 3])
        dis.blit(start_msg, [WIDTH // 3, HEIGHT // 2])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                    game_loop()

welcome_screen()