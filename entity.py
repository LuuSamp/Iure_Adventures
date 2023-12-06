

import pygame as pg  
from const import *
from abc import ABC, abstractmethod

class Entity(ABC, pg.sprite.Sprite):
    """
    """

    def __init__(self, position):
        """
        """
        super().__init__()
        self.image = pg.Surface((32,64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)
        self.facing = 1

        #movimento da entidade
        self.direction = pg.math.Vector2(0, 0)
        self.gravity = GRAVITY
        self.x_vel = ENTITY_X_VEL

        self.on_ground = True
        self.alive = True
        self.move_direction = 0
        self.collision = True

    def apply_gravity(self):
        #vai aplicar a todas as entidades a gravidade, alterando a posição vertical
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    @abstractmethod
    def move(self):
        ...

    def update(self):
        self.apply_gravity()
        if self.rect.top > 600: self.kill()
    
    def collide_with_square(self, square_group: pg.sprite.Group):
        self.on_ground = False

        if not self.collision: return 
        
        for square in pg.sprite.spritecollide(self, square_group, False):
            if self.direction.y + 3 > 0 and self.rect.bottom - self.direction.y - 1 < square.rect.top: 
                self.rect.bottom = square.rect.top
                self.direction.y = 0
                self.on_ground = True

            if self.direction.y < 0: 
                self.rect.top = square.rect.bottom
                self.direction.y = 0

        for square in pg.sprite.spritecollide(self, square_group, False):
            if self.direction.x > 0: 
                self.rect.right = square.rect.left
            if self.direction.x < 0: 
                self.rect.left = square.rect.right
    
    def die(self):
        self.collision = False
        self.x_vel = 0