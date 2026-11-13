import pygame

_image_cache = {}


def load_image(path: str, size: tuple = None, *, alpha=False):
    key = (path, size, alpha)
    if key in _image_cache:
        return _image_cache[key]
    image = pygame.image.load(path)
    if size is not None:
        image = pygame.transform.scale(image, size)
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    _image_cache[key] = image
    return image