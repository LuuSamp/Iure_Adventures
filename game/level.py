import pygame
from game.layout import import_csv_layout
from game.square import StaticSquare, ColisionSquare, CoinSquare, LevelDoor
from entities.player import Player
from entities.enemy import Enemy, EnemyShooter
from game.const import *
from entities.final_boss import FinalBoss
from os import path
from entities.princess import PrincessPinho, Smoke

class Level:
    """Principal fase do jogo a ser carregada.
    """
    def __init__(self, surface:pygame.display, player: Player, level_path='./level/level_1'):
        """Inicializa a fase

        Parameters
        ----------
        surface : pygame.display
            a tela do jogo
        player : Player
            o personagem do jogo
        level_path : str, optional
            o caminho para o arquivo, by default 'level'
        """
        #setup geral
        self.display_surface = surface
        self.player = player
        self.player_group = pygame.sprite.Group(self.player)
        self.level_path = level_path

        self.fonte = pygame.font.Font(None, 36)

        # terrain setup
        terrain_layout = import_csv_layout(f'{level_path}/terrain.csv')
        
        # fall blocks setup
        fall_blocks_layout = import_csv_layout(f'{level_path}/fall_blocks.csv')

        self.terrain_position = pygame.sprite.Group(self.create_terrain(terrain_layout, 'terrain'), self.create_terrain(fall_blocks_layout, 'fall_blocks'))

        # coins 
        coin_layout = import_csv_layout(f'{level_path}/coins.csv')
        self.coin_position = self.create_terrain(coin_layout, 'coins')

        # enemy 
        enemy_layout = import_csv_layout(f'{level_path}/enemies.csv')
        self.bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.enemy_position = self.create_enemies(enemy_layout)

        # decor_door
        decor_door_layout = import_csv_layout(f'{level_path}/decor_door.csv')
        self.decor_door_position = self.create_terrain(decor_door_layout, 'decor_door')

        # princess
        princess_layout = import_csv_layout(f'{level_path}/pinho.csv')
        self.princess_position = self.create_terrain(princess_layout, 'pinho')
        
        # door
        door_layout = import_csv_layout(f'{level_path}/door.csv')
        self.door_position = self.create_terrain(door_layout, 'door')

        player_position = import_csv_layout(f'{level_path}/player.csv')
        self.set_player_position(player_position)

        self.world_shift = 0
        self.first_x = 0
        self.last_x = SQUARE_SIZE * len(terrain_layout[0])

        self.level_completed = False
        self.end_timer = 0

        self.winning_song = pygame.mixer.Sound('./media/sounds/level_completed.mp3')
        self.winning_song.set_volume(0.3)


    def reset(self) -> None:
        """Reseta o nível do início
        """

        self.__init__(self.display_surface, self.player, self.level_path)

    def create_terrain(self, layout, type:str) -> pygame.sprite.Group:
        """Adiciona os elementos ao mapa

        Parameters
        ----------
        layout : _type_
            o layout desejado
        type : str
            tipo dos elementos gerados

        Returns
        -------
        pygame.sprite.Group
            o grupo do terreno gerado
        """
        squares = pygame.sprite.Group()
        self.doors = list()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * SQUARE_SIZE
                    y = row_index * SQUARE_SIZE

                    if type == 'terrain':
                        try:
                            square = StaticSquare(x, y, SQUARE_SIZE, f'./media/blocos/bloco__{val}.png')
                        except:
                            square = ColisionSquare(x, y, SQUARE_SIZE, './media/blocos/bloco__0.png', self.player)
                    elif type == 'fall_blocks':
                        square = ColisionSquare(x, y, SQUARE_SIZE, './media/blocos/bloco_11.png', self.player)
                    elif type == 'coins':
                        square = CoinSquare(x, y, SQUARE_SIZE, './media/coin.png', self.player)
                    elif type == 'door':
                        square = LevelDoor(x, y, SQUARE_SIZE * 2, './media/porta.png', self.player)
                        self.doors.append(square)
                    elif type == 'decor_door':
                        square = ColisionSquare(x, y, SQUARE_SIZE * 2, './media/porta.png', self.player)
                    elif type == "pinho":
                        square = PrincessPinho((x, y))

                    squares.add(square)

        return squares

    def set_player_position(self, layout) -> None:
        """Define a posição inicial do player

        Parameters
        ----------
        layout : _type_
            o layout desejado
        """
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val == "0":
                    x = col_index * SQUARE_SIZE
                    y = row_index * SQUARE_SIZE
                    self.player.rect.center = (x, y)

    def create_enemies(self, layout) -> pygame.sprite.Group:
        """Gera o grupo dos inimigos

        Parameters
        ----------
        layout : _type_
            o layout desejado

        Returns
        -------
        pygame.sprite.Group
            o grupo dos inimigos
        """
        enemies = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * SQUARE_SIZE
                y = row_index * SQUARE_SIZE
                if val == '0':
                    enemies.add(Enemy((x, y)))

                elif val == '2':
                    enemies.add(EnemyShooter((x, y), self.bullet_group))
                
                elif val == '3':
                    enemies.add(FinalBoss((x, y), self.player, self.bullet_group, self.explosion_group))
                    enemies.add(enemies.sprites()[-1].gun)
        
        return enemies
    
    def _update_world_shift(self) -> None:
        """Atualiza o deslocamento horizontal dos elementos
        """
        player_pos = self.player.rect.left
        if player_pos < SCREEN_WIDTH/2 - 50 and self.first_x < 0:
            self.world_shift = 5
        elif player_pos > SCREEN_WIDTH/2 + 50 and self.last_x > SCREEN_WIDTH:
            self.world_shift = -5
        else:
            self.world_shift = 0
        
        self.first_x += self.world_shift
        self.last_x += self.world_shift

    def update_elements(self):
        """Atualiza todos os elementos
        """
        if not self.player.alive(): 
            self.player.reset()
            self.reset()

        self.terrain_position.update(self.world_shift)
        self.enemy_position.update(self.terrain_position, self.world_shift)
        self.coin_position.update(self.world_shift)
        self.door_position.update(self.world_shift)
        self.decor_door_position.update(self.world_shift)
        self.player.collide_with_enemy(self.enemy_position)
        self.player.update(self.terrain_position, self.world_shift)
        self.bullet_group.update(self.player, self.world_shift)
        self.explosion_group.update()
        self.princess_position.update()

    def _draw_coin_text(self):
        """Gera o contador de moedas na tela
        """
        texto = self.fonte.render(f"Coins: {self.player.coin_count}", True, "#f0f8ff")
        text_rect = texto.get_rect(topleft=(10, 10))
        self.display_surface.blit(texto, text_rect)

    def draw_elements(self):
        """Adiciona os elementos a tela
        """
        self.princess_position.draw(self.display_surface)
        self.terrain_position.draw(self.display_surface)
        self.coin_position.draw(self.display_surface)
        self.door_position.draw(self.display_surface)
        self.decor_door_position.draw(self.display_surface)
        self.enemy_position.draw(self.display_surface)
        self.player_group.draw(self.display_surface)
        self.bullet_group.draw(self.display_surface)
        self.explosion_group.draw(self.display_surface)
        self._draw_coin_text()

    def game_run(self):
        """Faz o jogo rodar
        """
        self.draw_elements()
        self._update_world_shift()
        self.update_elements()

    def _check_game_completed(self) -> bool:
        """Checa se o jogo foi completado

        Returns
        -------
        bool
            True caso sim e False caso não
        """
        state = False
        for level_door in self.doors:
            if level_door.level_completed:
                state = True

        return state
    
    def _play_winning_song(self):
        """Toca a música de vitória
        """
        self.winning_song.play()

    def _game_finishing(self):
        """Realiza a cena de finalização do jogo
        """
        self._play_winning_song()
        self.draw_elements()
        self._fill_screen(0.3)
        self.end_timer += 1

        if self.end_timer >= FPS * 1.5:
            self.level_completed = True

    def _fill_screen(self, timer_factor:float, reverse=False):
        """Preenche a tela de preto aos poucos

        Parameters
        ----------
        timer_factor : float
            o fator de velocidade, quanto maior mais lento
        reverse : bool, optional
            Se ele deve escurecer ou clarear, by default False
        """
        fade_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        fade_image.fill("black")
        fade = fade_image.get_rect()
        if reverse:
            fade_alpha = 255 - int(self.end_timer/timer_factor)
        else:
            fade_alpha = int(self.end_timer/timer_factor)

        fade_image.set_alpha(fade_alpha)
        self.display_surface.blit(fade_image, fade)

    def run(self):
        """Faz o jogo rodar
        """
        if not self._check_game_completed():
            self.game_run()
        else:
            self._game_finishing()


class BossLevel(Level):
    """A fase do boss a ser derrotado
    """
    def __init__(self, surface:pygame.display, player: Player, level_path='./level/boss_level'):
        """Inicializa a fase

        Parameters
        ----------
        surface : pygame.display
            a tela do jogo
        player : Player
            o personagem do jogo
        level_path : str, optional
            o caminho para o arquivo, by default 'boss_level'
        """
        super().__init__(surface, player, level_path)

        self.boss = FinalBoss((1250,0), self.player, self.bullet_group, self.explosion_group)

        self.enemy_position.add(self.boss)
        self.enemy_position.add(self.boss.gun)
        self.boss.initial_pos = SQUARE_SIZE * 10
        self.boss.x_vel *= 3
        self.boss.move_range = 1200
        self.started = False

        self.princess = self.princess_position.sprites()[-1]

    def init_run(self):
        self.boss.facing = -1

        self.update_elements()
        self.boss.move_counter = 0
        self.boss.shot_time = 0
        self.draw_elements()

        if self.boss.rect.x <= self.boss.initial_pos: 
            self.boss.move_range = INITIAL_RANGE
            self.boss.x_vel /= 3
            self.player.x_vel = PLAYER_X_VEL
            self.started = True

    def run(self):
        if self.started:
            self.game_run()
        else:
            self.player.x_vel = 0
            self.init_run()
            self.initialized = True

    def _update_world_shift(self) -> None:
        """Atualiza o deslocamento horizontal dos elementos
        """
        self.world_shift = 0
    
    def game_run(self):
        super().game_run()
        if self.boss.health <= 0 and self.princess.animation_list == 0:
            self.princess.change_list()
            self.princess_position.add(Smoke(self.princess.rect.center))