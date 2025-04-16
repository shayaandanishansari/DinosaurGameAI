# game.py
import sys
import pygame
import random
from Player import Player
from Environment import Cloud, Ground, Cactus, Bird # Import all from environment
import settings

class Game:
    def __init__(self):
        pygame.display.set_caption("Dino AI Game")
        self.screen_surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.game_clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont(None, 30)
        self.is_running = True
        self.is_paused = False
        self.is_game_over = False
        self.game_speed = settings.INITIAL_GAME_SPEED
        self.score = 0
        self.BG_COLOR = settings.WHITE

        self.load_assets()
        self.create_sprites()

        self.obstacle_spawn_timer = 0
        self.next_spawn_delay = self.get_random_spawn_delay()
        self.cloud_spawn_timer = 0 # Simple timer for clouds
        self.cloud_next_spawn_delay = random.randint(3000, 8000) # ms

    def load_assets(self):
        # Load Player images using the new structure
        player_images_structured = []
        player_paths = settings.IMAGE_PATHS["player"]
        for idx, path_list in enumerate(player_paths):
            surfaces = [pygame.image.load(p).convert_alpha() for p in path_list]
            # Apply scaling specifically to air image list
            if idx == settings.PLAYER_AIR_IMAGE_INDEX:
                 scale_factor = getattr(settings, 'PLAYER_AIR_IMAGE_SCALE_FACTOR', 1)
                 if scale_factor != 1 and surfaces: # Check list not empty
                      surfaces = [pygame.transform.scale_by(s, scale_factor) for s in surfaces]
            player_images_structured.append(surfaces)
        self.player_images_structured = player_images_structured

        # Load other assets
        self.cloud_image = pygame.image.load(settings.IMAGE_PATHS["cloud"][0]).convert_alpha()
        self.cloud_image = pygame.transform.scale_by(self.cloud_image, 4)
        self.ground_image = pygame.image.load(settings.IMAGE_PATHS["ground"][0]).convert_alpha()
        self.cactus_images = [pygame.image.load(p).convert_alpha() for p in settings.IMAGE_PATHS["cactus"]]
        self.bird_images = [pygame.image.load(p).convert_alpha() for p in settings.IMAGE_PATHS["bird"]]


    def create_sprites(self):
        start_x = settings.PLAYER_START_X
        start_y = settings.GROUND_Y

        # Sprite Groups
        self.all_sprites_group = pygame.sprite.Group()
        self.ground_group = pygame.sprite.Group()
        self.cloud_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()

        # Player
        self.player_instance = Player(start_x, start_y, self.player_images_structured)
        self.all_sprites_group.add(self.player_instance)

        # Ground (Create two for seamless scrolling)
        ground_y_pos = settings.GROUND_Y
        ground_width = self.ground_image.get_width()
        self.ground1 = Ground(0, ground_y_pos, self.ground_image)
        self.ground2 = Ground(ground_width, ground_y_pos, self.ground_image)
        self.ground_group.add(self.ground1, self.ground2)
        self.all_sprites_group.add(self.ground1, self.ground2)

        # Initial Clouds (optional)
        for _ in range(3):
            self.spawn_cloud()

    def spawn_cloud(self):
         cloud_y = random.randint(50, 200)
         # Spawn slightly off screen right
         new_cloud = Cloud(settings.SCREEN_WIDTH, cloud_y, self.cloud_image)
         self.cloud_group.add(new_cloud)
         self.all_sprites_group.add(new_cloud)

    def get_random_spawn_delay(self):
        return random.randint(settings.OBSTACLE_MIN_SPAWN_DELAY_MS,
                              settings.OBSTACLE_MAX_SPAWN_DELAY_MS)

    def spawn_obstacle(self):
        if random.random() < 0.7 and self.cactus_images: # 70% chance for cactus
            new_obstacle = Cactus(settings.SCREEN_WIDTH, settings.GROUND_Y, self.cactus_images)
        elif self.bird_images:
            new_obstacle = Bird(settings.SCREEN_WIDTH, self.bird_images)
        else: # Fallback if bird images missing
             if self.cactus_images:
                  new_obstacle = Cactus(settings.SCREEN_WIDTH, settings.GROUND_Y, self.cactus_images)
             else:
                  return # Cannot spawn anything

        self.obstacle_group.add(new_obstacle)
        self.all_sprites_group.add(new_obstacle)

    def handle_events(self):
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                self.is_running = False
            if game_event.type == pygame.KEYDOWN:
                if game_event.key == pygame.K_p:
                    if not self.is_game_over:
                        self.is_paused = not self.is_paused
                elif game_event.key == pygame.K_r and self.is_game_over:
                    self.reset_game()
                elif not self.is_paused and not self.is_game_over:
                    if game_event.key == pygame.K_SPACE:
                        self.player_instance.handle_jump_press()
                    elif game_event.key == pygame.K_DOWN:
                        self.player_instance.handle_duck_press()
            if game_event.type == pygame.KEYUP:
                if not self.is_paused and not self.is_game_over:
                    if game_event.key == pygame.K_SPACE:
                        self.player_instance.handle_jump_release()
                    elif game_event.key == pygame.K_DOWN:
                        self.player_instance.handle_duck_release()

    def update(self, delta_time):
        if not self.is_paused and not self.is_game_over:
            self.game_speed = min(settings.MAX_GAME_SPEED, self.game_speed + settings.SPEED_INCREASE_RATE * delta_time)
            self.score += delta_time * 0.01 # Example score increase

            # Update sprites, passing delta_time and game_speed
            self.all_sprites_group.update(delta_time, self.game_speed)

            # Ground tiling logic
            if self.ground1.rect.right <= 0:
                self.ground1.rect.left = self.ground2.rect.right
            if self.ground2.rect.right <= 0:
                self.ground2.rect.left = self.ground1.rect.right

            # Obstacle Spawning
            self.obstacle_spawn_timer += delta_time
            spawn_delay_adjusted = self.next_spawn_delay / (self.game_speed / settings.INITIAL_GAME_SPEED)
            if self.obstacle_spawn_timer >= spawn_delay_adjusted:
                self.obstacle_spawn_timer = 0
                self.spawn_obstacle()
                self.next_spawn_delay = self.get_random_spawn_delay()

            # Cloud Spawning
            self.cloud_spawn_timer += delta_time
            if self.cloud_spawn_timer >= self.cloud_next_spawn_delay:
                 self.spawn_cloud()
                 self.cloud_spawn_timer = 0
                 self.cloud_next_spawn_delay = random.randint(5000, 15000) # Longer delay between clouds

            # Collision Check
            collided_obstacles = pygame.sprite.spritecollide(self.player_instance, self.obstacle_group, False, pygame.sprite.collide_mask) # Mask collision better
            if collided_obstacles:
                self.player_instance.die()
                self.is_game_over = True

    def draw_ui(self):
        score_surf = self.game_font.render(f"Score: {int(self.score)}", True, settings.GRAY)
        score_rect = score_surf.get_rect(topright=(settings.SCREEN_WIDTH - 10, 10))
        self.screen_surface.blit(score_surf, score_rect)

        if self.is_paused:
            overlay_surface = pygame.Surface(self.screen_surface.get_size(), pygame.SRCALPHA)
            overlay_surface.fill((200, 200, 200, 180))
            self.screen_surface.blit(overlay_surface, (0,0))
            pause_text_surface = self.game_font.render("PAUSED", True, settings.BLACK)
            pause_text_rect = pause_text_surface.get_rect(center=self.screen_surface.get_rect().center)
            self.screen_surface.blit(pause_text_surface, pause_text_rect)
        elif self.is_game_over:
            overlay_surface = pygame.Surface(self.screen_surface.get_size(), pygame.SRCALPHA)
            overlay_surface.fill((100, 0, 0, 180))
            self.screen_surface.blit(overlay_surface, (0,0))
            game_over_text_surface = self.game_font.render("GAME OVER", True, settings.WHITE)
            game_over_text_rect = game_over_text_surface.get_rect(center=(self.screen_surface.get_rect().centerx, self.screen_surface.get_rect().centery - 20))
            self.screen_surface.blit(game_over_text_surface, game_over_text_rect)
            reset_text_surface = self.game_font.render("Press R to Restart", True, settings.WHITE)
            reset_text_rect = reset_text_surface.get_rect(center=(self.screen_surface.get_rect().centerx, self.screen_surface.get_rect().centery + 20))
            self.screen_surface.blit(reset_text_surface, reset_text_rect)

    def draw(self):
        self.screen_surface.fill(self.BG_COLOR)
        # Draw order matters if not using LayeredUpdates
        self.cloud_group.draw(self.screen_surface)
        self.ground_group.draw(self.screen_surface)
        self.obstacle_group.draw(self.screen_surface)
        self.all_sprites_group.draw(self.screen_surface) # Only draws player now if others drawn separately
        # Simpler: Draw all_sprites which contains everything in correct layers if added properly?
        # Let's stick to drawing groups separately for explicit layering control
        self.screen_surface.blit(self.player_instance.image, self.player_instance.rect) # Draw player last

        self.draw_ui()
        pygame.display.flip()

    def reset_game(self):
         self.is_paused = False
         self.is_game_over = False
         self.game_speed = settings.INITIAL_GAME_SPEED
         self.score = 0
         self.obstacle_spawn_timer = 0
         self.next_spawn_delay = self.get_random_spawn_delay()
         self.cloud_spawn_timer = 0
         self.cloud_next_spawn_delay = random.randint(3000, 8000)

         self.all_sprites_group.empty()
         self.ground_group.empty()
         self.cloud_group.empty()
         self.obstacle_group.empty()
         self.create_sprites()

    def run(self):
        while self.is_running:
            delta_time = self.game_clock.tick(60)
            self.handle_events()
            self.update(delta_time)
            self.draw()