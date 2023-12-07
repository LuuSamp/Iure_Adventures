from player import Player
import pygame as pg
from const import *
from os import path

class Shot(pg.sprite.Sprite):
    """
    classe criada para modelar o comportamento dos projéteis
    """

    def __init__(self, position:tuple) -> None: 
        """
        inicialização dos porjéteis

        Parâmetros
            position:
                type: tuple
                position: coordenadas de spawn do projétil
        """
        super().__init__()
        current_dir = path.dirname(path.abspath(__file__))
        media_dir = path.join(current_dir, "media")
        
        #configurando o som ao atirar o projétil
        self.sound = pg.mixer.Sound(path.join(media_dir, "sounds/shooting-sound-fx-159024.mp3"))
        self.sound.play()

        #atributos gerais
        self.x_vel = VEL_BULLET
        self.image = pg.image.load(path.join(media_dir, "bullet_images/B1.png"))
        self.image = pg.transform.scale(self.image, DIM_BULLET)
        self.rect = self.image.get_rect(topleft = position)
        self.initial_pos = self.rect.left

        #atributos que configuram  o movimento e a animação da bala
        self.direction = -1
        self.current_frame = 0
        self.animation_frames = [
            pg.image.load(path.join(media_dir, "bullet_images/B1.png")),
            pg.image.load(path.join(media_dir, "bullet_images/B2.png"))                                                 
        ]
        self.animation_counter = 0
        self.animation_delay = 15

    def animation(self) -> None:
        """
        gestão das animações dos projéteis
        """

        #atualiza as imagens do projétil levando em consideração um delay arbritário
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            frame = pg.transform.scale(self.animation_frames[self.current_frame], (self.rect.width, self.rect.height))
            self.image = frame
            self.animation_counter = 0

        self.animation_counter += 1
        

    def collide_with_player(self, player:Player) -> None:
        """
        veriricação da colisão com o jogador

        Parâmetros
            player:
                type: Player
                description: personagem jogável
        """

        #verifica se houve colisão e mata o player
        if pg.sprite.collide_rect(self, player):
            player.die()

    def update(self, player:Player, offset) -> None:
        """
        método de atualização

        Parâmetros
            player:
                type: Player
                description: personagem jogável
        """

        #movimento contínuo 
        self.rect.left += self.direction * self.x_vel + offset

        #range de atuação 
        if self.initial_pos + offset - self.rect.left > RANGE_BULLET:
            self.kill()
        
        #animação e colisão
        self.animation()
        self.collide_with_player(player)