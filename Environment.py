import pygame
import settings
import random

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_factor = settings.CLOUD_SPEED_FACTOR

    def update(self, delta_time, game_speed):
        self.rect.x -= game_speed * self.speed_factor
        if self.rect.right < -100:
            self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_factor = settings.GROUND_SPEED_FACTOR

    def update(self, delta_time, game_speed):
        self.rect.x -= game_speed * self.speed_factor

class Cactus(pygame.sprite.Sprite):
    def __init__(self, screen_width, ground_y, images):
        super().__init__()
        self.image = random.choice(images)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (screen_width, ground_y)
        self.speed_factor = settings.CACTUS_SPEED_FACTOR

    def update(self, delta_time, game_speed):
        self.rect.x -= game_speed * self.speed_factor
        if self.rect.right < 0:
            self.kill()

class Bird(pygame.sprite.Sprite):
    def __init__(self, screen_width, images):
        super().__init__()
        self.images = images
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect()
        self.anim_timer = 0
        self.animation_speed = settings.BIRD_ANIMATION_SPEED

        flight_level = random.choice([settings.BIRD_FLY_HIGH_Y, settings.BIRD_FLY_LOW_Y])
        self.rect.bottomleft = (screen_width, flight_level)
        self.speed_factor = settings.BIRD_SPEED_FACTOR

    def update_animation(self, delta_time):
        old_center = self.rect.center
        self.anim_timer += delta_time
        if self.anim_timer >= self.animation_speed:
            self.anim_timer %= self.animation_speed
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.image = self.images[self.current_image_index]
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self, delta_time, game_speed):
        self.update_animation(delta_time)
        self.rect.x -= game_speed * self.speed_factor
        if self.rect.right < 0:
            self.kill()