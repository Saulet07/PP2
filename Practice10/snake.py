import pygame
import random
import time

pygame.init()

BG_DARK = (5, 5, 15)
NEON_CYAN = (0, 255, 255)
NEON_PINK = (255, 0, 255)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 25
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Ultra')
clock = pygame.time.Clock()

font_score = pygame.font.SysFont("Fixedsys", 30)
font_menu = pygame.font.SysFont("Verdana", 40, bold=True)

particles = []

def create_particles(x, y, color):
    for _ in range(15):
        particles.append([[x + BLOCK_SIZE//2, y + BLOCK_SIZE//2], 
                          [random.randint(-5, 5), random.randint(-5, 5)], 
                          random.randint(4, 7), color])

def draw_particles():
    for p in particles[:]:
        p[0][0] += p[1][0]
        p[0][1] += p[1][1]
        p[2] -= 0.2
        if p[2] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(dis, p[3], (int(p[0][0]), int(p[0][1])), int(p[2]))

def draw_snake_pro(snake_list):
    for i, seg in enumerate(snake_list):
        size_factor = 0.5 + (i / len(snake_list)) * 0.5
        current_size = int((BLOCK_SIZE // 2) * size_factor)
        center_x = seg[0] + BLOCK_SIZE // 2
        center_y = seg[1] + BLOCK_SIZE // 2
        color = NEON_CYAN if i == len(snake_list)-1 else (0, 150, 255)
        for r in range(3):
            pygame.draw.circle(dis, (*color, 50), (center_x, center_y), current_size + r*2)
        pygame.draw.circle(dis, color, (center_x, center_y), current_size)
        if i == len(snake_list)-1:
            pygame.draw.circle(dis, WHITE, (center_x - 5, center_y - 5), 3)
            pygame.draw.circle(dis, WHITE, (center_x + 5, center_y - 5), 3)

def welcome_screen():
    menu = True
    while menu:
        dis.fill(BG_DARK)
        title = font_menu.render("SNAKE ULTRA NEON", True, NEON_CYAN)
        start_msg = font_score.render("Press SPACE to Start", True, WHITE)
        quit_msg = font_score.render("Press Q to Quit", True, NEON_PINK)
        dis.blit(title, [WIDTH // 4, HEIGHT // 3])
        dis.blit(start_msg, [WIDTH // 3, HEIGHT // 2])
        dis.blit(quit_msg, [WIDTH // 3, HEIGHT // 2 + 50])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                    game_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def game_loop():
    game_over = False
    game_close = False
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0
    snake_list = []
    snake_len = 1
    score, level, speed = 0, 1, 12
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE

    while not game_over:
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0: dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0: dy, dx = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and dy == 0: dy, dx = BLOCK_SIZE, 0

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += dx
        y += dy
        dis.fill(BG_DARK)

        for i in range(0, WIDTH, BLOCK_SIZE * 2):
            pygame.draw.line(dis, (15, 15, 40), (i, 0), (i, HEIGHT))
        for i in range(0, HEIGHT, BLOCK_SIZE * 2):
            pygame.draw.line(dis, (15, 15, 40), (0, i), (WIDTH, i))

        pulse = abs(int(pygame.time.get_ticks() / 100 % 10 - 5))
        pygame.draw.circle(dis, NEON_PINK, (food_x + BLOCK_SIZE//2, food_y + BLOCK_SIZE//2), BLOCK_SIZE//2 - pulse)
        
        head = [x, y]
        snake_list.append(head)
        if len(snake_list) > snake_len:
            del snake_list[0]

        for seg in snake_list[:-1]:
            if seg == head:
                game_close = True

        draw_particles()
        draw_snake_pro(snake_list)
        
        score_txt = font_score.render(f"SCORE: {score} | LVL: {level}", True, NEON_CYAN)
        dis.blit(score_txt, [20, 20])

        pygame.display.update()

        if x == food_x and y == food_y:
            create_particles(food_x, food_y, NEON_PINK)
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE
            snake_len += 1
            score += 1
            if score % 3 == 0:
                level += 1
                speed += 2

        clock.tick(speed)

    pygame.quit()
    quit()

welcome_screen()