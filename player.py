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
    
    def collide_with_enemy(self, enemy_group: pg.sprite.Group):
        for enemy in pg.sprite.spritecollide(self, enemy_group, False):
            if pg.sprite.collide_rect(self, enemy):
                if (enemy.rect.collidepoint(self.rect.bottomright) or 
                enemy.rect.collidepoint(self.rect.midbottom) or
                enemy.rect.collidepoint(self.rect.bottomleft)):
                    enemy.kill()
                else:
                    self.kill()

    def update(self):
        super().update()
        self.rect.x += self.direction.x