import sys
from board import Board
from settings import *
from player import Player
from menu import MainMenu
from options_menu import OptionsMenu
from how_to_play_menu import HowToPlayMenu
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

        self.ui_font = pygame.font.Font(MENU_FONT_PATH, 35)

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
        self.how_to_play_menu = HowToPlayMenu()

        self.state = "menu"
        self.active_bombs = []
        self.is_moving = False

        # Bomb synchronisation
        self.pending_bomb = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "menu":
                clicked_button = self.main_menu.handle_event(event)

                if clicked_button == "JOIN GAME":
                    self.state = "shaking"
                elif clicked_button == "OPTIONS":
                    self.state = "options"
                elif clicked_button == "HOW TO PLAY":
                    self.state = "how_to_play"
                elif clicked_button == "QUIT GAME":
                    pygame.quit()
                    sys.exit()


            elif self.state == "options":
                action = self.options_menu.handle_event(event)
                if action == "GO BACK":
                    self.state = "menu"
            elif self.state == "how_to_play":
                action = self.how_to_play_menu.handle_event(event)
                if action == "GO BACK":
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

                            self.pending_bomb = (new_bomb.x, new_bomb.y)

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
        elif self.state == "how_to_play":
            self.how_to_play_menu.draw(self.screen)
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

        if hasattr(self, 'network') and self.network.all_players_data and self.state not in ["playing", "dying", "shaking", "hatching", "hatching"]:
            text_str = f"PLAYERS: {self.network.connected_players_count}/4"
            text_surface = self.ui_font.render(text_str, True, "white")
            text_rect = text_surface.get_rect(topright=(WIDTH - 20, 20))
            self.screen.blit(text_surface, text_rect)

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