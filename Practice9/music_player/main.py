import pygame
from player import play, stop, next_track, prev_track

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Music Player")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play()
            elif event.key == pygame.K_s:
                stop()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                prev_track()
            elif event.key == pygame.K_q:
                running = False

pygame.quit()