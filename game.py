import pygame
from level import Level, BossLevel
from player import Player
from input_handler import InputHandler
from const import *
from menu import Menu

class Game:
    def __init__(self):
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
    
    def load_level(self):
        return Level(self.screen, self.player)
    
    def run(self):
        self.game_loop()
    
    def load_menu(self):
        self.main_menu.run()
        self.game_state = self.main_menu.game_state
    
    def change_level(self):
        if self.levels[self.current_level].level_completed and self.current_level < len(self.levels) - 1:
            self.coins = self.levels[self.current_level].player.coin_count
            self.current_level += 1
            self.levels[self.current_level].player.coin_count = self.coins

    def game_loop(self):
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
                    self.game_state = "menu"
                    self.player.won = False

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()