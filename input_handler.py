from pygame.locals import *
import pygame as pg

def check_event(player):
    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP: player.jump()
        if event.type == QUIT: 
            pg.quit()
            exit()