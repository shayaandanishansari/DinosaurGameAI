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

        self.start_jump = 0
        self.jump_duration = 0

        self.image = self.run_images[self.current_image_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = y

    def movement(self):
        # For later: if settings.keyboard
        keyboard = settings.keyboard
        start_jump = 0
        end_jump = 0

        # JUMPING
        # Pressed Jump
        if keyboard["spacebar"] and not self.jumping:
            self.jumping = True
            self.start_jump = pygame.time.get_ticks()
        # Holding Jump
        elif self.jumping and keyboard["spacebar"]:
            self.jump_duration = pygame.time.get_ticks() - self.start_jump
        elif self.jumping and keyboard["spacebar"] and self.jump_duration < settings.max_jump_time:
            self.jumping = False
            self.jump_duration = 0

        if keyboard["down"]:
            # duck
            ...
        else:
            # running
            ...


    def update(self):
        self.movement()