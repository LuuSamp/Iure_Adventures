import pygame
from level import Level, BossLevel
from player import Player
from input_handler import InputHandler
from const import *
from menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player((0,0))
        self.main_menu = Menu(self.screen)
        self.input_handler = InputHandler(self.player)
        self.levels = [Level(self.screen, self.player), BossLevel(self.screen, self.player)]
        self.coins = 0
        self.current_level = 0
        self.game_state = "menu"
    
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
                self.screen.fill('black')
                self.levels[self.current_level].run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()