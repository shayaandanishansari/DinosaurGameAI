import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()

        self.coordinates = (x, y)

        self.running_images = images[0]
        self.running_images = images[1]
        self.running_images = images[2]

        self.running = True
        self.jumping = False
        self.ducking = False

        self.image = self.run_images[self.current_image_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = y

    def movement(self):
        # For later: if settings.keyboard
        keyboard = settings.keyboard
        start_jump = 0
        end_jump = 0

        if keyboard["spacebar"]:
            start_jump = pygame.time.get_ticks()
        else:
            end_jump = pygame.time.get_ticks() - start_jump

        if keyboard["down"]:
            # duck
            ...
        else:
            # running
            ...


    def update(self):
        self.movement()