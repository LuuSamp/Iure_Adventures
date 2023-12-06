import pygame as pg
from entity import Entity
from os import path

class Player(Entity):
    def __init__(self, position):
        super().__init__(position)
        current_dir = path.dirname(path.abspath(__file__))
        

    def move(self, direction):
        self.direction.x += self.x_vel*direction

    def jump(self):
        if self.on_ground:
            self.direction.y = -10
    
    def collide_with_enemy(self, enemy_group: pg.sprite.Group):
        for enemy in pg.sprite.spritecollide(self, enemy_group, False):
            if pg.sprite.collide_rect(self, enemy):
                if (enemy.rect.collidepoint(self.rect.bottomright) or 
                enemy.rect.collidepoint(self.rect.midbottom) or
                enemy.rect.collidepoint(self.rect.bottomleft)):
                    enemy.die()
                    self.direction.y = -5
                else:
                    self.die()

    def update(self, square_group: pg.sprite.Group):
        super().update(square_group)
        self.rect.x += self.direction.x

    def die(self):
        self.direction.x = 0
        super().die()