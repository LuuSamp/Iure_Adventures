import pygame as pg
from enemy import Enemy
from player import Player
from const import *
from shot import BossShot
from os import path

class FinalBoss(Enemy):
    """
    """

    def __init__(self, position: tuple, player:Player, shots:pg.sprite.Group, explosion:pg.sprite.Group) -> None:
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
        self.gun = BossGun(self, player, shots, explosion)

        self.move_range = INITIAL_RANGE
        self.move_counter = 0
        self.on_move = True
        self.rest_time = 0

        self.shooting = True

        self.sel_frame = 0
        self.frames = [[pg.image.load(path.join(self.image_dir, "final_boss_2.png")), pg.image.load(path.join(self.image_dir, "final_boss_5.png"))],
                       [pg.image.load(path.join(self.image_dir, "final_boss_1.png")), pg.image.load(path.join(self.image_dir, "final_boss_4.png"))],
                       [pg.image.load(path.join(self.image_dir, "final_boss_0.png")), pg.image.load(path.join(self.image_dir, "final_boss_3.png"))]
        ]

        self.animation_counter = 0
        self.animation_delay = 10

    def animation(self) -> None:
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
            self.image = pg.transform.flip(self.image, True, False)
            self.x_vel = ENTITY_X_VEL
            self.gun.shot()

        elif self.rect.left < self.initial_pos - self.move_range and self.on_move and self.shooting:
            self.facing = 1
            self.move_counter += 1
            self.image = pg.transform.flip(self.image, True, False)
            self.x_vel = ENTITY_X_VEL
            self.gun.shot()

        elif self.move_counter == 4:
            self.move_range = FINAL_RANGE

        elif self.move_counter == 5:
            self.on_move = False
            self.shooting = False
            self.delay()

        self.move()
        self.animation()

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
        """
        if self.player.alive():
            self.shots.add(BossShot((self.rect.center[0], self.rect.center[1]), self.player, self.aim_vector, self.explosion))

    def update_image(self) -> None:
        """
        """
        if self.holder.health == 0:
            self.initial_image = pg.transform.scale(self.frames[self.holder.health ], (32, 120))
        else:
            self.initial_image = pg.transform.scale(self.frames[self.holder.health - 1], (32, 120))



    def update(self, *args):
        self.update_image()
        self.aim_vector = (pg.math.Vector2(self.holder.rect.center) - pg.math.Vector2(self.player.rect.center)).normalize()
        self.angle_to_player = self.still_vector.angle_to(self.aim_vector)
        self.image = pg.transform.rotate(self.initial_image, -self.angle_to_player)
        self.rect = self.image.get_rect()
        if self.holder.facing == 1:
            self.position_on_holder = (self.holder.rect.left + 4 * 4, self.holder.rect.top + 14 * 4 - 1)
        else:
            self.position_on_holder = (self.holder.rect.right - 4 * 4, self.holder.rect.top + 14 * 4 - 1)
        self.rect.center = self.position_on_holder