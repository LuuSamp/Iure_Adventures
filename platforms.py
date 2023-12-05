import pygame as pg
from typing import Tuple

class Platform(pg.sprite.Sprite):
    def __init__(self, width: int, height: int, position: Tuple[int]) -> None:
        super().__init__()

        self.image = pg.Surface((width, height))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)