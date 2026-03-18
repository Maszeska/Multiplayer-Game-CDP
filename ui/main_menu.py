from settings import *
from ui.base_menu import BaseMenu


class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__()

        self.bg_title = pygame.image.load(BG_TITLE_PATH).convert_alpha()
        self.bg_title = pygame.transform.scale(self.bg_title, (WIDTH, HEIGHT))

        self.create_vertical_buttons(
            button_texts=["JOIN GAME", "OPTIONS", "HOW TO PLAY", "QUIT GAME"],
            start_y=HEIGHT * 0.4
        )

    def handle_event(self, event):
        return self.handle_button_event(event, pygame.mouse.get_pos())

    def draw(self, screen):
        self.parallax_bg.draw(screen)
        screen.blit(self.bg_title, (0, 0))
        self.draw_buttons(screen, pygame.mouse.get_pos())