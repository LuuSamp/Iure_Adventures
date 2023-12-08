import pygame as pg  
from const import *
from abc import ABC, abstractmethod
from const import *

class Entity(ABC, pg.sprite.Sprite):
    """
    classe abstrata criada para modelar o comportamento genérico de entidades
    """

    def __init__(self, position:tuple) -> None:
        """
        inicialização das entidades genéricas
        """

        super().__init__()
        self.image = pg.Surface(DIM_ENTITY)
        self.rect = self.image.get_rect(topleft = position)
        self.facing = 1

        #movimento da entidade
        self.direction = pg.math.Vector2(0, 0)
        self.gravity = GRAVITY
        self.x_vel = ENTITY_X_VEL
        self.jump_height = JUMP_HEIGHT

        #atributos gerais
        self.on_ground = True
        self.is_alive = True
        self.collision = True

    def apply_gravity(self) -> None:
        """
        método que modela a gravidade das entidades
        """
        #vai aplicar a todas as entidades a gravidade, alterando a posição vertical
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    @abstractmethod
    def move(self):
        ...
    
    def collide_with_square(self, square_group: pg.sprite.Group) -> None:
        """
        método que modela e verifica a colisão entre blocos do cenário e a entidade

        Parâmetros 
            square_group:
                type: pg.sprite.Group
                description: sprites do cenário para verificação da colisão
        """

        self.on_ground = False

        if not self.collision: return 
        
        for square in pg.sprite.spritecollide(self, square_group, False):
            if (self.direction.y + 3 > 0 and self.rect.bottom - self.direction.y - 1 < square.rect.top
                and (self.rect.right != square.rect.left + 5 and self.rect.left != square.rect.right - 5)): 
                self.rect.bottom = square.rect.top
                self.direction.y = 0
                self.on_ground = True

            elif self.direction.y < 0 and self.rect.top - self.direction.y >= square.rect.bottom:
                self.rect.top = square.rect.bottom
                self.direction.y = 0

        for square in pg.sprite.spritecollide(self, square_group, False):
            if self.direction.x > 0 and self.rect.right - self.direction.x <= square.rect.left: 
                self.rect.right = square.rect.left

            if self.direction.x < 0 and self.rect.left - self.direction.x >= square.rect.right: 
                self.rect.left = square.rect.right
                
    def die(self) -> None:
        """
        modelagem da morte de todas as entidades
        """

        self.is_alive = False
        self.collision = False
        
        #para o movimento horizontal e dá um leve movimento vertical
        self.x_vel = 0
        self.direction.y = -4

    def update(self, square_group: pg.sprite.Group, offset) -> None:
        """
        método de atualização
        """
        
        self.rect.x += offset

        self.apply_gravity()
        self.collide_with_square(square_group)
        if self.rect.top > SCREEN_HEIGHT: 
            self.kill()