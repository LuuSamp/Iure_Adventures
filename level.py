import pygame as pg
from platforms import Platform
from player import Player
from enemy import Enemy

class Level:
    def __init__(self) -> None:

        self.platform_list = pg.sprite.Group()
        self.enemie_list = pg.sprite.Group()

    def update(self):
        self.platform_list.update()
        self.enemie_list.update()
        

    def draw(self, screen: pg.Surface):
        screen.fill("white")
        self.platform_list.draw(screen)
        self.enemie_list.draw(screen)

class TestLevel(Level):
    def __init__(self) -> None:
        super().__init__()
        
        for block in range(5):
            self.platform_list.add(Platform(70, 50, (100*block, 200)))
