import sys
import pygame
from Player import Player
import settings
from HelperFunctions import load_images

pygame.init()

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
P = Player(40, 600, load_images(settings.images))

visible_sprites = pygame.sprite.Group()
visible_sprites.add(P)

Pause = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pygame.mouse.get_pressed()[0]:
        Pause = True

    if pygame.mouse.get_pressed()[2]:
        Pause = False

    if Pause == True:
        continue

    dt = clock.tick(60)

    screen.fill(0)

    P.update(dt)
    visible_sprites.draw(screen)

    pygame.display.flip()

if __name__ == '__main__':
    print("Hello World")