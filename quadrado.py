import pygame as pg
from player import Player
from const import *
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


class TimerSquare(StaticSquare):
    def __init__(self, x, y, size, image_path):
        super().__init__(x, y, size, image_path)
        self.timer = 3
        self.gravity = GRAVITY
        self.direction = pg.math.Vector2(0, 0)
        self.init_x = x
        self.init_y = y


    def apply_gravity(self) -> None:
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    def collide_with_player(self, player:Player) -> None:
        if pg.sprite.collide_rect(self, player):
            return True
        else:
            return False


    def update(self, player:Player) -> None:
        if self.collide_with_player(player=player):
            time.sleep(self.timer)

            start_time = time.time()
            while time.time() - start_time <= 5:
                self.apply_gravity()
            
            self.rect.x = self.init_x 
            self.rect.y = self.init_y

