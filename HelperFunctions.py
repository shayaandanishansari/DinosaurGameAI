import settings
import pygame
import sys

def load_player_images(images):
    loaded_images = []
    for image_path_list in images: # Read paths from settings
        surface_list = []
        for path in image_path_list:
            surface_list.append(pygame.image.load(path).convert_alpha())
        loaded_images.append(surface_list)
    return loaded_images

