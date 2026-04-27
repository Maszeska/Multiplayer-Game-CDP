import pygame
from settings import *
from core.board import Board
from entities.player import Player
from entities.bomb import Bomb
from ui.map_background import MapBackground  # <--- Dodany import tła mapy

#----------------------------------------------------
# Game Scene - Handle game state changes and states of all network objects -> During the main game
#----------------------------------------------------

class GameScene:
    def __init__(self, change_scene_callback, network, map_index):
        self.change_scene = change_scene_callback

        self.map_bg = MapBackground(map_index)
        self.board = Board(map_index)

        self.network = network
        self.player_id = int(self.network.start_pos)

        self._init_player()

        self.enemies = {}
        self.active_bombs = []
        self.is_moving = False
        self.all_players_data = []

        self.game_state = "shaking"

        #  initialising general timer
        self.start_time = pygame.time.get_ticks()
        self.min_game_duration = 3000

        self.dead_players = []
        self.final_ranking = []
        # In method __init__
        self.victory_timer = None
        self.victory_delay = 200

        self.ui_font = pygame.font.Font(MENU_FONT_PATH, 24)


    # --- initialise player's position ---
    def _init_player(self):
        rows = len(self.board.grid)
        cols = len(self.board.grid[0])

        # place players on right positions based on their id
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



    # Handle placing bombs on map - ownership of bombs
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
        return None



    # update game state
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
            self.player.death_frame_index += ANIMATION_SPEED
            if int(self.player.death_frame_index) >= len(self.player.death_frames) - 1:
                self.game_state = "dead"

        self._handle_network()

        if self.game_state == "dead" and self.player_id not in self.dead_players:
            self.dead_players.append(self.player_id)

        # update data about all players
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

                    #                                      --- OPTIONAL: FOR THE PURPOSE OF DEBUGGING ---
                    if (total_players > 1 >= alive_count) or (total_players == 1 and alive_count == 0):
                        if self.victory_timer is None:
                            self.victory_timer = current_time

                        elif current_time - self.victory_timer > self.victory_delay:
                            self.game_state = "game_over"

                            all_ids = {self.player_id}
                            if self.all_players_data:
                                for i, d in enumerate(self.all_players_data):
                                    if d is not None:
                                        all_ids.add(i)

                            winners = [pid for pid in all_ids if pid not in self.dead_players]
                            self.final_ranking = winners + list(reversed(self.dead_players))
                            self.change_scene("end_screen", self.final_ranking)



    def _handle_network(self):
        # Create a list of all active bombs that belong to this player
        my_bombs_data = []
        for bomb in self.active_bombs:
            if getattr(bomb, 'owner', -1) == self.player_id:
                my_bombs_data.append({'x': bomb.x, 'y': bomb.y})
        
        my_data = {
            'x': self.player.x, 'y': self.player.y,
            'is_moving': self.is_moving, 'facing_left': self.player.facing_left,
            'state': self.game_state, 'invulnerable_timer': self.player.invulnerable_timer,
            'bombs': my_bombs_data,
            'lives': self.player.lives,
            'death_frame': self.player.death_frame_index
        }
        try:
            self.all_players_data = self.network.send(my_data)

            if self.all_players_data:
                for i, data in enumerate(self.all_players_data):
                    if i != self.player_id and data is not None:
                        # Process all bombs from this player
                        bombs_data = data.get('bombs', [])
                        for bomb_pos in bombs_data:
                            bx, by = bomb_pos['x'], bomb_pos['y']
                            already_exists = any(b.x == bx and b.y == by for b in self.active_bombs)
                            if not already_exists:
                                enemy_bomb = Bomb(bx, by, self.board.tile_size)
                                enemy_bomb.owner = i
                                self.active_bombs.append(enemy_bomb)
        except Exception as e:
            print("Synchronisation error:", e)

    def draw(self, screen):
        self.map_bg.draw(screen)
        self.board.draw(screen)
        for bomb in self.active_bombs:
            bomb.draw(screen, self.board)

        if self.all_players_data:
            for i, data in enumerate(self.all_players_data):
                if i != self.player_id and data is not None:
                    if 'x' not in data: continue

                    if data.get('state') == "dead":
                        continue

                    if i not in self.enemies:
                        self.enemies[i] = Player(data['x'], data['y'], self.board.tile_size, i)

                    enemy = self.enemies[i]
                    enemy.x, enemy.y = data['x'], data['y']
                    enemy.facing_left = data['facing_left']
                    enemy.invulnerable_timer = data.get('invulnerable_timer', 0)
                    enemy.death_frame_index = data.get('death_frame', 0)

                    enemy.draw(screen, data['state'], data['is_moving'])

        self.draw_player_ui(screen)

        if self.game_state != "dead":
            self.player.draw(screen, self.game_state, self.is_moving)

    def draw_player_ui(self, screen):
        players_hp = {}
        players_hp[self.player_id] = self.player.lives

        if self.all_players_data:
            for i, data in enumerate(self.all_players_data):
                if data is not None and i != self.player_id:
                    players_hp[i] = data.get('lives', 0)

        margin_x, margin_y = 20, 20
        box_w, box_h = 160, 50

        ui_positions = {
            0: (margin_x, margin_y),
            1: (WIDTH - margin_x - box_w, HEIGHT - margin_y - box_h),
            2: (WIDTH - margin_x - box_w, margin_y),
            3: (margin_x, HEIGHT - margin_y - box_h)
        }

        for pid, hp in players_hp.items():
            if pid in ui_positions:
                x, y = ui_positions[pid]

                bg_rect = pygame.Rect(x, y, box_w, box_h)
                bg_surface = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, 150))
                screen.blit(bg_surface, (x, y))
                pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)

                color = (50, 255, 50) if hp > 0 else (255, 50, 50)
                hp_text = f"P{pid + 1} HP: {max(0, hp)}"

                text_surf = self.ui_font.render(hp_text, True, color)
                text_rect = text_surf.get_rect(center=bg_rect.center)
                screen.blit(text_surf, text_rect)