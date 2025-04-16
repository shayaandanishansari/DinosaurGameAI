# game.py
import sys
import pygame
from Player import Player
import settings

def load_entity_images(entity_key):
    loaded_images_structured = []
    image_paths_list = settings.IMAGE_PATHS[entity_key]
    for idx, image_path_list in enumerate(image_paths_list):
        surfaces_for_state = []
        for path in image_path_list:
            surface = pygame.image.load(path).convert_alpha()
            if entity_key == "player" and idx == settings.PLAYER_AIR_IMAGE_INDEX:
                scale_factor = getattr(settings, 'PLAYER_AIR_IMAGE_SCALE_FACTOR', 1)
                if scale_factor != 1:
                    surface = pygame.transform.scale_by(surface, scale_factor)
            surfaces_for_state.append(surface)
        loaded_images_structured.append(surfaces_for_state)
    return loaded_images_structured

class Game:
    def __init__(self):
        pygame.display.set_caption("Dino AI Game")
        self.screen_surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.game_clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont(None, 30)
        self.is_running = True
        self.is_paused = False
        self.is_game_over = False
        self.BG_COLOR = settings.WHITE

        self.player_images_structured = load_entity_images("player")
        start_x = settings.PLAYER_START_X
        start_y = settings.GROUND_Y
        self.player_instance = Player(start_x, start_y, self.player_images_structured)
        self.all_sprites_group = pygame.sprite.Group()
        self.all_sprites_group.add(self.player_instance)

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
            self.all_sprites_group.update(delta_time)
            # Placeholder collision logic
            # obstacles = pygame.sprite.Group()
            # if pygame.sprite.spritecollide(self.player_instance, obstacles, False):
            #     self.player_instance.die()
            #     self.is_game_over = True

    def draw(self):
        self.screen_surface.fill(self.BG_COLOR)
        self.all_sprites_group.draw(self.screen_surface)

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

        pygame.display.flip()

    def reset_game(self):
         self.is_paused = False
         self.is_game_over = False
         self.all_sprites_group.empty()
         start_x = settings.PLAYER_START_X
         start_y = settings.GROUND_Y
         self.player_instance = Player(start_x, start_y, self.player_images_structured)
         self.all_sprites_group.add(self.player_instance)

    def run(self):
        while self.is_running:
            delta_time = self.game_clock.tick(60)
            self.handle_events()
            self.update(delta_time)
            self.draw()