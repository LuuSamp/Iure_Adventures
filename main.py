import pygame
import sys
from menu import *
from level import Level
from player import Player
from input_handler import InputHandler

pygame.init()

# pygame setup
square_size = 64
screen_width = 1200
screen_height = 11 * square_size
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# creating variables
is_running = True
game_state = "menu"
 
# creating used objects
play_img = pygame.image.load("media/button_images/play.png")
exit_img = pygame.image.load("media/button_images/quit.png")
play_button = Button(400, 200, play_img, 0.8)
exit_button = Button(400, 400, exit_img, 0.8)
player = Player((70, 0))
level = Level(screen, player)
input_handler = InputHandler(player)

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    game_state = "menu"

    if game_state == "menu":
        screen.fill("black")
        if play_button.draw_button(screen):
            game_state = "playing"

        if exit_button.draw_button(screen):
            is_running = False
            
    if game_state == "playing": #roda o jogo
        input_handler.update()
    
        screen.fill('black')
        level.run()

    pygame.display.update()

    clock.tick(60)


pygame.quit()
sys.exit()
