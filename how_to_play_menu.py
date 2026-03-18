import pygame
import os
from settings import *
from parallax_background import ParallaxBackground


class HowToPlayMenu:
    def __init__(self):
        self.parallax_bg = ParallaxBackground(LAYER_CONFIG)

        self.font_max = pygame.font.Font(MENU_FONT_PATH, 45)

        self.timer = 0.0
        self.buttons = []

        try:
            self.instructions_img = pygame.image.load(INSTRUCTION).convert_alpha()

            target_width = int(WIDTH * 0.7)
            aspect_ratio = self.instructions_img.get_height() / self.instructions_img.get_width()
            target_height = int(target_width * aspect_ratio)

            self.instructions_img = pygame.transform.smoothscale(self.instructions_img, (target_width, target_height))

            self.img_rect = self.instructions_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.45))
        except pygame.error:
            print(f"Nie udało się załadować obrazka instrukcji z: {INSTRUCTION}")
            self.instructions_img = None

        self._calculate_buttons()

    def _calculate_buttons(self):
        self.buttons = []
        temp_font = pygame.font.Font(MENU_FONT_PATH, 45)

        left_x = 130
        bottom_y = HEIGHT * 0.80

        goback_w, goback_h = temp_font.size("GO BACK")
        btn_goback = pygame.Rect(left_x, bottom_y, goback_w, goback_h)

        self.buttons.append({
            "action": "GO BACK",
            "text": "GO BACK",
            "rect": btn_goback,
            "centery": btn_goback.centery,
            "scale": 0.83
        })

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["action"] == "GO BACK":
                        return "GO BACK"
        return None

    def draw(self, screen):
        self.parallax_bg.draw(screen)

        self.timer += 0.1
        mouse_pos = pygame.mouse.get_pos()

        if self.instructions_img:
            screen.blit(self.instructions_img, self.img_rect)

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