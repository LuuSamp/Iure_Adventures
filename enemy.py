import pygame as pg  
from entity import Entity

class Enemy(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.initial_pos = self.rect.x 
        self.image.fill("blue")

    def move(self):
        self.direction.x = self.x_vel*self.facing
        self.rect.x += self.direction.x

    def natural_sound(self):
        pass

    def to_die():
        pass

    def update(self):
        super().update()
        self.move()
        if self.rect.bottomleft[1] < 200:
            self.on_ground = False
            self.gravity = 0.8
        else:
            self.on_ground = True
            self.gravity = 0
            self.direction.y = 0

        if self.rect.left > 400:
            self.facing = -1
        elif self.rect.left < 200:
            self.facing = 1

        self.move()