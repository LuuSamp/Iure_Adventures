import pygame
from layout import import_csv_layout
from quadrado import StaticSquare
from player import Player
from enemy import Enemy, EnemyShooter
from const import *
import os
import sys


os.chdir(os.getcwd())

square_size = 64

class Level:
    def __init__(self, surface, player: Player):
        #setup geral
        self.display_surface = surface
        self.world_shift = 0
        self.player = player
        self.player_group = pygame.sprite.Group(self.player)
        
        # terrain setup
        terrain_layout = import_csv_layout('level/terrain.csv')
        self.terrain_position = self.create_terrain(terrain_layout, 'terrain')

        # coins 
        coin_layout = import_csv_layout('level/coins.csv')
        self.coin_position = self.create_terrain(coin_layout, 'coins')

        # enemy 
        enemy_layout = import_csv_layout('level/enemies.csv')
        self.enemy_position = self.create_enemies(enemy_layout)

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

                    squares.add(square)

        return squares

    def create_enemies(self, layout):
        enemies = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * square_size
                    y = row_index * square_size

                    enemies.add(Enemy((x, y)))
        
        return enemies

    def update_elements(self):
        self.terrain_position.update(self.world_shift)
        self.enemy_position.update(self.terrain_position, self.world_shift)
        self.coin_position.update(self.world_shift)
        self.player.update(self.terrain_position, self.world_shift)

    def draw_elements(self):
        self.terrain_position.draw(self.display_surface)
        self.enemy_position.draw(self.display_surface)
        self.coin_position.draw(self.display_surface)
        self.player_group.draw(self.display_surface)
        self.player.collide_with_enemy(self.enemy_position)

    def run(self):
            self.draw_elements()
            self.update_elements()
