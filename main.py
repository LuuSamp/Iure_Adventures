import pygame
import sys
from level import Level
from player import Player
from input_handler import InputHandler
from const import *

screen_width = SCREEN_WIDTH
screen_height = SCREEN_HEIGHT

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
print(type(screen))
clock = pygame.time.Clock()
player = Player((200, 0))
level = Level(screen, player)
input_handler = InputHandler(player)
while True:
    input_handler.update()
    
    screen.blit(pygame.transform.scale(pygame.image.load("media/background/background_frame.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
    level.run()

    pygame.display.update()
    clock.tick(FPS)