import pygame as pg
from entity import Entity

class Player(Entity):
    def __init__(self, position):
        super().__init__(position)
        

    def move(self, direction):
        self.direction.x += self.x_vel*direction

    def jump(self):
        if self.on_ground:
            self.direction.y = -10
    
    def update(self):
        super().update()
        self.rect.x += self.direction.x

        if self.rect.bottomleft[1] < 200:
            self.on_ground = False
            self.gravity = 0.8
        else:
            self.on_ground = True
            self.gravity = 0
            self.direction.y = 0