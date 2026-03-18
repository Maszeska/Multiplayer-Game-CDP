import pygame
from settings import *
from core.board import Board
from entities.player import Player
from entities.bomb import Bomb


class GameScene:
    def __init__(self, change_scene_callback, network, map_index):
        self.change_scene = change_scene_callback
        self.board = Board(BOARDS[map_index])
        self.network = network
        self.player_id = int(self.network.start_pos)

        self._init_player()

        self.enemies = {}
        self.active_bombs = []
        self.is_moving = False
        self.pending_bomb = None
        self.all_players_data = []

        self.game_state = "shaking"

        self.start_time = pygame.time.get_ticks()
        self.min_game_duration = 3000

        self.dead_players = []
        self.final_ranking = []
        # W metodzie __init__
        self.victory_timer = None
        self.victory_delay = 4000

    def _init_player(self):
        rows = len(self.board.grid)
        cols = len(self.board.grid[0])

        if self.player_id == 0:
            grid_x, grid_y = 1, 1
        elif self.player_id == 1:
            grid_x, grid_y = cols - 2, rows - 2
        elif self.player_id == 2:
            grid_x, grid_y = cols - 2, 1
        else:
            grid_x, grid_y = 1, rows - 2

        start_x = self.board.offset_x + (grid_x * self.board.tile_size)
        start_y = self.board.offset_y + (grid_y * self.board.tile_size)

        self.player = Player(start_x, start_y, self.board.tile_size, self.player_id)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_state == "playing":
                if event.key == pygame.K_SPACE:
                    my_bombs = [b for b in self.active_bombs if getattr(b, 'owner', -1) == self.player_id]
                    if len(my_bombs) < 2:
                        new_bomb = self.player.drop_bomb(self.board)
                        if new_bomb:
                            new_bomb.owner = self.player_id
                            self.active_bombs.append(new_bomb)
                            self.pending_bomb = (new_bomb.x, new_bomb.y)
        return None

    def update(self):
        self.is_moving = False
        current_time = pygame.time.get_ticks()

        if self.game_state == "playing":
            self.player.update_timers()

        for bomb in self.active_bombs:
            bomb.update(self.board)
            if bomb.state == "exploding":
                player_pos = self.player.get_grid_pos(self.board)
                if player_pos in bomb.blast_tiles:
                    self.player.take_damage()

        self.active_bombs = [bomb for bomb in self.active_bombs if bomb.state != "done"]

        if self.game_state == "playing" and self.player.lives <= 0:
            self.game_state = "dying"

        if self.game_state == "shaking":
            if self.player.shake_timer >= SHAKE_DURATION:
                self.game_state = "hatching"
            else:
                self.player.shake_timer += 1
        elif self.game_state == "hatching":
            self.player.hatch_frame_index += HATCH_SPEED
            if int(self.player.hatch_frame_index) >= len(self.player.hatch_frames):
                self.game_state = "playing"
        elif self.game_state == "playing":
            self.is_moving = self.player.move(self.board)
        elif self.game_state == "dying":
            self.player.death_frame_index += PLAYER_SPEED
            if int(self.player.death_frame_index) >= len(self.player.death_frames) - 1:
                self.game_state = "dead"

        self._handle_network()

        if self.game_state == "dead" and self.player_id not in self.dead_players:
            self.dead_players.append(self.player_id)

        if self.all_players_data:
            for i, data in enumerate(self.all_players_data):
                if data and data.get('state') == "dead" and i not in self.dead_players:
                    self.dead_players.append(i)

                if self.game_state not in ["game_over", "menu"] and (
                        current_time - self.start_time > self.min_game_duration):
                    total_players = self.network.connected_players_count
                    active_states = ["playing", "shaking", "dying", "hatching"]
                    alive_count = 0

                    if self.game_state in active_states:
                        alive_count += 1

                    if self.all_players_data:
                        for i, data in enumerate(self.all_players_data):
                            if i != self.player_id and data is not None and 'state' in data:
                                if data.get('state') in active_states:
                                    alive_count += 1

                    if (total_players > 1 >= alive_count) or (total_players == 1 and alive_count == 0):
                        if self.victory_timer is None:
                            self.victory_timer = current_time

                        elif current_time - self.victory_timer > self.victory_delay:
                            self.game_state = "game_over"

                            # --- FIX RANKINGU: Używamy set(), żeby nie było duplikatów ---
                            all_ids = {self.player_id}
                            if self.all_players_data:
                                for i, d in enumerate(self.all_players_data):
                                    if d is not None:
                                        all_ids.add(i)

                            # Zwycięzcy (ci, których nie ma w dead_players)
                            winners = [pid for pid in all_ids if pid not in self.dead_players]

                            # Ostateczna lista: Zwycięzca (lub zwycięzcy) + reszta w odwrotnej kolejności zgonów
                            self.final_ranking = winners + list(reversed(self.dead_players))

                            self.change_scene("end_screen", self.final_ranking)

    def _handle_network(self):
        my_data = {
            'x': self.player.x, 'y': self.player.y,
            'is_moving': self.is_moving, 'facing_left': self.player.facing_left,
            'state': self.game_state, 'invulnerable_timer': self.player.invulnerable_timer,
            'bomb_event': self.pending_bomb
        }
        try:
            self.all_players_data = self.network.send(my_data)
            self.pending_bomb = None

            if self.all_players_data:
                for i, data in enumerate(self.all_players_data):
                    if i != self.player_id and data is not None:
                        bomb_pos = data.get('bomb_event')
                        if bomb_pos:
                            bx, by = bomb_pos
                            already_exists = any(b.x == bx and b.y == by for b in self.active_bombs)
                            if not already_exists:
                                enemy_bomb = Bomb(bx, by, self.board.tile_size)
                                enemy_bomb.owner = i
                                self.active_bombs.append(enemy_bomb)
        except Exception as e:
            print("Błąd synchronizacji:", e)

    def draw(self, screen):
        self.board.draw(screen)

        for bomb in self.active_bombs:
            bomb.draw(screen, self.board)

        # 1. Rysowanie przeciwników
        if self.all_players_data:
            for i, data in enumerate(self.all_players_data):
                if i != self.player_id and data is not None:
                    if 'x' not in data: continue

                    # Jeśli wróg jest "dead", po prostu go nie rysujemy (znika)
                    if data.get('state') == "dead":
                        continue

                    if i not in self.enemies:
                        self.enemies[i] = Player(data['x'], data['y'], self.board.tile_size, i)

                    enemy = self.enemies[i]
                    enemy.x, enemy.y = data['x'], data['y']
                    enemy.facing_left = data['facing_left']
                    enemy.invulnerable_timer = data.get('invulnerable_timer', 0)

                    # Rysujemy normalnie (jeśli stan to "dying", odegra animację i zniknie w następnej klatce)
                    enemy.draw(screen, data['state'], data['is_moving'])

        # 2. Rysowanie lokalnego gracza (Ciebie)
        # Rysujemy tylko, jeśli nie jesteśmy martwi
        if self.game_state != "dead":
            self.player.draw(screen, self.game_state, self.is_moving)