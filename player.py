import pygame as pg
from entity import Entity
from os import path
from typing import Tuple

class Player(Entity):
    """
    Representa a entidade Player.

    Recebe herança da classe Entity e usa seus métodos padrões.
    """

    def __init__(self, position: Tuple[int]):
        """
        Inicializa o objeto Player. Carrega as imagens do jogador.

        Parâmetros:
            position (Tuple[int]): a posição inicial do jogador (x, y).
        """
        super().__init__(position)

        current_dir = path.dirname(path.abspath(__file__))
        media_dir = path.join(current_dir, "media")
        self.image_dir = path.join(media_dir, "player_images")
        self.sound_dir = path.join(media_dir, "sounds")

        self.walk_frames = [
            pg.image.load(path.join(self.image_dir, "walk", "player_walking_1.png")),
            pg.image.load(path.join(self.image_dir, "walk", "player_walking_2.png")),
            pg.image.load(path.join(self.image_dir, "walk", "player_walking_3.png"))
        ]
        self.standing_frame = pg.image.load(path.join(self.image_dir, "stand", "player_standing.png"))
        self.jump_frame = pg.image.load(path.join(self.image_dir, "jump", "player_jumping.png"))

        self.current_frame = 0
        self.animation_delay = 7
        self.animation_counter = 0

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

    def move(self, direction: int):
        """
        Move o Player na direção dada.

        Args:
            direction (int): A direção do movimento (-1 para esquerda, 1 para direita).
        """
        self.direction.x += self.x_vel * direction
        if self.direction.x != 0:
            self.facing = direction

    def jump(self):
        """
        Faz o Player pular se estiver no chão.
        """
        if self.on_ground:
            self.direction.y = self.jump_height
            pg.mixer.Sound(path.join(self.sound_dir, "jump_sound.mp3")).play()

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
                    enemy.die()
                    self.direction.y = -5
                else:
                    self.die()

    def update(self, square_group: pg.sprite.Group):
        """
        Atualiza o Player

        Parâmetros:
            square_group (pg.sprite.Group): O grupo de sprites Square.
        """
        super().update(square_group)
        self.rect.x += self.direction.x
        self.animation()

    def die(self):
        """
        Para a movimentação horizontal do jogador e o faz perder a colisão com os blocos.
        """
        self.direction.x = 0
        super().die()