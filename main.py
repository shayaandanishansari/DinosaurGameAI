import sys

import pygame
pygame.init()

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)

if __name__ == '__main__':
    print("Hello World")