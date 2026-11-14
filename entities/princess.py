import pygame as pg
from entities.final_boss import FinalBoss
from os import path
from game.const import *
from game.helpers import load_image
from game.resource import resource_path

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

        self.princess_dir = resource_path("media", "princess")

        frame_size = (2 * SQUARE_SIZE, 2 * SQUARE_SIZE)
        self.frames = [[load_image(path.join(self.princess_dir, "preso/pinho_preso_1.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "preso/pinho_preso_2.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "preso/pinho_preso_3.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "preso/pinho_preso_4.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "preso/pinho_preso_5.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "preso/pinho_preso_6.png"), frame_size, alpha=True)],

                       [load_image(path.join(self.princess_dir, "livre/pinho_feliz0.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "livre/pinho_feliz1.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "livre/pinho_feliz0.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "livre/pinho_feliz1.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "livre/pinho_feliz0.png"), frame_size, alpha=True),
                        load_image(path.join(self.princess_dir, "livre/pinho_feliz1.png"), frame_size, alpha=True)],
                        
                        [load_image(path.join(self.princess_dir, "preso/pinho_preso_7.png"), frame_size, alpha=True),
                         load_image(path.join(self.princess_dir, "preso/pinho_preso_8.png"), frame_size, alpha=True),
                         load_image(path.join(self.princess_dir, "livre/pinho_solto0.png"), frame_size, alpha=True)]
                        ]
        
        self.animation_counter = 0
        self.animation_delay = 120
        self.animation_list = 0

        self.image = pg.Surface(frame_size)
        self.rect = self.image.get_rect(topleft=position)
        self.animated = True

    def change_list(self) -> None:
        """
        método para mudar a lista de animações
        """
        self.animation_list = 2
        self.animated = False
        self.animation_counter = 0
        
    def animation(self) -> None:
        """
        método que controla as animações levando em consideração um delay
        """
        if self.animated:
            if self.animation_counter >= self.animation_delay:
                self.animation_counter = 0

            self.image = self.frames[self.animation_list][self.animation_counter // 20]

            self.animation_counter += 1

    def animation_jail(self) -> None:
        """
        método para modelar a animação da cela caindo
        """
        if not self.animated and self.animation_counter > 60:
            self.animated = True
            self.animation_counter = 0
            self.animation_list = 1

        if not self.animated:
            try:
                self.image = self.frames[self.animation_list][self.animation_counter // 20]
            except:
                pass

            self.animation_counter += 1
        
    def update(self) -> None:
        """
        método de atualizações
        """
        self.animation()
        self.animation_jail()

class Smoke(pg.sprite.Sprite):
    """
    classe para modelar o comportamento da fumaça
    """
    def __init__(self, position:tuple) -> None:
        """
        método de inicialização da fumaça

        Parâmetros
            position:
                type: tuple
                description: posição onde vai ser criada a fumaça
        """

        super().__init__()
        
        self.princess_dir = resource_path("media", "princess")

        self.image = pg.Surface((150, 150))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=position)

        smoke_size = (150, 150)
        self.frames = [load_image(path.join(self.princess_dir, "smoke/smoke_0.png"), smoke_size, alpha=True),
                       load_image(path.join(self.princess_dir, "smoke/smoke_1.png"), smoke_size, alpha=True),
                       load_image(path.join(self.princess_dir, "smoke/smoke_2.png"), smoke_size, alpha=True),
                       load_image(path.join(self.princess_dir, "smoke/smoke_3.png"), smoke_size, alpha=True)]
        
        self.smoke_counter = 0

    def animation(self) -> None:
        """
        método para modelar a animação da fumaça
        """

        if self.smoke_counter < 15:
            frame = 0
        elif self.smoke_counter < 30:
            frame = 1
        elif self.smoke_counter < 45:
            frame = 2
        elif self.smoke_counter < 60:
            frame = 3
        else:
            self.kill()
            return
        try:
            self.image = self.frames[frame]
            self.smoke_counter += 1
        except Exception as err:
            print(err)
            return
        
    def update(self) -> None:
        """
        método de atualização
        """

        self.animation()