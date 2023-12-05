import pygame as pg
from platforms import Platform
from player import Player
from enemy import Enemy
from input_handler import check_event

class Level:
    def __init__(self, player, enemy) -> None:

        self.platform_list = pg.sprite.Group()
        self.player_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()

        self.player = player
        self.player_list.add(self.player)

        self.enemy = enemy
        self.enemy_list.add(self.enemy)

    def update(self):
        check_event(self.player)
        self.platform_list.update()
        self.player_list.update()
        self.enemy_list.update()
        

    def draw(self, screen: pg.Surface):
        screen.fill("white")

        self.player_list.draw(screen)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

class TestLevel(Level):
    def __init__(self, player, enemy) -> None:
        super().__init__(player, enemy)
        
        for block in range(5):
            self.platform_list.add(Platform(70, 50, (100*block, 200)))


if __name__ == "__main__":
    pg.init()
    player = Player((100, 0))
    enemy = Enemy((300, 0))
    level = TestLevel(player, enemy)
    screen = pg.display.set_mode((500, 600))
    clock = pg.time.Clock()

    while True:
        level.update()
        level.draw(screen)
        pg.display.update()
        clock.tick(30)