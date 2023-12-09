import pygame as pg
from pygame.sprite import _Group
from final_boss import FinalBoss
from os import path

class PrincessPinho(pg.sprite.Sprite):
    """
    classe para modelar o comportamento da princesa
    """
    def __init__(self, position:tuple) -> None:
        """
        método de inicialização da princesa

        Parâmetros
            position:
                type: tuple
                description: posição onde vai ser criada a princesa
        """
        super().__init__()

        self.current_dir = path.dirname(path.abspath(__file__))
        self.princess_dir = path.join(self.current_dir, "media", "princess")

        self.frames = [[pg.image.load(path.join(self.princess_dir, "preso/pinho_preso_1.png")),
                        pg.image.load(path.join(self.princess_dir, "preso/pinho_preso_2.png")),
                        pg.image.load(path.join(self.princess_dir, "preso/pinho_preso_3.png")),
                        pg.image.load(path.join(self.princess_dir, "preso/pinho_preso_4.png")),
                        pg.image.load(path.join(self.princess_dir, "preso/pinho_preso_5.png")),
                        pg.image.load(path.join(self.princess_dir, "preso/pinho_preso_6.png"))],

                       [pg.image.load(path.join(self.princess_dir, "livre/pinho_solto0.png")),
                        pg.image.load(path.join(self.princess_dir, "livre/pinho_solto1.png")),
                        pg.image.load(path.join(self.princess_dir, "livre/pinho_solto2.png")),
                        pg.image.load(path.join(self.princess_dir, "livre/pinho_solto3.png")),
                        pg.image.load(path.join(self.princess_dir, "livre/pinho_solto4.png")),
                        pg.image.load(path.join(self.princess_dir, "livre/pinho_solto5.png"))]]
        
        self.animation_counter = 0
        self.animation_delay = 120
        self.animation_list = 0

        self.image = pg.Surface((100, 100))
        self.rect = self.image.get_rect(center=position)

    def change_list(self) -> None:
        """
        método para mudar a lista de animações
        """
        self.animation_list = 1
        
    def animation(self) -> None:
        """
        método que controla as animações levando em consideração um delay
        """
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0

        frame = self.frames[self.animation_list][self.animation_counter // 20]
        self.image = pg.transform.scale(frame, (100, 100))

        self.animation_counter += 1

    def update(self) -> None:
        """
        método de atualizações
        """
        self.animation()

class Smoke(pg.sprite.Sprite):
    """
    """
    def __init__(self, position:tuple) -> None:
        """
        """

        super().__init__()
        
        self.current_dir = path.dirname(path.abspath(__file__))
        self.princess_dir = path.join(self.current_dir, "media", "princess")

        self.image = pg.Surface((120, 120))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=position)

        self.frames = [pg.image.load(path.join(self.princess_dir, "smoke/smoke_0.png")),
                       pg.image.load(path.join(self.princess_dir, "smoke/smoke_0.png")),
                       pg.image.load(path.join(self.princess_dir, "smoke/smoke_0.png")),
                       pg.image.load(path.join(self.princess_dir, "smoke/smoke_0.png"))]
        
        self.smoke_counter = 40

    def animation(self):
        """
        """

        if self.smoke_counter < 8:
            frame = 0
        elif self.smoke_counter < 16:
            frame = 1
        elif self.smoke_counter < 24:
            frame = 2
        elif self.smoke_counter < 32:
            frame = 3
        else:
            self.kill()
        try:
            self.image = pg.transform.scale(self.frames[frame], (120, 120))
            self.smoke_counter += 1
        except:
            return
        
    def update(self):
        self.animation()