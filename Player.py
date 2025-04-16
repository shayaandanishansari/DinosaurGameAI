import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()

        self.x = x
        self.y = y

        self.default_position = (x, y)

        self.running_images = images[0]
        self.jumping_images = images[1]
        self.ducking_images = images[2]

        self.running = True
        self.jumping = False
        self.ducking = False

        self.start_jump = 0
        self.jump_duration = 0

        self.image = self.running_images[0]
        print(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        print(self.rect.bottomleft)

        self.velocity = 1
        self.current_image_index = 0

    def input_handling(self):
        keyboard = pygame.key.get_pressed()

        # 1. JUMPING
        # Pressed Spacebar
        if keyboard[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.running = False
            self.start_jump = pygame.time.get_ticks()
        # Holding Spacebar
        elif self.jumping and keyboard[pygame.K_SPACE]:
            self.jump_duration = pygame.time.get_ticks() - self.start_jump
        # Left Spacebar or Timeout
        elif self.jumping and not keyboard[pygame.K_SPACE] or self.jump_duration > settings.max_jump_time:
            self.jumping = False
            self.running = False
            self.jump_duration = 0

        # 2. DUCKING
        # Pressing Down Key
        if keyboard[pygame.K_DOWN] and not self.ducking:
            self.ducking = True
            self.jumping = False
            self.running = False
        # Left Down Key
        elif not keyboard[pygame.K_DOWN] and self.ducking:
            self.ducking = False

        # 3. RUNNING
        if self.rect.bottomleft == self.default_position:
            self.running = True


    def movement(self, dt):
        # 1. JUMPING UP
        if self.jumping:
            self.y -= self.velocity
        if not self.jumping and self.rect.bottomleft > self.default_position:
            self.x += self.velocity
            if self.ducking:
                self.y += self.velocity * 2

        # 2. DUCKING DOWN

        # 2. RUNNING
        # No special movement only animation

    def animation(self, dt):
        if self.jumping:
            self.current_image_index = 0
            self.rect = self.jumping_images[self.current_image_index].get_rect()
            self.rect.bottomleft = (self.x, self.y)

        elif self.ducking:
            self.rect = self.ducking_images[self.current_image_index].get_rect()
            self.current_image_index = (self.current_image_index + 1) % len(self.ducking_images)
            self.rect.bottomleft = (self.x, self.y)

        elif self.running:
            self.rect = self.running_images[self.current_image_index].get_rect()
            self.current_image_index = (self.current_image_index + 1) % len(self.running_images)
            self.rect.bottomleft = self.default_position


    def update(self, dt):
        self.input_handling()
        self.movement(dt)
        self.animation(dt)

        print(f"Running:{self.running}\nJumping:{self.jumping}\nDucking:{self.ducking}\n\n")
