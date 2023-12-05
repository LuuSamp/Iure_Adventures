import pygame as pg
from platforms import Platform
from player import Player
from enemies import Enemies
from input_handler import check_event

class Level:
    def __init__(self, player, enemie) -> None:

        self.platform_list = pg.sprite.Group()
        self.player_list = pg.sprite.Group()
        self.enemie_list = pg.sprite.Group()

        self.player = player
        self.player_list.add(self.player)

        self.enemie = enemie
        self.enemie_list.add(self.enemie)

    def update(self):
        check_event(self.player)
        self.platform_list.update()
        self.player_list.update()
        self.enemie_list.update()
        

    def draw(self, screen: pg.Surface):
        screen.fill("white")

        self.player_list.draw(screen)
        self.platform_list.draw(screen)
        self.enemie_list.draw(screen)

class TestLevel(Level):
    def __init__(self, player, enemie) -> None:
        super().__init__(player, enemie)
        
        for block in range(5):
            self.platform_list.add(Platform(70, 50, (100*block, 200)))


if __name__ == "__main__":
    pg.init()
    player = Player((100, 0))
    enemie = Enemies((300, 0))
    level = TestLevel(player, enemie)
    screen = pg.display.set_mode((500, 600))
    clock = pg.time.Clock()

    while True:
        level.update()
        level.draw(screen)
        pg.display.update()
        clock.tick(30)