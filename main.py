import os

from game.resource import base_path

os.chdir(base_path())

from game.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
