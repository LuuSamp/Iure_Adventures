import pygame
from game.level import Level, BossLevel
from entities.player import Player
from game.input_handler import InputHandler
from game.const import *
from game.menu import Menu
from game.options_menu import OptionsMenu
from game.audio import SFXAudio, MusicAudio

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
        self.music = MusicAudio("./media/sounds/background_music.mp3", volume=0.04)
        self.music.play()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player((0,0))
        self.main_menu = Menu(self.screen)
        self.input_handler = InputHandler(self.player)
        self.levels = [
            (Level, './level/level_1'),
            (BossLevel, './level/boss_level')
        ]
        self.coins = 0
        self.current_level = 0
        self.current_level_obj = None
        self.options_menu = OptionsMenu(self.screen)
        
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
        if self.current_level_obj is None:
            self.current_level_obj = self.levels[self.current_level][0](
                self.screen, self.player, self.levels[self.current_level][1]
                )
            
        if self.current_level_obj.level_completed and self.current_level < len(self.levels) - 1:
            self.coins = self.current_level_obj.player.coin_count
            self.current_level += 1
            self.current_level_obj = self.build_level(self.current_level)
            self.current_level_obj.player.coin_count = self.coins
            
    def build_level(self, idx):
        """
        Constrói o nível atual.
        """
        return self.levels[idx][0](self.screen, self.player, self.levels[idx][1])

    def game_loop(self):
        """
        O loop em que o jogo ocorre.
        """
        while True:
            self.music.update()
            self.input_handler.update()
            if self.game_state == "menu":
                self.load_menu()

            if self.game_state =="playing":
                self.change_level()
                self.current_level_obj.run()

            if self.player.won == True:
                self.win_counter += 1
                if self.win_counter >= FPS*5:
                    self.reset()

            if self.game_state == "options":
                if not self.options_menu.run():
                    self.game_state = "menu"

            pygame.display.update()
            self.clock.tick(FPS)