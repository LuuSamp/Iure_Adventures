import pygame as pg
from player import Player
from const import *
from entity import Entity
import time

class Rect(pg.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y):
        super().__init__()
        self.image = pg.Surface((size_x, size_y))
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def update(self, shift):
        self.rect.x += shift
        
class Square(Rect):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)

class StaticSquare(Square):
    def __init__(self, x, y, size, image_path):
        super().__init__(x, y, size)
        image = pg.image.load(image_path)
        frame = pg.transform.scale(image, (size, size))
        self.image = frame


class ColisionSquare(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.timer = 3
        self._init_y = position[1]

    def move():
        pass

    def _reset_square(self):
        self.on_ground = True
        self.is_alive = True
        self.collision = True
        self.rect.y = self._init_y

    def update(self, square_group: pg.sprite.Group):
        self.collide_with_square(square_group)
        if pg.sprite.spritecollide(self, square_group):
            pass


