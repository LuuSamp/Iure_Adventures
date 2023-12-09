import pygame
import sys
from menu import Menu
from const import *

def exit_game():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_menu():

    #Pygame setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    main_menu = Menu(screen)

    while True:
        exit_game()

        main_menu.run()
        
        pygame.display.update()

        clock.tick(FPS)


def play():
    pass