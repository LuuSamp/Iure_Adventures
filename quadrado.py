import pygame

class Rect(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y):
        super().__init__()
        self.image = pygame.Surface((size_x, size_y))
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def update(self, shift):
        self.rect.x += shift
        
class Square(Rect):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)

class StaticSquare(Square):
    def __init__(self, x, y, size, image_path):
        super().__init__(x, y, size)
        image = pygame.image.load(image_path)
        frame = pygame.transform.scale(image, (size, size))
        self.image = frame
        