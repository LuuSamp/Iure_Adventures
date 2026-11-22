import pygame
from game.const import SCREEN_WIDTH

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
        self.rect.center = (x, y)
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