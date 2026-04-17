import pygame

x = 300
y = 300
radius = 25
speed = 20

def move(key):
    global x, y

    if key == pygame.K_LEFT and x - speed - radius >= 0:
        x -= speed
    if key == pygame.K_RIGHT and x + speed + radius <= 600:
        x += speed
    if key == pygame.K_UP and y - speed - radius >= 0:
        y -= speed
    if key == pygame.K_DOWN and y + speed + radius <= 600:
        y += speed

def draw(screen):
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)