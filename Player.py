import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images_structured):
        super().__init__()

        self.run_images = images_structured[settings.PLAYER_RUN_IMAGES_INDEX]
        self.jump_images = images_structured[settings.PLAYER_JUMP_IMAGES_INDEX]
        self.ducking_images = images_structured[settings.PLAYER_DUCK_IMAGES_INDEX]
        self.air_image = images_structured[settings.PLAYER_AIR_IMAGE_INDEX][0]
        self.dead_image = images_structured[settings.PLAYER_DEAD_IMAGE_INDEX][0]

        self.jumping = False
        self.ducking = False
        self._on_ground = True
        self._playing_jump_anim = False
        self.is_alive = True
        self._down_key_held = False

        self.current_run_index = 0
        self.current_jump_index = 0
        self.current_duck_index = 0
        self.anim_timer = 0
        self.animation_speed = settings.ANIMATION_SPEED

        self.image = self.run_images[self.current_run_index]
        self.rect = self.image.get_rect()
        self.ground_y = y
        self.rect.bottomleft = (x, y)
        self.y_velocity = 0
        self.gravity = settings.GRAVITY
        self.jump_power = settings.JUMP_POWER
        self.jump_cut_factor = settings.JUMP_CUT_FACTOR
        self.fast_fall_multiplier = getattr(settings, 'FAST_FALL_MULTIPLIER', 3)

        self.stand_rect_ref = self.run_images[0].get_rect()
        self.duck_rect_ref = self.ducking_images[0].get_rect()

    def handle_jump_press(self):
        if self._on_ground and not self.ducking and self.is_alive:
            self.y_velocity = self.jump_power
            self.jumping = True
            self._on_ground = False
            if self.jump_images:
                self._playing_jump_anim = True
                self.current_jump_index = 0

    def handle_jump_release(self):
        if self.jumping and self.y_velocity < 0:
            self.y_velocity *= self.jump_cut_factor

    def handle_duck_press(self):
        self._down_key_held = True
        #
        if self.is_alive:
             self.ducking = True
             if self.jumping:
                  self._playing_jump_anim = False
        # --- End CHANGE 1 ---

    def handle_duck_release(self):
        self._down_key_held = False
        self.ducking = False

    def apply_physics(self, delta_time):
        if not self._on_ground:
            if self._down_key_held:
                self.y_velocity += self.gravity * self.fast_fall_multiplier
            else:
                self.y_velocity += self.gravity

        self.rect.y += self.y_velocity

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.y_velocity = 0
            if self.jumping:
                self.jumping = False
            self._on_ground = True
            self._playing_jump_anim = False
        else:
            self._on_ground = False

    def update_animation(self, delta_time):
        old_bottomleft = self.rect.bottomleft
        target_image = self.image

        self.anim_timer += delta_time
        run_anim_this_frame = self.anim_timer >= self.animation_speed

        if run_anim_this_frame:
            self.anim_timer %= self.animation_speed

        if not self.is_alive:
            target_image = self.dead_image
        # --- CHANGE 2: Check ducking state FIRST, regardless of ground ---
        elif self.ducking: # Show ducking anim if ducking flag is set
            if self.ducking_images:
                if run_anim_this_frame:
                    self.current_duck_index = (self.current_duck_index + 1) % len(self.ducking_images)
                target_image = self.ducking_images[self.current_duck_index]
        # --- End CHANGE 2 ---
        elif self.jumping or not self._on_ground: # Airborne (and NOT ducking)
            if self._playing_jump_anim and self.jump_images:
                if run_anim_this_frame:
                    self.current_jump_index += 1
                if self.current_jump_index >= len(self.jump_images):
                    self._playing_jump_anim = False
                    target_image = self.air_image
                else:
                    target_image = self.jump_images[self.current_jump_index]
            else:
                target_image = self.air_image
        else: # Running (on ground, not ducking)
            if self.run_images:
                if run_anim_this_frame:
                    self.current_run_index = (self.current_run_index + 1) % len(self.run_images)
                target_image = self.run_images[self.current_run_index]

        if self.image is not target_image:
            self.image = target_image
            new_rect = self.image.get_rect()
            self.rect.size = new_rect.size
            self.rect.bottomleft = old_bottomleft
        elif self.rect.size != self.image.get_rect().size:
            new_rect = self.image.get_rect()
            self.rect.size = new_rect.size
            self.rect.bottomleft = old_bottomleft

    def die(self):
        if self.is_alive:
            self.is_alive = False

    def update(self, delta_time, game_speed):
        if self.is_alive:
            self.apply_physics(delta_time)
        self.update_animation(delta_time)