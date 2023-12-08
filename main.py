
import pygame as pg
import sys
from menu import *


pg.init()


screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()
is_running = True
is_in_menu = True

play_img = pg.image.load("media/button_images/play.png")
exit_img = pg.image.load("media/button_images/quit.png")
play_button = Button(200, 150, play_img, 0.8)
exit_button = Button(200, 350, exit_img, 0.8)


while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_SPACE:
                    is_in_menu = True

    if is_in_menu:
        screen.fill("black") #screen.fill((107,35,142))
        if play_button.draw_button(screen):
            is_in_menu = False

        if exit_button.draw_button(screen):
            is_running = False
            
    else: #roda o jogo
        screen.fill("black")

    pg.display.flip()

    clock.tick(60)


pg.quit()
sys.exit()
