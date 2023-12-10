import os
os.chdir(os.getcwd())

from game.game import Game

game = Game()
game.run()
