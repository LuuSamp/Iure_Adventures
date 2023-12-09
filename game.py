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
        self.levels = [self.load_level()]
        self.coins = []
        self.current_level = 0
    
    def load_level(self):
        return Level(self.screen, self.player)
    
    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            self.input_handler.update()
            
            self.screen.fill('black')
            self.levels[self.current_level].run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()