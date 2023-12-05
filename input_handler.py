from pygame.locals import *
import pygame as pg

class InputHandler:
    def __init__(self, player) -> None:
        self._player = player

    def update(self):
        self.check_event()

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP: self._player.jump()
            if event.key == K_LEFT: self._player.move(-1)
            if event.key == K_RIGHT: self._player.move(1)
        
        if event.type == KEYUP:
            if event.key == K_LEFT: self._player.move(1)
            if event.key == K_RIGHT: self._player.move(-1)

        if event.type == QUIT: 
            pg.quit()
            exit()

    def check_event(self):
        for event in pg.event.get():
            self.handle_event(event)