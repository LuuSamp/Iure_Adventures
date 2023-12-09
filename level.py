import pygame
from layout import import_csv_layout
from quadrado import StaticSquare, ColisionSquare, CoinSquare, LevelDoor
from player import Player
from enemy import Enemy, EnemyShooter
from const import *
import os
import sys


os.chdir(os.getcwd())

class Level:
    def __init__(self, surface, player: Player, level_path='level'):
        #setup geral
        self.display_surface = surface
        self.player = player
        self.player_group = pygame.sprite.Group(self.player)

        self.fonte = pygame.font.Font(None, 36)

        # terrain setup
        terrain_layout = import_csv_layout(f'{level_path}/terrain.csv')
        self.terrain_position = self.create_terrain(terrain_layout, 'terrain')

        # coins 
        coin_layout = import_csv_layout(f'{level_path}/coins.csv')
        self.coin_position = self.create_terrain(coin_layout, 'coins')

        # enemy 
        enemy_layout = import_csv_layout(f'{level_path}/enemies.csv')
        self.bullet_group = pygame.sprite.Group()
        self.enemy_position = self.create_enemies(enemy_layout)

        self.world_shift = 0
        self.first_x = 0
        self.last_x = SQUARE_SIZE * len(terrain_layout[0])

        self.level_completed = False

    def create_terrain(self, layout, type):
        squares = pygame.sprite.Group()
        self.doors = list()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * SQUARE_SIZE
                    y = row_index * SQUARE_SIZE

                    if type == 'terrain':
                        square = StaticSquare(x, y, SQUARE_SIZE, './imagens/madeira.jpg')
                    elif type == 'fall_block':
                        square = ColisionSquare(x, y, SQUARE_SIZE, './imagens/madeira.jpg', self.player)
                    elif type == 'coins':
                        square = CoinSquare(x, y, SQUARE_SIZE, './imagens/coin.png', self.player)
                    elif type == 'door':
                        square = LevelDoor(x, y, SQUARE_SIZE, './imagens/coin.png', self.player)
                        self.doors.append(square)

                    squares.add(square)

        return squares

    def create_enemies(self, layout):
        enemies = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * SQUARE_SIZE
                y = row_index * SQUARE_SIZE
                if val == '0':
                    enemies.add(Enemy((x, y)))

                elif val == '1':
                    enemies.add(EnemyShooter((x, y), self.bullet_group))
        
        return enemies
    
    def _update_world_shift(self):
        player_pos = self.player.rect.left
        if player_pos < 100 and self.first_x < 0:
            self.world_shift = 5
        elif player_pos > 400 and self.last_x > SCREEN_WIDTH:
            self.world_shift = -5
        else:
            self.world_shift = 0
        
        self.first_x += self.world_shift
        self.last_x += self.world_shift
        # print("First", self.first_x)
        # print("Last", self.last_x)

    def update_elements(self):
        self.terrain_position.update(self.world_shift)
        self.enemy_position.update(self.terrain_position, self.world_shift)
        self.coin_position.update(self.world_shift)
        self.player.collide_with_enemy(self.enemy_position)
        self.player.update(self.terrain_position, self.world_shift)
        self.bullet_group.update(self.player, self.world_shift)

    def _draw_coin_text(self):
        texto = self.fonte.render(f"Coins: {self.player.coin_count}", True, "#f0f8ff")
        text_rect = texto.get_rect(topleft=(10, 10))
        self.display_surface.blit(texto, text_rect)

    def draw_elements(self):
        self.terrain_position.draw(self.display_surface)
        self.coin_position.draw(self.display_surface)
        self.enemy_position.draw(self.display_surface)
        self.player_group.draw(self.display_surface)
        self.bullet_group.draw(self.display_surface)
        self._draw_coin_text()

    def run(self):
        self.draw_elements()
        self._update_world_shift()
        self.update_elements()

        for level_door in self.doors:
            if level_door.level_completed:
                self.level_completed = True


class BossLevel(Level):
    def __init__(self, surface, player: Player, level_path='boss_level'):
        super().__init__(surface, player, level_path)

    def run(self):
        self.draw_elements()
        self.update_elements()
