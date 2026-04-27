import pygame
from settings import *
from ui.parallax_background import ParallaxBackground

#----------------------------------------------------
# Basic form of menu window - Abstract Class
#----------------------------------------------------

class BaseMenu:
    def __init__(self):
        self.parallax_bg = ParallaxBackground(LAYER_CONFIG)
        self.font_max = pygame.font.Font(MENU_FONT_PATH, 45)
        self.buttons = []
        self.timer = 0.0

    def add_button(self, action, text, rect):
        self.buttons.append({
            "action": action,
            "text": text,
            "rect": rect,
            "centery": rect.centery,
            "scale": 0.83
        })

    def create_vertical_buttons(self, button_texts, start_y, gap=80, x_pos=130):
        temp_font = pygame.font.Font(MENU_FONT_PATH, 50)

        for i, text in enumerate(button_texts):
            text_width, text_height = temp_font.size(text)
            y = start_y + (i * gap)
            rect = pygame.Rect(x_pos, y, text_width, text_height)
            self.add_button(action=text, text=text, rect=rect)

    def handle_button_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    return button["action"]
        return None

    def draw_buttons(self, screen, mouse_pos):
        self.timer += 0.1
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            target_scale = 1.0 if is_hover else 0.83

            button["scale"] += (target_scale - button["scale"]) * 0.15

            color = (52, 107, 211) if is_hover else "white"
            text_surface = self.font_max.render(button["text"], True, color)

            new_width = int(text_surface.get_width() * button["scale"])
            new_height = int(text_surface.get_height() * button["scale"])
            scaled_surface = pygame.transform.smoothscale(text_surface, (new_width, new_height))

            draw_rect = scaled_surface.get_rect(x=button["rect"].x, centery=button["centery"])
            screen.blit(scaled_surface, draw_rect)