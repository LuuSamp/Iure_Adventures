import pygame as pg
from platforms import Platform
from const import *

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
        
        for block in range(20):
            self.platform_list.add(Platform(*DIM_ENTITY, (32*block, 264)))
        for block in range(20):
            self.platform_list.add(Platform(*DIM_ENTITY, (128*block, 200)))
