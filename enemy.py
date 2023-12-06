import pygame as pg  
from entity import Entity
from shot import Shot

class Enemy(Entity):

    def __init__(self, position):
        super().__init__(position)
        self.initial_pos = self.rect.left
        self.image.fill("black")
        self.sound = pg.mixer.Sound("media/monster-death-grunt-131480.mp3")

        self.walk_frames = [
            pg.image.load("media/1.png"),
            pg.image.load("media/2.png"),
            pg.image.load("media/3.png")
        ]

        self.current_frame = 0 
        self.animation_delay = 7
        self.animation_counter = 0

    def animation(self):
        self.animation_counter += 1
        
        #uma forma de ajustar um delay
        if self.animation_counter >= self.animation_delay:
            #muda de frame
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            
            #ajusta a imagem no tamanho do rect
            frame = pg.transform.scale(self.walk_frames[self.current_frame], (self.rect.width, self.rect.height))

            #inverte a imagem se o movimento for para a esquerda
            if self.facing == -1:
                frame = pg.transform.flip(frame, True, False)

            #atualiza a imagem do inimigo
            self.image = frame

            #reinicia a contagem
            self.animation_counter = 0

    def move(self):
        self.direction.x = self.x_vel*self.facing
        self.rect.x += self.direction.x

    def natural_sound(self):
        self.sound.set_volume(0.2)
        self.sound.play()

    def die(self):
        self.sound = pg.mixer.Sound("media/pixel-death-66829.mp3")
        self.sound.play()
        self.kill()

        self.x_vel = 0

    def update(self, square_group):
        super().update(square_group)

        #impedindo ele de cair além da plataforma
        if self.rect.bottomleft[1] < 200:
            self.on_ground = False
            self.gravity = 0.8
        else:
            self.on_ground = True
            self.gravity = 0
            self.direction.y = 0

        #movimento contínuo do inimigo
        if self.rect.right > self.initial_pos + 100:
            self.facing = -1
            self.natural_sound()
        elif self.rect.left < self.initial_pos - 100:
            self.facing = 1
            self.natural_sound()

        self.move()
        self.animation()
            

class Enemy_Shooter(Enemy):

    def __init__(self, position, shots):
        super().__init__(position)

        self.shots = shots

        self.jump_counter = 0
        self.jump_delay = 50

        self.shot_counter = 0
        self.shot_delay = 40

    def move(self):
        if self.on_ground and self.jump_counter >= self.jump_delay:
            self.direction.y = -10
            self.jump_counter = 0
        self.jump_counter +=1

    def animation(self):
        self.shot_counter +=1
        if self.shot_counter >= self.shot_delay:
            self.shots.add(Shot((self.rect.x, self.rect.center[1])))
            self.shot_counter = 0

    def update(self, square_group):
        super().update(square_group)
