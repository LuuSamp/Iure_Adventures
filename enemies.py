import pygame as pg  
from entity import Entity

class Enemies(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.initial_pos = self.rect.x 
        self.image.fill("blue")

    def move(self):
        pass

    def update(self):
        super().update()

        if self.rect.bottomleft[1] < 200:
            self.on_ground = False
            self.gravity = 0.8
        else:
            self.on_ground = True
            self.gravity = 0
            self.direction.y = 0

        if self.rect.left == 300:
            direction_a = 1

        elif self.rect.left == 354:
            direction_a = -1

        dir = direction_a

        self.direction.x = self.x_vel*dir
        self.rect.x += self.direction.x