import sys
from settings import *

from ui.main_menu import MainMenu
from ui.options_menu import OptionsMenu
from ui.how_to_play_menu import HowToPlayMenu
from ui.lobby import Lobby
from ui.end_screen import EndScreen
from core.game_scene import GameScene
from core.network import Network

#----------------------------------------------------
# BOOM-IT main game loop
#----------------------------------------------------

def load_assets():
    try:
        game_icon = pygame.image.load(ICON_PATH).convert_alpha()
        pygame.display.set_icon(game_icon)
    except pygame.error:
        pass

    try:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Boomit!")
        self.timer = pygame.time.Clock()

        self.ui_font = pygame.font.Font(MENU_FONT_PATH, 35)

        # initialise Network object
        self.network = Network()

        load_assets()

        self.scenes = {
            "menu": MainMenu(),
            "options": OptionsMenu(),
            "how_to_play": HowToPlayMenu(),
            "lobby": None,
            "game": None,
            "end_screen": None
        }

        self.current_scene_name = "menu"


    def change_scene(self, scene_name, scene_data=None):
        if scene_name == "lobby":
            if self.scenes["lobby"] is None:
                self.scenes["lobby"] = Lobby(self.change_scene, self.network)
            # Reset map selection for new round
            self.scenes["lobby"].reset_map_selection()

        elif scene_name == "game":
            self.scenes["game"] = GameScene(self.change_scene, self.network, scene_data)

        elif scene_name == "end_screen":
            self.scenes["end_screen"] = EndScreen(self.change_scene, scene_data)

        self.current_scene_name = scene_name



    # while in menu -> change window when click navigation button
    def handle_events(self):
        current_scene = self.scenes[self.current_scene_name]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            action = current_scene.handle_event(event)

            if action:
                if action == "JOIN GAME":
                    self.change_scene("lobby")
                elif action == "OPTIONS":
                    self.change_scene("options")
                elif action == "HOW TO PLAY":
                    self.change_scene("how_to_play")
                elif action == "GO BACK":
                    self.change_scene("menu")
                elif action == "QUIT GAME":
                    pygame.quit()
                    sys.exit()


    #update scene
    def update(self):
        current_scene = self.scenes[self.current_scene_name]
        if hasattr(current_scene, "update"):
            current_scene.update()



    # draw scene
    def draw(self):
        current_scene = self.scenes[self.current_scene_name]
        current_scene.draw(self.screen)

        if self.current_scene_name in ["menu", "options", "how_to_play"] and self.network:
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
    game = Main()
    game.run()