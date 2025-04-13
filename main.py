import pygame

pygame.init()

screen = pygame.display.set_mode()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if pygame.event.type == pygame.QUIT:
            pygame.quit()
    clock.tick(60)

if __name__ == '__main__':
    print("Hello World")