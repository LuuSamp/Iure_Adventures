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

class ColisionSquare(StaticSquare):
    def __init__(self, x, y, size, image_path, player: Player):
        super().__init__(x, y, size, image_path)
        self.player = player
        self.speed_y = 0
        self.gravity = GRAVITY
        self.collision = True
        self.init_y = y
        self.cooldown = 0

    def _player_collision(self) -> bool:
        if self.collision == False:
            return False
        elif self.player.rect.right >= self.rect.left and self.player.rect.left <= self.rect.right and self.player.rect.bottom == self.rect.top:
            return True
        else:
            return False

    def fall(self) -> None:
        self.speed_y = 4
        self.rect.y += self.speed_y

    def _reset_block(self):
        self.rect.y = self.init_y
    
    def update(self, shift):
        self.rect.x += shift

        if self._player_collision() == True:
            self.cooldown += 1
        if self.cooldown >= FPS * 2:
            self.fall()
        elif self.cooldown > 0:
            self.cooldown += 1