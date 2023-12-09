from pygame.locals import *
import pygame as pg
from player import Player

class InputHandler:
    """
    Manuseia as entradas do usuário e move o jogador.
    
    Parâmetros:
        player (Player): O objeto Player que será movido com as entradas
    """
    def __init__(self, player: Player) -> None:
        self._player = player

    def update(self):
        """
        Atualiza o InputHandler
        """
        self.handle_move_keys()
        self.check_event()

    def handle_move_keys(self):
        keys = pg.key.get_pressed()
        
        if keys[K_RIGHT]: self._player.move(1)
        if keys[K_LEFT]: self._player.move(-1)

    def handle_event(self, event: pg.event.Event):
        """
        Manuseia as ações de cada evento.
        
        Parâmetros:
            event (pygame.event.Event): O evento a ser manuseado.
        """
        if event.type == KEYDOWN:
            if event.key == K_UP: self._player.jump()

        if event.type == QUIT: 
            pg.quit()
            exit()

    def check_event(self):
        """
        Checa por eventos de entrada do usuário e chama o método handle_event.
        """
        for event in pg.event.get():
            self.handle_event(event)