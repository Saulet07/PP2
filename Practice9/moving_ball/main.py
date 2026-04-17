import pygame
from ball import move, draw

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            move(event.key)

    draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()