import pygame
import sys
from game.const import *
from game.helpers import load_image

class Button:
    """
    Classe que representa um botão.
    """
    def __init__(self, x, y, image, image_clicked, scale = 1):
        """
        Inicialização do botão.

        Parâmetros
            x
                type: int
                description: posição x do centro do botão

            y
                type: int
                description: posição y do centro do botão

            image
                type: str
                description: path da imagem do botão sem o mouse em cima

            image_clicked
                type: str
                description: path da imagem do botão com o mouse em cima

            scale
                type: float
                description: escala para redimensionar a imagem
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.image_clicked = pygame.transform.scale(image_clicked, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, y)
        self.clicked = False
        self.mouse_pos = pygame.mouse.get_pos()

    def draw_button(self, surface):
        """
        Método que desenha o botão já funcionando na tela.
        """
    
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
    """
    Classe que representa o menu.
    """
    def __init__(self, surface):
        """
        Inicialização o menu.

        Parâmetros
            surface
                type: pygame.surface.Surface
                description: superfície que será desenhado o menu
        """
        self.display_surface = surface
        self.game_state = "menu"
        
        # criando os objetos que serão usados
        self.scaled_background = load_image(
            "media/background/background_frame.png", (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.play_img = load_image("media/button_images/play.png", None, alpha=True)
        self.play_clicked_img = load_image("media/button_images/play_clicked.png", None, alpha=True)
        self.quit_img = load_image("media/button_images/quit.png", None, alpha=True)
        self.quit_clicked_img = load_image("media/button_images/quit_clicked.png", None, alpha=True)
        self.play_button = Button(420, 400, self.play_img, self.play_clicked_img, 0.8)
        self.quit_button = Button(420, 550, self.quit_img, self.quit_clicked_img, 0.8)
        
        self._init_texts()
        
    def _init_texts(self):
        """
        Inicialização dos textos.
        """
        self.font = pygame.font.Font("media/button_images/PressStart2P-Regular.ttf", 16)
        
        # Nome dos criadores do jogo
        self.text_lines = ["Made by:", "Gustavo Tironi", "Luciano Sampaio", "Luís Felipe Marciano", "Matheus Carvalho", "Sillas Rocha"]
        self.line_height = 20
        self.y = 530
        self.text_lines_surface = []
        self.text_lines_rect = []
        
        # Renderização dos Nomes dos criadores
        for line in self.text_lines:
            self.text_lines_surface.append(self.font.render(line, True, "white"))
            self.text_lines_rect.append(self.text_lines_surface[-1].get_rect(center=(1000, self.y)))
            self.y += self.line_height
        
        # Título do jogo
        self.title1 = "Iure"
        self.title2 = "Adventures"
        
        # Renderização dos Titulos
        self.font_title1 = pygame.font.Font("media/button_images/PressStart2P-Regular.ttf", 80)
        self.title1_surface = self.font_title1.render(self.title1, True, "white")
        self.title1_rect = self.title1_surface.get_rect(center=(SCREEN_WIDTH/2, 170))
        
        self.font_title2 = pygame.font.Font("media/button_images/PressStart2P-Regular.ttf", 60)
        self.title2_surface = self.font_title2.render(self.title2, True, "red")
        self.title2_rect = self.title2_surface.get_rect(center=(SCREEN_WIDTH/2, 250))
        
    def draw_texts(self):
        """
        Médodo para botar todos os textos na tela.
        """
        # botando nome dos criadores do jogo
    
        for i, line in enumerate(self.text_lines):
            self.display_surface.blit(self.text_lines_surface[i], self.text_lines_rect[i])

        # botando primeira parte do título do jogo
        self.display_surface.blit(self.title1_surface, self.title1_rect)
       
        # botando segunda parte do título do jogo
        self.display_surface.blit(self.title2_surface, self.title2_rect)

    def run(self):
        """
        Método que desenha na tela tudo que tem no menu.
        """
        self.game_state = "menu"
        self.display_surface.blit(self.scaled_background, (0,0))
        self.draw_texts()

        # se botão play for clicado
        if self.play_button.draw_button(self.display_surface):
            self.game_state = "playing"

        # se botão quit for clicado
        if self.quit_button.draw_button(self.display_surface):
            pygame.quit()
            sys.exit()
    