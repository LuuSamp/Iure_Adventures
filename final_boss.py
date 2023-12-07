import pygame as pg
from enemy import Enemy
from player import Player
from const import *
from entity import Entity

class FinalBoss(Enemy):
    """
    """

    def __init__(self, position: tuple, player:Player) -> None:
        super().__init__(position)

        self.image.fill("blue")
        
        self.player = player
        self.facing = 1
        self.initial_pos = self.rect.left

        self.gun = BossGun(self, player)

        self.move_range = 100
        self.move_counter = 0
        self.on_move = True
        self.shot_delay = 0

    def animation(self) -> None:
        pass

    def move(self) -> None:
        """
        """
        if self.on_move:
            self.direction.x = self.x_vel*self.facing
            self.rect.x += self.direction.x

    def delay(self):
        self.shot_delay += 1
        if self.shot_delay == FPS * 5:
            self.shot_delay = 0
            self.move_counter = 0
            self.on_move = True

    def update(self, square_group: pg.sprite.Group, offset) -> None:
        self.initial_pos += offset

        self.rect.x += offset
        self.apply_gravity()
        self.collide_with_square(square_group)
        if self.rect.top > SCREEN_HEIGHT: 
            self.kill()

        if self.rect.left > self.initial_pos + self.move_range and self.on_move:
            self.facing = -1
            self.move_counter += 1

        elif self.rect.left < self.initial_pos - self.move_range and self.on_move:
            self.facing = 1
            self.move_counter += 1

        if self.move_counter == 4:
            pass

        elif self.move_counter == 5:
            self.on_move = False
            self.delay()

        self.move()

class BossGun(pg.sprite.Sprite):
    def __init__(self, holder: FinalBoss, player: Player) -> None:
        super().__init__()
        self.holder = holder
        self.player = player

        self.aim_vector = pg.math.Vector2(self.holder.rect.center) - pg.math.Vector2(self.player.rect.center)
        self.still_vector = pg.math.Vector2(1, 0)
        self.angle_to_player = self.still_vector.angle_to(self.aim_vector)

        self.initial_image = pg.transform.scale(pg.image.load("media/bullet_images/B1.png"), (64, 32))
        self.rect = self.initial_image.get_rect(center= self.holder.rect.center)

        self.image = pg.transform.rotate(self.initial_image, -self.angle_to_player)

    def update(self, *args):
        self.rect.center = self.holder.rect.center
        self.aim_vector = pg.math.Vector2(self.holder.rect.center) - pg.math.Vector2(self.player.rect.center)
        self.angle_to_player = self.still_vector.angle_to(self.aim_vector)
        self.image = pg.transform.rotate(self.initial_image, -self.angle_to_player)