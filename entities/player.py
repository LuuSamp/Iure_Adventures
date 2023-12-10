import pygame as pg
from entities.entity import Entity
from os import path
from typing import Tuple
from const import *

class Player(Entity):
    """
    Representa a entidade Player.

    Recebe herança da classe Entity e usa seus métodos padrões.
    """

    def __init__(self, position: Tuple[int] = (0,0)):
        """
        Inicializa o objeto Player. Carrega as imagens do jogador.

        Parâmetros:
            position (Tuple[int]): a posição inicial do jogador (x, y).
        """
        super().__init__(position)

        current_dir = path.dirname(path.abspath(__file__))
        media_dir = path.join(current_dir, "..", "media")
        self.image_dir = path.join(media_dir, "player_images")
        self.sound_dir = path.join(media_dir, "sounds")

        self.walk_frames = [
            pg.image.load(path.join(self.image_dir, "walk", "player_walking_1.png")),
            pg.image.load(path.join(self.image_dir, "walk", "player_walking_2.png")),
            pg.image.load(path.join(self.image_dir, "walk", "player_walking_3.png")),
            pg.image.load(path.join(self.image_dir, "walk", "player_walking_4.png"))
        ]
        self.standing_frame = pg.image.load(path.join(self.image_dir, "stand", "player_standing.png"))
        self.jump_frame = pg.image.load(path.join(self.image_dir, "jump", "player_jumping.png"))

        self.x_vel = PLAYER_X_VEL
        self.jump_height = PLAYER_Y_VEL
        self.current_frame = 0
        self.animation_delay = 2
        self.animation_counter = 0
        self._coin_count = 0
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, "jump_sound.mp3"))
        self.jump_sound.set_volume(0.2)

        self.won = False

    def reset(self):
        self.__init__()

    @property
    def coin_count(self) -> int:
        return self._coin_count
    
    @coin_count.setter
    def coin_count(self, new_coin_count) -> None:
        self._coin_count = new_coin_count
    
    def add_coin(self) -> None:
        self.coin_count += 1

    def animation(self):
        """
        Seleciona a imagem do jogador baseado no seu movimento.
        """
        if not self.on_ground:
            self.animation_counter = 1
            frame = pg.transform.scale(self.jump_frame, (self.rect.width, self.rect.height))

        elif self.direction.x == 0:
            self.animation_counter = 1
            frame = pg.transform.scale(self.standing_frame, (self.rect.width, self.rect.height))

        else:
            self.animation_counter -= 1

        if self.animation_counter == 0:
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            frame = pg.transform.scale(self.walk_frames[self.current_frame], (self.rect.width, self.rect.height))
            self.animation_counter = self.animation_delay

        try:
            frame
        except:
            return

        if self.facing == -1:
            frame = pg.transform.flip(frame, True, False)
            self.image = frame

        self.image = frame

    def move(self, direction: int = 0):
        """
        Move o Player na direção dada.

        Args:
            direction (int): A direção do movimento (-1 para esquerda, 1 para direita).
        """
        self.direction.x = self.x_vel * direction
        if self.direction.x != 0:
            self.facing = direction

    def jump(self):
        """
        Faz o Player pular se estiver no chão.
        """
        if self.on_ground:
            self.direction.y = self.jump_height
            self.jump_sound.play()


    def collide_with_enemy(self, enemy_group: pg.sprite.Group):
        """
        Detecta colisão com o inimigo. 
        Se o Player colidir acima do inimigo, mata o inimigo. 
        Caso contrário, mata o Player

        Parâmetros:
            enemy_group (pg.sprite.Group): O grupo de sprites Enemy
        """
        if self.collision == False: return
        for enemy in pg.sprite.spritecollide(self, enemy_group, False):
            if enemy.collision == False: continue
            if pg.sprite.collide_rect(self, enemy):
                if (enemy.rect.collidepoint(self.rect.bottomright) or
                        enemy.rect.collidepoint(self.rect.midbottom) or
                        enemy.rect.collidepoint(self.rect.bottomleft)):
                    self.direction.y = -5
                    enemy.die()
                else:
                    self.die()

    def update(self, square_group: pg.sprite.Group, offset):
        """
        Atualiza o Player

        Parâmetros:
            square_group (pg.sprite.Group): O grupo de sprites Square.
        """
        super().update(square_group, offset)
        self.rect.x += self.direction.x
        self.animation()
        self.move()

    def die(self):
        """
        Para a movimentação horizontal do jogador e o faz perder a colisão com os blocos.
        """
        self.direction.x = 0
        super().die()