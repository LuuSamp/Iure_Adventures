import pygame
import sys
import screens

class Button:
    def __init__(self, x, y, image, image_clicked, scale = 1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.image_clicked = pygame.transform.scale(image_clicked, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.mouse_pos = pygame.mouse.get_pos()

    def draw_button(self, surface):
        action = False
        mouse_pos = pygame.mouse.get_pos()


        if self.rect.collidepoint(mouse_pos):
            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
               self.clicked = True
               action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            surface.blit(self.image_clicked, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Menu:
    def __init__(self, surface):
        self.display_surface = surface
        self.background = pygame.image.load("media/button_images/background.png")
        self.play_img = pygame.image.load("media/button_images/play.png")
        self.play_clicked_img = pygame.image.load("media/button_images/play_clicked.png")
        self.quit_img = pygame.image.load("media/button_images/quit.png")
        self.quit_clicked_img = pygame.image.load("media/button_images/quit_clicked.png")
        self.play_button = Button(400, 200, self.play_img, self.play_clicked_img, 0.8)
        self.quit_button = Button(400, 400, self.quit_img, self.quit_clicked_img, 0.8)
        self.game_state = "menu"

    def run(self):
        self.display_surface.fill("black") # cria o background
        self.game_state = "menu"

        if self.play_button.draw_button(self.display_surface):
            self.game_state = "playing"

        if self.quit_button.draw_button(self.display_surface):
            pygame.quit()
            sys.exit()
    