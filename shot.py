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

class BossShot(pg.sprite.Sprite):
    """
    """

    def __init__(self, position:tuple, player:Player, vector_player:pg.math.Vector2, explosion:pg.sprite.Group) -> None:
        """
        """

        super().__init__()

        #configurando os paths
        current_dir = path.dirname(path.abspath(__file__))
        media_dir = path.join(current_dir, "media")

        #atributos gerais
        self.vector_player = vector_player
        self.shot_vel = 10
        self.image = pg.Surface((30, 30))
        self.image = pg.transform.scale(pg.image.load("media/fireball0.png"), (30, 30))
        self.rect = self.image.get_rect(topleft=position)
        self.explosion = explosion
        self.sound = pg.mixer.Sound("media\sounds\shooting-sound-fx-159024.mp3")
        self.sound.play()

    def animation(self) -> None:
        """
        """

    def move(self) -> None:
        """
        """
        self.rect.x -= (self.vector_player.x) * (self.shot_vel)
        self.rect.y -= (self.vector_player.y) * (self.shot_vel)

    def collide_with_player(self, player:Player) -> None:
        """
        """
        #verifica se houve colisão e mata o player
        if pg.sprite.collide_rect(self, player):
            self.explosion.add(Explosion((self.rect.center[0], self.rect.center[1])))
            player.die()
            self.kill()

    def update(self, player:Player, offset:int) -> None:
        """
        """
        self.rect.x += offset

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

        self.move()
        self.collide_with_player(player)

class Explosion(pg.sprite.Sprite):
    """
    """

    def __init__(self, position:tuple) -> None:
        super().__init__()

        current_dir = path.dirname(path.abspath(__file__))
        media_dir = path.join(current_dir, "media")

        self.image = pg.Surface((120, 120))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=position)

        self.frames = [pg.image.load(path.join(media_dir, "explosion_images/S_1.png")),
                       pg.image.load(path.join(media_dir, "explosion_images/S_2.png")),
                       pg.image.load(path.join(media_dir, "explosion_images/S_3.png")),
                       pg.image.load(path.join(media_dir, "explosion_images/S_4.png"))]
        
        self.explosion_counter = 0

    def animation(self):
        """
        """
        if self.explosion_counter < 8:
            frame = 0
        elif self.explosion_counter < 16:
            frame = 1
        elif self.explosion_counter < 24:
            frame = 2
        elif self.explosion_counter < 32:
            frame = 3
        else:
            self.kill()
        try:
            self.image = pg.transform.scale(self.frames[frame], (120, 120))
            self.explosion_counter += 1
        except:
            return
        
    def update(self):
        self.animation()