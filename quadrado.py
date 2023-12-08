import pygame as pg
from player import Player
from const import *
from entity import Entity
import time

class Rect(pg.sprite.Sprite):
    """
    Classe padrão de objetos de cenário.

    """
    def __init__(self, x: int, y: int, size_x:int, size_y:int) -> None:
        """Ininicializa o objeto de cenário com sua posição e tamanho.

        Parameters
        ----------
        x : int
            posição em relação ao eixo x
        y : int
            posição em relação ao eixo y
        size_x : int
            tamanho em relação ao eixo x
        size_y : int
            tamanho em relação ao eixo y
        """
        super().__init__()
        self.image = pg.Surface((size_x, size_y))
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def update(self, shift:int) -> None:
        """Atualiza a posição do objeto em relação a movimentação do cenário.

        Parameters
        ----------
        shift : int
            movimentação realizada.
        """
        self.rect.x += shift
        
class Square(Rect):
    """
    Objeto padrão de cenário de quadrado.

    """
    def __init__(self, x:int, y:int, size:int) -> None:
        """Inicializa o quadrado

        Parameters
        ----------
        x : int
            posição em relação ao eixo x
        y : int
            posição em relação ao eixo y
        size : int
            lado do retângulo
        """
        super().__init__(x, y, size, size)

class StaticSquare(Square):
    """
    Objeto de cenário quadrado com uma imagem fixa.

    """
    def __init__(self, x:int, y:int, size:int, image_path:str) -> None:
        """Inicializa o quadrado com uma imagem

        Parameters
        ----------
        x : int
            posição em relação ao eixo x
        y : int
            posição em relação ao eixo y
        size : int
            lado do retângulo
        image_path : str
            caminho onde a imagem do objeto se localiza
        """
        super().__init__(x, y, size)
        image = pg.image.load(image_path)
        frame = pg.transform.scale(image, (size, size))
        self.image = frame

class ColisionSquare(StaticSquare):
    """
    Objeto de cenário que, ao entrar em contato com o jogador, irá cair e depois reaparecer.

    """
    def __init__(self, x: int, y: int, size: int, image_path: str, player: Player) -> None:
        """Inicializa o bloco que reage a colisões.

        Parameters
        ----------
        x : int
            posição em relação ao eixo x
        y : int
            posição em relação ao eixo y
        size : int
            lado do retângulo
        image_path : str
            caminho onde a imagem do objeto se localiza
        player : Player
            jogador com que as colisões ocorrerão
        """
        super().__init__(x, y, size, image_path)
        self.player = player
        self.speed_y = 0
        self.gravity = GRAVITY
        self.collision = True
        self.init_y = y
        self.cooldown = 0

    def _player_collision(self) -> bool:
        """ Verifica se houve colisão entre o jogador e o objeto

        Returns
        -------
        bool
            True caso sim e False caso não
        """
        if self.collision == False:
            return False
        elif self.player.rect.right >= self.rect.left and self.player.rect.left <= self.rect.right and self.player.rect.bottom == self.rect.top:
            return True
        else:
            return False

    def fall(self) -> None:
        """Faz com que o objeto caia quando desejado.
        """
        self.speed_y = 4
        self.rect.y += self.speed_y

    def _reset_block(self) -> None:
        """Retorna o objeto a sua posição de altura inicial.
        """
        self.rect.y = self.init_y
    
    def update(self, shift:int) -> None:
        """Inicia um timer caso haja uma colisão entre o jogador e a parte superior do bloco,
        após alguns instantes o bloco cai e logo após volta a aparecer onde estava inciialmente.

        Parameters
        ----------
        shift : int
            deslocamento horizontal
        """
        self.rect.x += shift

        if self._player_collision() == True:
            self.cooldown += 1
        elif self.cooldown > 0:
            self.cooldown += 1

        if self.cooldown >= FPS * 5:
            self.cooldown = 0
            self._reset_block()
            self.collision = True
        elif self.cooldown >= FPS * 2:
            self.fall()

