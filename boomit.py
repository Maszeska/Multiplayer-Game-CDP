import sys
from board import Board
from settings import *
from player import Player
from menu import MainMenu
from options_menu import OptionsMenu
from network import Network
from bomb import Bomb

def load_assets():
    try:
        game_icon = pygame.image.load(ICON_PATH).convert_alpha()
        pygame.display.set_icon(game_icon)
    except pygame.error:
        print("Nie udało się załadować ikonki okna.")

    try:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Nie znaleziono pliku muzycznego, gra uruchomi się bez dźwięku.")


class BoomIt:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()


        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Boomit!")
        self.timer = pygame.time.Clock()

        load_assets()

        self.board = Board(BOARD)

        print("Łączenie z serwerem...")
        self.network = Network()

        self.player_id = int(self.network.start_pos)
        print(f"Jestem graczem numer: {self.player_id}")

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
        self.enemies = {}
        self.main_menu = MainMenu()
        self.options_menu = OptionsMenu()

        self.state = "menu"
        self.active_bombs = []
        self.is_moving = False

        # Bomb synchronisation
        self.bombs_dropped = 0
        self.last_bomb_pos = (0, 0)
        self.enemies_bomb_count = {0: 0, 1: 0, 2: 0, 3: 0}

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "menu":
                clicked_button = self.main_menu.handle_event(event)
                if clicked_button == "PLAY":
                    self.state = "shaking"
                elif clicked_button == "OPTIONS":
                    self.state = "options"

            elif self.state == "options":
                clicked_button = self.options_menu.handle_event(event)
                if clicked_button == "BACK":
                    self.state = "menu"

            elif event.type == pygame.KEYDOWN:
                if self.state == "playing":
                    if event.key == pygame.K_SPACE:
                        my_bombs = [b for b in self.active_bombs if
                                    getattr(b, 'owner', self.player_id) == self.player_id]

                        if len(my_bombs) < 2:
                            new_bomb = self.player.drop_bomb(self.board)
                            new_bomb.owner = self.player_id
                            self.active_bombs.append(new_bomb)

                            self.bombs_dropped += 1
                            self.last_bomb_pos = (new_bomb.x, new_bomb.y)

    def update(self):
        self.is_moving = False

        if self.state not in ("menu", "options"):

            if self.state == "playing":
                self.player.update_timers()

            # Setting bombs for explosion
            for bomb in self.active_bombs:
                bomb.update(self.board)

                if bomb.state == "exploding":
                    player_pos = self.player.get_grid_pos(self.board)
                    if player_pos in bomb.blast_tiles:
                        self.player.take_damage()

            # Deleting bombs which have exploded already
            self.active_bombs = [bomb for bomb in self.active_bombs if bomb.state != "done"]

            if self.state == "playing" and self.player.lives <= 0:
                self.state = "dying"

            if self.state == "shaking":
                if self.player.shake_timer >= SHAKE_DURATION:
                    self.state = "hatching"
                else:
                    self.player.shake_timer += 1
            elif self.state == "hatching":
                if int(self.player.hatch_frame_index) >= len(self.player.hatch_frames):
                    self.state = "playing"
            elif self.state == "playing":
                self.is_moving = self.player.move(self.board)
            elif self.state == "dying":
                if int(self.player.death_frame_index) >= len(self.player.death_frames) - 1:
                    self.state = "game_over"

            # Handle multiplayer updates
            my_data = {
                'x': self.player.x,
                'y': self.player.y,
                'is_moving': self.is_moving,
                'facing_left': self.player.facing_left,
                'state': self.state,
                'invulnerable_timer': self.player.invulnerable_timer,
                'bombs_dropped': self.bombs_dropped,
                'last_bomb_pos': self.last_bomb_pos
            }
            try:
                self.all_players_data = self.network.send(my_data)

                if self.all_players_data:
                    for i, data in enumerate(self.all_players_data):
                        if i != self.player_id and data is not None:
                            enemy_bomb_count = data.get('bombs_dropped', 0)

                            if enemy_bomb_count > self.enemies_bomb_count.get(i, 0):
                                self.enemies_bomb_count[i] = enemy_bomb_count

                                bx, by = data.get('last_bomb_pos', (0, 0))
                                enemy_bomb = Bomb(bx, by, self.board.tile_size)
                                enemy_bomb.owner = i

                                self.active_bombs.append(enemy_bomb)
            except Exception as e:
                print("Błąd synchronizacji:", e)

    def draw(self):
        if self.state == "menu":
            self.main_menu.draw(self.screen)
        elif self.state == "options":
            self.options_menu.draw(self.screen)
        else:
            self.board.draw(self.screen)

            for bomb in self.active_bombs:
                bomb.draw(self.screen, self.board)

            if hasattr(self, 'all_players_data') and self.all_players_data:
                for i, data in enumerate(self.all_players_data):
                    if i != self.player_id and data is not None:

                        if i not in self.enemies:
                            self.enemies[i] = Player(data['x'], data['y'], self.board.tile_size, i)

                        enemy = self.enemies[i]
                        enemy.x = data['x']
                        enemy.y = data['y']
                        enemy.facing_left = data['facing_left']

                        enemy.invulnerable_timer = data.get('invulnerable_timer', 0)

                        enemy.draw(self.screen, data['state'], data['is_moving'])

            self.player.draw(self.screen, self.state, self.is_moving)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.timer.tick(FPS)


if __name__ == "__main__":
    game = BoomIt()
    game.run()