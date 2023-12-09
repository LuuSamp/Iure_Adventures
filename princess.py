import pygame as pg
from final_boss import FinalBoss

class PrincessPinho(pg.sprite.Sprite):
    """
    """
    def __init__(self, final_boss:FinalBoss, position:tuple) -> None:
        super().__init__()
        self.final_boss = final_boss

        self.frames = [[pg.image.load("media\princess\preso\pinho_preso_1.png"),
                        pg.image.load("media\princess\preso\pinho_preso_2.png"),
                        pg.image.load("media\princess\preso\pinho_preso_3.png"),
                        pg.image.load("media\princess\preso\pinho_preso_4.png"),
                        pg.image.load("media\princess\preso\pinho_preso_5.png"),
                        pg.image.load("media\princess\preso\pinho_preso_6.png"),],

                       [pg.image.load("media\princess\livre\pinho_solto0.png"),
                        pg.image.load("media\princess\livre\pinho_solto1.png"),
                        pg.image.load("media\princess\livre\pinho_solto2.png"),
                        pg.image.load("media\princess\livre\pinho_solto3.png"),
                        pg.image.load("media\princess\livre\pinho_solto4.png"),
                        pg.image.load("media\princess\livre\pinho_solto5.png"),]]
        
        self.animation_counter = 0
        self.animation_delay = 120
        self.animation_list = 0

        self.image = pg.Surface((64, 64))
        self.rect = self.image.get_rect(center=position)

    def animation(self) -> None:
        """
        """
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0

        #quando o boss morre
        if self.final_boss.health <= 0:
            self.animation_list = 1
            
        else:
            self.animation_list = 0

        frame = self.frames[self.animation_list[self.animation_counter // 20]]
        self.image = pg.transform.scale(frame, (64, 64))

        self.animation_counter += 1

    def update(self) -> None:
        """
        """
        self.animation()