import pygame
import os
from clock import get_time_angles

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(__file__)
hand_img = pygame.image.load(
    os.path.join(BASE_DIR, "images", "mickey_hand.png")
)
hand_img = pygame.transform.scale(hand_img, (200, 200))

center = (WIDTH // 2, HEIGHT // 2)

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    minute_angle, second_angle = get_time_angles()

    minute_hand = pygame.transform.rotate(hand_img, -minute_angle)
    second_hand = pygame.transform.rotate(hand_img, -second_angle)

    rect1 = minute_hand.get_rect(center=center)
    rect2 = second_hand.get_rect(center=center)

    screen.blit(minute_hand, rect1)
    screen.blit(second_hand, rect2)

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()