import pygame
from layout import import_csv_layout
from quadrado import StaticSquare
from platforms import Platform
from const import *
import os
import sys


os.chdir(os.getcwd())

square_size = 64

class Level:
    def __init__(self, surface):
        #setup geral
        self.display_surface = surface
        self.world_shift = 0

        # terrain setup
        terrain_layout = import_csv_layout('level/terrain.csv')
        self.terrain_position = self.create_terrain(terrain_layout, 'terrain')

        # coins 
        coin_layout = import_csv_layout('level/coins.csv')
        self.coin_position = self.create_terrain(coin_layout, 'coins')

        # enemy 
        enemy_layout = import_csv_layout('level/enemies.csv')
        self.enemy_position = self.create_terrain(enemy_layout, 'enemies')

    def create_terrain(self, layout, type):
        squares = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * square_size
                    y = row_index * square_size

                    if type == 'terrain':
                        square = StaticSquare(x, y, square_size, './imagens/madeira.jpg')
                    if type == 'coins':
                        square = StaticSquare(x, y, square_size, './imagens/coin.png')
                    if type == 'enemies':
                        square = StaticSquare(x, y, square_size, './imagens/mario.png')

                    squares.add(square)

        return squares

    def update_elements(self):
        self.terrain_position.update(self.world_shift)
        self.enemy_position.update(self.world_shift)
        self.coin_position.update(self.world_shift)

    def draw_elements(self):
        self.terrain_position.draw(self.display_surface)
        self.enemy_position.draw(self.display_surface)
        self.coin_position.draw(self.display_surface)

    def run(self):
            self.draw_elements()
            self.update_elements()


class TestLevel(Level):
    def __init__(self) -> None:
        super().__init__()
        
        for block in range(20):
            self.platform_list.add(Platform(*DIM_ENTITY, (32*block, 264)))
        for block in range(20):
            self.platform_list.add(Platform(*DIM_ENTITY, (128*block, 200)))
