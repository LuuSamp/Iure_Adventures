

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

    def apply_gravity(self):
        #vai aplicar a todas as entidades a gravidade, alterando a posição vertical
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    @abstractmethod
    def move(self):
        ...

    def update(self):
        self.apply_gravity()
        