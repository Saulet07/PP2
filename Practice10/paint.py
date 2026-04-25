import pygame
import sys

pygame.init()

W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint Pro Max")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)
RED = (255, 50, 50)
GREEN = (50, 200, 50)

canvas = pygame.Surface((W - 100, H))
canvas.fill(WHITE)

clock = pygame.time.Clock()
curr_color = BLACK
curr_shape = 'brush'
thickness = 5
drawing = False
start_pos = (0, 0)

def draw_sidebar():
    pygame.draw.rect(screen, GRAY, (0, 0, 100, H))
    pygame.draw.line(screen, BLACK, (100, 0), (100, H), 2)
    colors = [BLACK, RED, GREEN, BLUE]
    for i, col in enumerate(colors):
        pygame.draw.rect(screen, col, (25, 50 + i*60, 50, 50), border_radius=10)
        if curr_color == col:
            pygame.draw.rect(screen, WHITE, (25, 50 + i*60, 50, 50), 3, border_radius=10)
    
    font = pygame.font.SysFont("Arial", 12)
    labels = ["B-Brush", "R-Rect", "C-Circle", "E-Eraser"]
    for i, txt in enumerate(labels):
        lbl = font.render(txt, True, BLACK)
        screen.blit(lbl, (20, 300 + i*30))

def main():
    global curr_color, curr_shape, thickness, drawing, start_pos
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(GRAY)
        screen.blit(canvas, (100, 0))
        draw_sidebar()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[0] > 100:
                    drawing = True
                    start_pos = (mouse_pos[0] - 100, mouse_pos[1])
                else:
                    if 25 < mouse_pos[0] < 75:
                        if 50 < mouse_pos[1] < 100: curr_color = BLACK
                        elif 110 < mouse_pos[1] < 160: curr_color = RED
                        elif 170 < mouse_pos[1] < 220: curr_color = GREEN
                        elif 230 < mouse_pos[1] < 280: curr_color = BLUE

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = (mouse_pos[0] - 100, mouse_pos[1])
                    if curr_shape == 'rect':
                        pygame.draw.rect(canvas, curr_color, (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1])), thickness)
                    elif curr_shape == 'circle':
                        rad = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                        pygame.draw.circle(canvas, curr_color, start_pos, rad, thickness)
                    drawing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: curr_shape = 'brush'
                if event.key == pygame.K_r: curr_shape = 'rect'
                if event.key == pygame.K_c: curr_shape = 'circle'
                if event.key == pygame.K_e: curr_shape = 'eraser'

        if drawing and curr_shape == 'brush':
            pygame.draw.circle(canvas, curr_color, (mouse_pos[0] - 100, mouse_pos[1]), thickness)
        
        if drawing and curr_shape == 'eraser':
            pygame.draw.circle(canvas, WHITE, (mouse_pos[0] - 100, mouse_pos[1]), thickness * 2)

        if drawing and curr_shape in ['rect', 'circle']:
            end_p = (mouse_pos[0], mouse_pos[1])
            if curr_shape == 'rect':
                pygame.draw.rect(screen, curr_color, (min(start_pos[0]+100, end_p[0]), min(start_pos[1], end_p[1]), abs(end_p[0]-(start_pos[0]+100)), abs(end_p[1]-start_pos[1])), 1)
            elif curr_shape == 'circle':
                rad = int(((end_p[0]-(start_pos[0]+100))**2 + (end_p[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, curr_color, (start_pos[0]+100, start_pos[1]), rad, 1)

        pygame.display.flip()
        clock.tick(120)

main()