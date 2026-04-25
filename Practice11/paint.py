import pygame
import sys
import math

pygame.init()

# Window Setup
W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint Pro Max - Shapes Edition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)
RED = (255, 50, 50)
GREEN = (50, 200, 50)

# Main drawing surface
canvas = pygame.Surface((W - 100, H))
canvas.fill(WHITE)

clock = pygame.time.Clock()
curr_color = BLACK
curr_shape = 'brush'
thickness = 2
drawing = False
start_pos = (0, 0)

def draw_sidebar():
    """Draw the UI sidebar with color selection and instructions"""
    pygame.draw.rect(screen, GRAY, (0, 0, 100, H))
    pygame.draw.line(screen, BLACK, (100, 0), (100, H), 2)
    
    # Color squares
    colors = [BLACK, RED, GREEN, BLUE]
    for i, col in enumerate(colors):
        pygame.draw.rect(screen, col, (25, 30 + i*50, 50, 40), border_radius=5)
        if curr_color == col:
            pygame.draw.rect(screen, WHITE, (25, 30 + i*50, 50, 40), 3, border_radius=5)
    
    # Keybind Labels
    font = pygame.font.SysFont("Arial", 13)
    labels = [
        "B-Brush", "R-Rect", "C-Circle", "S-Square",
        "T-Right Tri", "U-Equi Tri", "H-Rhombus", "E-Eraser"
    ]
    for i, txt in enumerate(labels):
        lbl = font.render(txt, True, BLACK)
        screen.blit(lbl, (10, 250 + i*30))

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
                if mouse_pos[0] > 100: # Click on canvas
                    drawing = True
                    start_pos = (mouse_pos[0] - 100, mouse_pos[1])
                else: # Click on sidebar
                    if 25 < mouse_pos[0] < 75:
                        if 30 < mouse_pos[1] < 70: curr_color = BLACK
                        elif 80 < mouse_pos[1] < 120: curr_color = RED
                        elif 130 < mouse_pos[1] < 170: curr_color = GREEN
                        elif 180 < mouse_pos[1] < 220: curr_color = BLUE

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = (mouse_pos[0] - 100, mouse_pos[1])
                    w = end_pos[0] - start_pos[0]
                    h = end_pos[1] - start_pos[1]

                    # --- TASK: Drawing different shapes ---
                    if curr_shape == 'rect':
                        pygame.draw.rect(canvas, curr_color, (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), abs(w), abs(h)), thickness)
                    
                    elif curr_shape == 'square':
                        size = max(abs(w), abs(h))
                        pygame.draw.rect(canvas, curr_color, (start_pos[0], start_pos[1], size, size), thickness)
                    
                    elif curr_shape == 'circle':
                        rad = int((w**2 + h**2)**0.5)
                        pygame.draw.circle(canvas, curr_color, start_pos, rad, thickness)
                    
                    elif curr_shape == 'right_tri':
                        pts = [start_pos, (start_pos[0], end_pos[1]), end_pos]
                        pygame.draw.polygon(canvas, curr_color, pts, thickness)
                    
                    elif curr_shape == 'equi_tri':
                        # Height of equilateral triangle = side * sqrt(3)/2
                        side = w
                        height_tri = side * math.sqrt(3) / 2
                        pts = [start_pos, end_pos, (start_pos[0] + side/2, start_pos[1] - height_tri)]
                        pygame.draw.polygon(canvas, curr_color, pts, thickness)
                    
                    elif curr_shape == 'rhombus':
                        pts = [
                            (start_pos[0] + w/2, start_pos[1]),       # Top
                            (start_pos[0] + w, start_pos[1] + h/2),   # Right
                            (start_pos[0] + w/2, start_pos[1] + h),   # Bottom
                            (start_pos[0], start_pos[1] + h/2)        # Left
                        ]
                        pygame.draw.polygon(canvas, curr_color, pts, thickness)
                    
                    drawing = False

            # Handle keybinds for shape selection
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: curr_shape = 'brush'
                if event.key == pygame.K_r: curr_shape = 'rect'
                if event.key == pygame.K_c: curr_shape = 'circle'
                if event.key == pygame.K_s: curr_shape = 'square'
                if event.key == pygame.K_t: curr_shape = 'right_tri'
                if event.key == pygame.K_u: curr_shape = 'equi_tri'
                if event.key == pygame.K_h: curr_shape = 'rhombus'
                if event.key == pygame.K_e: curr_shape = 'eraser'

        # Continuous drawing for Brush/Eraser
        if drawing and curr_shape == 'brush':
            pygame.draw.circle(canvas, curr_color, (mouse_pos[0] - 100, mouse_pos[1]), 5)
        
        if drawing and curr_shape == 'eraser':
            pygame.draw.circle(canvas, WHITE, (mouse_pos[0] - 100, mouse_pos[1]), 20)

        pygame.display.flip()
        clock.tick(120)

main()