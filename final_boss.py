import pygame as pg
from enemy import Enemy
from player import Player
from const import *

class FinalBoss(Enemy):
    """
    """

    def __init__(self, position: tuple, player:Player) -> None:
        super().__init__(position)

        self.image.fill("blue")

        self.player = player
        self.facing = 1
        self.initial_pos = self.rect.left

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