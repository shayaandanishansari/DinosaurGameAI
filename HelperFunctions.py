import pygame

def load_images(images):
    loaded_images = []

    for image in images:
        image_list = []
        for i in image:
            image_list.append(pygame.image.load(i).convert_alpha())
        loaded_images.append(image_list)

    return loaded_images