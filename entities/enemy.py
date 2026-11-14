import pygame as pg  
from entities.entity import Entity
from entities.shot import Shot
from game.const import *
from game.helpers import load_image
from game.resource import resource_path

from os import path

class Enemy(Entity):
    """
    classe criada para modelar o comportamento dos inimigos simples 
    """

    def __init__(self, position:tuple) -> None:
        """
        inicialização dos inimigos simples

        Parâmetros
            position:
                type: tuple
                position: coordenadas de spawn do inimigo
        """

        #atributos padrões de entidades
        super().__init__(position)
        self.media_dir = resource_path("media")
        

        #atributos iniciais
        self.initial_pos = self.rect.left
        self.x_vel = VEL_ENEMY_DEFAULT

        # morte
        frame_size = (self.rect.width, self.rect.height)
        self.death_image = load_image(
            path.join(self.media_dir, "enemy_images/enemy3.png"), frame_size, alpha=True
        )
        
        #som padrão
        self.death_sound = pg.mixer.Sound(path.join(self.media_dir, "sounds/pixel-death-66829.mp3"))
        self.death_sound.set_volume(0.5)

        #atributos de animação
        self.walk_frames = [
            load_image(path.join(self.media_dir, "enemy_images/enemy0.png"), frame_size, alpha=True),
            load_image(path.join(self.media_dir, "enemy_images/enemy1.png"), frame_size, alpha=True),
            load_image(path.join(self.media_dir, "enemy_images/enemy2.png"), frame_size, alpha=True),
        ]
        self.current_frame = 0 
        self.animation_delay = 7
        self.animation_counter = 7

    def animation(self) -> None:
        """
        gestão das animações dos inimigos simples (animação horizontal)
        """
        
        self.animation_counter += 1
        
        #atualiza a imagem com base na direção, mas levando em conta um delay arbritário
        if self.animation_counter >= self.animation_delay and self.x_vel != 0 and self.is_alive:
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            frame = self.walk_frames[self.current_frame]
            #inverte a imagem se o movimento for para a esquerda
            if self.facing == -1:
                frame = pg.transform.flip(frame, True, False)
            self.image = frame
            self.animation_counter = 0

        #caso o inimigo morra, a imagem dele muda
        if not self.is_alive:
            self._death_animation()
            
    def _death_animation(self) -> None:
        """
        animação de morte do inimigo simples
        """
        frame = self.death_image
        frame = pg.transform.flip(frame, True, False)
        self.image = frame

    def move(self) -> None:
        """
        modelagem do movimento dos inimigos
        """

        #muda a posição dele com base na velocidade e na direção do inimigo
        self.direction.x = self.x_vel*self.facing
        self.rect.x += self.direction.x

    def natural_sound(self) -> None:
        """
        modelagem do som padrão dos inimigos simples
        """

        #configuração e ativação do som
        self.sound.set_volume(0.2)
        self.sound.play()

    def die(self) -> None:
        """
        modelagem da morte do inimigo simples
        """

        #configuração do som de "morte"
        self.death_sound.play()

        super().die()

    def update(self, square_group:pg.sprite.Group, offset) -> None:
        """
        método de atualização

        Parâmetros
            square_group:
                type: pg.sprite.Group
                description: sprites do cenário para verificação da colisão
        """
        super().update(square_group, offset)
        self.initial_pos += offset
        
        #movimento contínuo do inimigo delimitado por uma range
        if self.rect.right > self.initial_pos + RANGE_ENEMY_DEFAULT:
            self.facing = -1
        elif self.rect.left < self.initial_pos - RANGE_ENEMY_DEFAULT:
            self.facing = 1

        #moviemnto e animação
        self.move()
        self.animation()
            

class EnemyShooter(Enemy):
    """
    classe criada para modelar o comportamento dos inimigos que atiram
    """

    def __init__(self, position:tuple, shots:pg.sprite.Group) -> None:
        """
        inicialização dos inimigos que atiram

        Parâmetros
            position:
                type: tuple
                position: coordenadas de spawn do inimigo
        """

        super().__init__(position)
        self.media_dir = resource_path("media")

        #atributos de animação e de lançamento de projéteis
        self.shots = shots

        self.jump_counter = 0
        self.jump_delay = 50

        self.shot_counter = 0
        self.shot_delay = 60

        frame_size = (self.rect.width, self.rect.height)
        self.walk_frames = [
            load_image(path.join(self.media_dir, "enemy_shooter_images/enemy_shooter0.png"), frame_size, alpha=True),
            load_image(path.join(self.media_dir, "enemy_shooter_images/enemy_shooter1.png"), frame_size, alpha=True),
            load_image(path.join(self.media_dir, "enemy_shooter_images/enemy_shooter2.png"), frame_size, alpha=True),
            load_image(path.join(self.media_dir, "enemy_shooter_images/enemy_shooter3.png"), frame_size, alpha=True),
            load_image(path.join(self.media_dir, "enemy_shooter_images/enemy_shooter4.png"), frame_size, alpha=True),
            load_image(path.join(self.media_dir, "enemy_shooter_images/enemy_shooter5.png"), frame_size, alpha=True),
        ]

        self.death_image = load_image(
            path.join(self.media_dir, "enemy_shooter_images/enemy_shooter6.png"),
            frame_size,
            alpha=True,
        )

    def move(self) -> None:
        """
        modelagem do movimento dos inimigos
        """

        #controla os pulos automáticos levando em consideração um delay arbritário
        if self.on_ground and self.jump_counter >= self.jump_delay:
            self.direction.y = JUMP_HEIGHT
            self.jump_counter = 0
        self.jump_counter +=1

    def animation(self) -> None:
        """
        gestão das animações dos inimigos simples (animação vertical)
        """

        #modelagem dos projéteis levando em conta um delay
        self.shot_counter +=1
        if self.shot_counter >= self.shot_delay and self.is_alive:
            self.shots.add(Shot((self.rect.x, self.rect.center[1])))
            self.shot_counter = 0
        
        #modelagem das animações (caso esteja vivo)
        if self.is_alive:
            if self.on_ground == True and self.shot_counter == 0:
                self.current_frame = 2
            
            elif self.on_ground == True and self.shot_counter > 0 and self.shot_counter <= 25:
                self.current_frame = 0

            elif self.on_ground == True and self.shot_counter > 3 and self.shot_counter >= self.animation_delay:
                self.current_frame = 1

            if self.on_ground == False and self.shot_counter == 0:
                self.current_frame = 5
            
            elif self.on_ground == False and self.shot_counter > 0 and self.shot_counter <= 20:
                self.current_frame = 3

            elif self.on_ground == False and self.shot_counter > 3 and self.shot_counter >= self.animation_delay:
                self.current_frame = 4

            frame = self.walk_frames[self.current_frame]
            
            self.image = frame

        #modelagem das animações (caso esteja morto)
        else:
            self._death_animation()
