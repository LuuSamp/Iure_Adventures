import pygame as pg
from enemy import Enemy
from player import Player
from const import *
from shot import BossShot
from os import path

class FinalBoss(Enemy):
    """
    classe criada para modelar o comportamento do boss final
    """

    def __init__(self, position: tuple, player:Player, shots:pg.sprite.Group, explosion:pg.sprite.Group) -> None:
        """
        método de inicialização

        Parâmetros
            position
                type: tuple
                description: posição onde o inimigo final deve ser criado

            player
                type: Player
                description: player principal do jogo

            shots
                type: pg.sprite.Group
                description: grupo de tiros

            explosion
                type: pg.sprite.Group
                description: grupo de explosões
        """
        super().__init__(position)

        current_dir = path.dirname(path.abspath(__file__))
        media_dir = path.join(current_dir, "media")
        self.image_dir = path.join(media_dir, "final_boss", "boss")
        initial_image = path.join(self.image_dir, "final_boss_0.png")

        self.image = pg.transform.scale(pg.image.load(initial_image), (64, 128))
        self.rect = self.image.get_rect(topleft = position)
        
        self.player = player
        self.facing = 1
        self.initial_pos = self.rect.left

        self.health = 3

        self.move_range = INITIAL_RANGE
        self.move_counter = 0
        self.on_move = True
        self.rest_time = 0

        self.gun = BossGun(self, player, shots, explosion)
        self.shooting = True
        self.shot_cooldown = 2*FPS
        self.shot_time = 0
        
        self.sel_frame = 0
        self.frames = [[pg.image.load(path.join(self.image_dir, "final_boss_2.png")), pg.image.load(path.join(self.image_dir, "final_boss_5.png"))],
                       [pg.image.load(path.join(self.image_dir, "final_boss_1.png")), pg.image.load(path.join(self.image_dir, "final_boss_4.png"))],
                       [pg.image.load(path.join(self.image_dir, "final_boss_0.png")), pg.image.load(path.join(self.image_dir, "final_boss_3.png"))]
        ]

        self.animation_counter = 0
        self.animation_delay = 10

    def animation(self) -> None:
        """
        método de gerenciamento das animações do boss final
        """
        if self.animation_counter >= self.animation_delay/(self.x_vel + 1) and self.is_alive == True and self.on_move == True:

            if self.sel_frame == 0:
                self.image = pg.transform.scale(self.frames[self.health - 1][self.sel_frame], (64, 128))
                self.sel_frame = 1

            elif self.sel_frame == 1:
                self.image = pg.transform.scale(self.frames[self.health - 1][self.sel_frame], (64, 128))
                self.sel_frame = 0

            if self.facing == -1:
                self.image = pg.transform.flip(self.image, True, False)

            self.animation_counter = 0
        self.animation_counter += 1
        

    def move(self) -> None:
        """
        método que modela o movimento
        """
        if self.on_move:
            self.direction.x = self.x_vel*self.facing
            self.rect.x += self.direction.x

    def delay(self):
        """
        método que controla os momentos de vunerabilidade do inimigo
        """
        self.rest_time += 1
        if self.rest_time == FPS * 5:
            self.rest_time = 0
            self.move_range = INITIAL_RANGE
            self.move_counter = 0
            self.on_move = True

    def shoot(self):
        """
        método que cria os tiros sempre que necessário
        """
        self.shot_time += 1
        #criação do tiro com base em um cooldown estabelecido que vai variando a medida que ele toma dano (método die())
        if self.shot_time == self.shot_cooldown:
            self.gun.shot()
            self.shot_time = 0

    def update(self, square_group: pg.sprite.Group, offset) -> None:
        """
        método de atualização
        """
        self.initial_pos += offset
        self.rect.x += offset
        self.apply_gravity()
        self.collide_with_square(square_group)
        if self.rect.top > SCREEN_HEIGHT: 
            self.kill()

        if self.rect.left == self.initial_pos:
            self.shooting = True

        if self.rect.left > self.initial_pos + self.move_range and self.on_move and self.shooting:
            self.facing = -1
            self.move_counter += 1
            self.image = pg.transform.flip(self.image, True, False)
            self.x_vel = ENTITY_X_VEL

        elif self.rect.left < self.initial_pos - self.move_range and self.on_move and self.shooting:
            self.facing = 1
            self.move_counter += 1
            self.image = pg.transform.flip(self.image, True, False)
            self.x_vel = ENTITY_X_VEL

        elif self.move_counter == 4:
            self.move_range = FINAL_RANGE

        elif self.move_counter == 5:
            self.on_move = False
            self.shooting = False
            self.delay()

        self.move()
        self.animation()
        if self.shooting:
            self.shoot()

    def die(self):
        """
        método de gerenciamento da morte do boss final
        """
        if self.move_counter == 0: 
            return

        #comportamentos necessário a cada dano que ele leva do player principal
        self.health -= 1
        self.shot_cooldown -= 0.5*FPS
        self.move_counter = 0
        self.x_vel *= 2
        self.rest_time = 0
        self.on_move = True
        self.move_range = INITIAL_RANGE
        
        #caso o número de vidas dele acabe, ele será removido do grupo
        if self.health == 0:
            super().die()

class BossGun(pg.sprite.Sprite):
    """
    classe que modela o comportamento da arma do final boss
    """

    def __init__(self, holder: FinalBoss, player: Player, shots:pg.sprite.Group, explosion:pg.sprite.Group) -> None:
        """
        método de inicialização

        Parâmetros:
            holder
                type: FinalBoss
                descripition: inimigo principal para que ela seja posicionada corretamente sobre ele 

            player
                type: Player
                descripition: player para que seja extraida a posição dele e criado um vetor que vai modelar o movimento de cada projétil

            shots
                type: pg.sprite.Group
                descripition: grupo de projéteis

            explosion
                type: pg.sprite.Group
                descripition: grupo de explosões
        """

        super().__init__()
        self.holder = holder
        self.player = player
        self.shots = shots
        self.explosion = explosion
        self.collision = False
        
        #vetor com a direção do player
        self.aim_vector = (pg.math.Vector2(self.holder.rect.center) - pg.math.Vector2(self.player.rect.center)).normalize()
        self.still_vector = pg.math.Vector2(0, -1)
        self.angle_to_player = self.still_vector.angle_to(self.aim_vector)

        current_dir = path.dirname(path.abspath(__file__))
        media_dir = path.join(current_dir, "media")
        self.image_dir = path.join(media_dir, "final_boss", "gun")
        initial_image = path.join(self.image_dir, "boss_gun_0.png")

        self.frames = [
            pg.image.load(path.join(self.image_dir, "boss_gun_2.png")),
            pg.image.load(path.join(self.image_dir, "boss_gun_1.png")),
            pg.image.load(path.join(self.image_dir, "boss_gun_0.png"))
        ]

        self.initial_image = pg.transform.scale(pg.image.load(initial_image), (32, 120))
        self.position_on_holder = (self.holder.rect.left + 4 * 4, self.holder.rect.top + 15 * 4)

        self.image = pg.transform.rotate(self.initial_image, -self.angle_to_player)
        self.rect = self.initial_image.get_rect(center= self.position_on_holder)
        self.image.get_rect()

    def shot(self) -> None:
        """
        método que cria cada um dos projéteis
        """
        #caso o inimigo ainda esteja vivo, ele irá atirar na direção do player
        if self.player.alive():
            self.shots.add(BossShot((self.rect.center[0], self.rect.center[1]), self.player, self.aim_vector, self.explosion))

    def update_image(self) -> None:
        """
        método que atualiza a imagem da arma com base no nível de vida do boss
        """
        if self.holder.health == 0:
            self.initial_image = pg.transform.scale(self.frames[self.holder.health], (32, 120))
        else:
            self.initial_image = pg.transform.scale(self.frames[self.holder.health - 1], (32, 120))



    def update(self) -> None:
        """
        método de atualização
        """
        self.update_image()
        #geração do vetor com a direção do player 
        self.aim_vector = (pg.math.Vector2(self.holder.rect.center) - pg.math.Vector2(self.player.rect.center)).normalize()
        self.angle_to_player = self.still_vector.angle_to(self.aim_vector)
        self.image = pg.transform.rotate(self.initial_image, -self.angle_to_player)
        self.rect = self.image.get_rect()

        #posicionamento da arma sobre o inimigo final
        if self.holder.facing == 1:
            self.position_on_holder = (self.holder.rect.left + 4 * 4, self.holder.rect.top + 14 * 4 - 1)
        else:
            self.position_on_holder = (self.holder.rect.right - 4 * 4, self.holder.rect.top + 14 * 4 - 1)
        self.rect.center = self.position_on_holder