import pygame
from game.level import Level, BossLevel
from entities.player import Player
from game.input_handler import InputHandler
from game.const import *
from game.menu import Menu

class Game:
    """
    Classe responsável por manusear o jogo.
    """
    def __init__(self):
        """
        Método construtor da classe Game. 
        Inicializa os principais recursos do pygame e as principais entidades do jogo.
        """
        pygame.init()
        pygame.display.set_caption('Iure Adventures')
        pygame.mixer.init()
        pygame.mixer.music.load("./media/sounds/background_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.04)  
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player((0,0))
        self.main_menu = Menu(self.screen)
        self.input_handler = InputHandler(self.player)
        self.levels = [Level(self.screen, self.player), BossLevel(self.screen, self.player)]
        self.coins = 0
        self.current_level = 0
        self.game_state = "menu"

        self.win_counter = 0
    
    def reset(self):
        """
        Reseta o objeto Game.
        """
        self.__init__()
    
    def run(self):
        """
        Roda o jogo.
        """
        self.game_loop()
    
    def load_menu(self):
        """
        Carrega o menu do jogo.
        """
        self.main_menu.run()
        self.game_state = self.main_menu.game_state
    
    def change_level(self):
        """
        Muda o nível se o nível atual for completado.
        """
        if self.levels[self.current_level].level_completed and self.current_level < len(self.levels) - 1:
            self.coins = self.levels[self.current_level].player.coin_count
            self.current_level += 1
            self.levels[self.current_level].player.coin_count = self.coins

    def game_loop(self):
        """
        O loop em que o jogo ocorre.
        """
        while True:
            self.input_handler.update()
            if self.game_state == "menu":
                self.load_menu()

            if self.game_state =="playing":
                self.change_level()
                self.screen.blit(pygame.transform.scale(pygame.image.load("media/background/background_frame.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
                self.levels[self.current_level].run()

            if self.player.won == True:
                self.win_counter += 1
                if self.win_counter >= FPS*5:
                    self.reset()

            pygame.display.update()
            self.clock.tick(FPS)