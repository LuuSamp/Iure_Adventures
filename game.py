import pygame
from level import Level, BossLevel
from player import Player
from input_handler import InputHandler
from const import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player((0,0))
        self.input_handler = InputHandler(self.player)
        self.levels = [BossLevel(self.screen, self.player)]
        self.coins = 0
        self.current_level = 0
        self.game_state = "playing"
    
    def load_level(self):
        return Level(self.screen, self.player)
    
    def run(self):
        self.game_loop()
    
    def load_menu(self):
        pass
    
    def change_level(self):
        if self.levels[self.current_level].level_completed and self.current_level < len(self.levels) - 1:
            self.coins = self.levels[self.current_level].player.coin_count
            self.current_level += 1
            self.levels[self.current_level].player.coin_count = self.coins

    def game_loop(self):
        while True:
            self.input_handler.update()
            self.change_level()
            self.screen.fill('black')
            self.levels[self.current_level].run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()