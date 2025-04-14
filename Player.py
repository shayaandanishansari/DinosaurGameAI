import pygame

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
        if settings.keyboard