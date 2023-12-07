import pygame as pg  
from entity import Entity
from shot import Shot
from const import * 
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
        self.current_dir = path.dirname(path.abspath(__file__))
        self.media_dir = path.join(self.current_dir, "media")

        #atributos iniciais
        self.initial_pos = self.rect.left
        self.x_vel = VEL_ENEMY_DEFAULT

        #som padrão
        self.sound = pg.mixer.Sound(path.join(self.media_dir, "sounds/monster-death-grunt-131480.mp3"))

        #atributos de animação
        self.walk_frames = [
            pg.image.load(path.join(self.media_dir, "enemy_images/1.png")),
            pg.image.load(path.join(self.media_dir, "enemy_images/2.png")),
            pg.image.load(path.join(self.media_dir, "enemy_images/3.png"))
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
            frame = pg.transform.scale(self.walk_frames[self.current_frame], (self.rect.width, self.rect.height))
            #inverte a imagem se o movimento for para a esquerda
            if self.facing == -1:
                frame = pg.transform.flip(frame, True, False)
            self.image = frame
            self.animation_counter = 0

        #caso o inimigo morra, a imagem dele muda
        if not self.is_alive:
            death_image = pg.image.load(path.join(self.media_dir, "enemy_images/4.png"))
            frame = pg.transform.scale(death_image, (self.rect.width, self.rect.height))
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
        self.sound = pg.mixer.Sound(path.join(self.media_dir, "sounds/pixel-death-66829.mp3"))
        self.sound.play()

        super().die()

    def update(self, square_group:pg.sprite.Group) -> None:
        """
        método de atualização

        Parâmetros
            square_group:
                type: pg.sprite.Group
                description: sprites do cenário para verificação da colisão
        """
        super().update(square_group)

        #movimento contínuo do inimigo delimitado por uma range
        if self.rect.right > self.initial_pos + RANGE_ENEMY_DEFAULT:
            self.facing = -1
            self.natural_sound()
        elif self.rect.left < self.initial_pos - RANGE_ENEMY_DEFAULT:
            self.facing = 1
            self.natural_sound()

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
        self.current_dir = path.dirname(path.abspath(__file__))
        self.media_dir = path.join(self.current_dir, "media")

        #atributos de animação e de lançamento de projéteis
        self.shots = shots

        self.jump_counter = 0
        self.jump_delay = 50

        self.shot_counter = 0
        self.shot_delay = 40

        self.walk_frames = [
            pg.image.load(path.join(self.media_dir, "enemy_shoter_images/enemy_shooter0.png")),
            pg.image.load(path.join(self.media_dir, "enemy_shoter_images/enemy_shooter1.png")),
            pg.image.load(path.join(self.media_dir, "enemy_shoter_images/enemy_shooter2.png")),
            pg.image.load(path.join(self.media_dir, "enemy_shoter_images/enemy_shooter3.png")),
            pg.image.load(path.join(self.media_dir, "enemy_shoter_images/enemy_shooter4.png")),
            pg.image.load(path.join(self.media_dir, "enemy_shoter_images/enemy_shooter5.png")),
        ]

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

            frame = pg.transform.scale(self.walk_frames[self.current_frame], (self.rect.width, self.rect.height))

        #modelagem das animações (caso esteja morto)
        else:
            death_image = pg.image.load(path.join(self.media_dir, "enemy_shoter_images/J_5-removebg-preview.png"))
            frame = pg.transform.scale(death_image, (self.rect.width, self.rect.height))

        self.image = frame

    def update(self, square_group:pg.sprite.Group) -> None:
        """
        método de atualização

        Parâmetros
            square_group:
                type: pg.sprite.Group
                description: sprites do cenário para verificação da colisão
        """

        super().update(square_group)
