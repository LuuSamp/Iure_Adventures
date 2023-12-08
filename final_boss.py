import pygame as pg
from enemy import Enemy
from player import Player
from const import *
from shot import BossShot

class FinalBoss(Enemy):
    """
    """

    def __init__(self, position: tuple, player:Player, shots:pg.sprite.Group, explosion:pg.sprite.Group) -> None:
        super().__init__(position)


        self.image = pg.Surface((128, 128))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft = position)
        
        self.player = player
        self.facing = 1
        self.initial_pos = self.rect.left

        self.health = 3
        self.gun = BossGun(self, player, shots, explosion)

        self.move_range = INITIAL_RANGE
        self.move_counter = 0
        self.on_move = True
        self.rest_time = 0

        self.shooting = True

    def animation(self) -> None:
        pass

    def move(self) -> None:
        """
        """
        if self.on_move:
            self.direction.x = self.x_vel*self.facing
            self.rect.x += self.direction.x

    def delay(self):

        self.rest_time += 1
        if self.rest_time == FPS * 5:
            self.rest_time = 0
            self.move_range = INITIAL_RANGE
            self.move_counter = 0
            self.on_move = True

    def update(self, square_group: pg.sprite.Group, offset) -> None:
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
            self.x_vel = ENTITY_X_VEL
            self.gun.shot()

        elif self.rect.left < self.initial_pos - self.move_range and self.on_move and self.shooting:
            self.facing = 1
            self.move_counter += 1
            self.x_vel = ENTITY_X_VEL
            self.gun.shot()

        elif self.move_counter == 4:
            self.move_range = FINAL_RANGE

        elif self.move_counter == 5:
            self.on_move = False
            self.shooting = False
            self.delay()

        self.move()

    def die(self):
        if self.move_counter == 0: return

        self.health -= 1
        self.move_counter = 0
        self.x_vel *= 2
        self.rest_time = 0
        self.on_move = True
        self.move_range = INITIAL_RANGE
        
        if self.health == 0:
            super().die()

class BossGun(pg.sprite.Sprite):
    def __init__(self, holder: FinalBoss, player: Player, shots:pg.sprite.Group, explosion:pg.sprite.Group) -> None:
        super().__init__()
        self.holder = holder
        self.player = player
        self.shots = shots
        self.explosion = explosion
        self.collision = False

        self.aim_vector = (pg.math.Vector2(self.holder.rect.center) - pg.math.Vector2(self.player.rect.center)).normalize()
        self.still_vector = pg.math.Vector2(1, 0)
        self.angle_to_player = self.still_vector.angle_to(self.aim_vector)

        self.initial_image = pg.transform.scale(pg.image.load("media/bullet_images/B1.png"), (64, 32))
        self.rect = self.initial_image.get_rect(center= self.holder.rect.center)

        self.image = pg.transform.rotate(self.initial_image, -self.angle_to_player)

    def shot(self) -> None:
        """
        """
        if self.player.alive():
            self.shots.add(BossShot((self.rect.center[0], self.rect.center[1]), self.player, self.aim_vector, self.explosion))


    def update(self, *args):
        self.rect.center = self.holder.rect.center
        self.aim_vector = (pg.math.Vector2(self.holder.rect.center) - pg.math.Vector2(self.player.rect.center)).normalize()
        self.angle_to_player = self.still_vector.angle_to(self.aim_vector)
        self.image = pg.transform.rotate(self.initial_image, -self.angle_to_player)