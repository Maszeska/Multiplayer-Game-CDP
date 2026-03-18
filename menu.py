import math
from settings import *
from parallax_background import ParallaxBackground


class MainMenu:
    def __init__(self):
        self.parallax_bg = ParallaxBackground(LAYER_CONFIG)

        self.bg_title = pygame.image.load("assets/background/bg_title.png").convert_alpha()
        self.bg_title = pygame.transform.scale(self.bg_title, (WIDTH, HEIGHT))

        self.font_max = pygame.font.Font(MENU_FONT_PATH, 45)

        self.options = ["JOIN GAME", "OPTIONS", "HOW TO PLAY", "QUIT GAME"]
        self.buttons = []
        self.timer = 0.0

        self._calculate_buttons()

    def _calculate_buttons(self):
        start_y = HEIGHT * 0.4
        gap = 80

        temp_font = pygame.font.Font(MENU_FONT_PATH, 50)

        for i, text in enumerate(self.options):
            text_width, text_height = temp_font.size(text)
            x = 130
            y = start_y + (i * gap)

            rect = pygame.Rect(x, y, text_width, text_height)

            self.buttons.append({
                "text": text,
                "rect": rect,
                "centery": rect.centery,
                "scale": 0.83
            })

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        return button["text"]
        return None

    def draw(self, screen):
        self.parallax_bg.draw(screen)

        screen.blit(self.bg_title, (0, 0))

        self.timer += 0.1
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            text = button["text"]
            rect = button["rect"]

            is_hover = rect.collidepoint(mouse_pos)

            target_scale = 1.0 if is_hover else 0.83

            button["scale"] += (target_scale - button["scale"]) * 0.15

            color = (52, 107, 211) if is_hover else "white"
            text_surface = self.font_max.render(text, True, color)

            new_width = int(text_surface.get_width() * button["scale"])
            new_height = int(text_surface.get_height() * button["scale"])
            scaled_surface = pygame.transform.smoothscale(text_surface, (new_width, new_height))


            draw_rect = scaled_surface.get_rect(x=rect.x, centery=button["centery"])

            screen.blit(scaled_surface, draw_rect)