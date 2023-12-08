import pygame as pg
import sys
from menu import *
from level import Level


pg.init()

square_size = 64
screen_width = 1200
screen_height = 11 * square_size
screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()
is_running = True
#is_in_menu = True
game_state = "menu"

level = Level(screen)

play_img = pg.image.load("media/button_images/play.png")
exit_img = pg.image.load("media/button_images/quit.png")
play_button = Button(400, 200, play_img, 0.8)
exit_button = Button(400, 400, exit_img, 0.8)


while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_SPACE:
                    game_state = "menu"

    if game_state == "menu":
        screen.fill("black")
        if play_button.draw_button(screen):
            game_state = "playing"

        if exit_button.draw_button(screen):
            is_running = False
            
    if game_state == "playing": #roda o jogo
        screen.fill("black")
        level.run()

    pg.display.flip()

    clock.tick(60)


pg.quit()
sys.exit()
