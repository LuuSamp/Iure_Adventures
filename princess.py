import pygame as pg
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
                        pg.image.load(path.join(self.princess_dir, "livre/pinho_solto5.png"))],
                        
                        [pg.image.load(path.join(self.princess_dir, "preso/pinho_preso_7.png")),
                         pg.image.load(path.join(self.princess_dir, "preso/pinho_preso_8.png")),
                         pg.image.load(path.join(self.princess_dir, "livre/pinho_solto0.png"))]
                        ]
        
        self.animation_counter = 0
        self.animation_delay = 120
        self.animation_list = 0

        self.image = pg.Surface((100, 100))
        self.rect = self.image.get_rect(center=position)
        self.on_animation = True

    def change_list(self) -> None:
        """
        método para mudar a lista de animações
        """
        self.animation_list = 2
        self.on_animation = False
        self.animation_counter = 0
        
    def animation(self) -> None:
        """
        método que controla as animações levando em consideração um delay
        """
        if self.on_animation:
            if self.animation_counter >= self.animation_delay:
                self.animation_counter = 0

            frame = self.frames[self.animation_list][self.animation_counter // 20]
            self.image = pg.transform.scale(frame, (100, 100))

            self.animation_counter += 1

    def animation_jail(self):
        """
        método para modelar a animação da cela caindo
        """
        if not self.on_animation:
            frame = self.frames[self.animation_list][self.animation_counter // 20]
            self.image = pg.transform.scale(frame, (100, 100))

            self.animation_counter += 1

        if self.animation_counter >= 60:
            self.on_animation = True
            self.on_animation = 0
            self.animation_counter = 0
            self.animation_list = 1
        

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
        
        self.current_dir = path.dirname(path.abspath(__file__))
        self.princess_dir = path.join(self.current_dir, "media", "princess")

        self.image = pg.Surface((120, 120))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=position)

        self.frames = [pg.image.load(path.join(self.princess_dir, "smoke/smoke_0.png")),
                       pg.image.load(path.join(self.princess_dir, "smoke/smoke_0.png")),
                       pg.image.load(path.join(self.princess_dir, "smoke/smoke_0.png")),
                       pg.image.load(path.join(self.princess_dir, "smoke/smoke_0.png"))]
        
        self.smoke_counter = 60

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
        try:
            self.image = pg.transform.scale(self.frames[frame], (120, 120))
            self.smoke_counter += 1
        except:
            return
        
    def update(self) -> None:
        """
        método de atualização
        """

        self.animation()