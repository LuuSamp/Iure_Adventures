import pygame

def load_image(path: str, size: tuple = None, *, alpha=False):
    image = pygame.image.load(path)
    if size is not None:
        image = pygame.transform.scale(image, size)
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image