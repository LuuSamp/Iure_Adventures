import pygame as pg
from entity import Entity
from os import path

class Player(Entity):
    def __init__(self, position):
        super().__init__(position)
        current_dir = path.dirname(path.abspath(__file__))
        media_dir = path.join(current_dir, "media", "player_images")
        self.walk_frames = [
            pg.image.load(path.join(media_dir, "walk", "player_walking_1.png")),
            pg.image.load(path.join(media_dir, "walk", "player_walking_2.png")),
            pg.image.load(path.join(media_dir, "walk", "player_walking_3.png"))
        ]
        self.standing_frame = pg.image.load(path.join(media_dir, "stand", "player_standing.png"))

        self.current_frame = 0 
        self.animation_delay = 7
        self.animation_counter = 0

    def animation(self):
        if self.direction.x == 0: 
            self.animation_counter = 1
            frame = pg.transform.scale(self.standing_frame, (self.rect.width, self.rect.height))
        else: 
            self.animation_counter -= 1

        
        #uma forma de ajustar um delay
        if self.animation_counter == 0:
            #muda de frame
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            
            #ajusta a imagem no tamanho do rect
            frame = pg.transform.scale(self.walk_frames[self.current_frame], (self.rect.width, self.rect.height))
            
            #reinicia a contagem
            self.animation_counter = self.animation_delay
        
        try:
            frame
        except:
            return
        
        #inverte a imagem se o movimento for para a esquerda
        if self.facing == -1:
            frame = pg.transform.flip(frame, True, False)
            self.image = frame

        #atualiza a imagem
        self.image = frame

    def move(self, direction):
        self.direction.x += self.x_vel*direction
        self.facing = direction

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
        self.animation()

    def die(self):
        self.direction.x = 0
        super().die()