import math
import pygame
from settings import *


class MainMenu:
    def __init__(self):
        self.bg_image = pygame.image.load(BG_IMAGE_MENU).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        self.font = pygame.font.SysFont(MENU_FONT_PATH, 50, bold=True)
        self.options = ["PLAY", "OPTIONS"]
        self.buttons = []
        self.timer = 0.0

        self._calculate_buttons()

    def _calculate_buttons(self):
        start_y = HEIGHT * 0.6
        gap = 80

        for i, text in enumerate(self.options):
            text_width, text_height = self.font.size(text)
            x = (WIDTH - text_width) // 2
            y = start_y + (i * gap)

            rect = pygame.Rect(x, y, text_width, text_height)
            self.buttons.append({"text": text, "rect": rect})

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        return button["text"]
        return None

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        self.timer += 0.1

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            text = button["text"]
            rect = button["rect"]

            is_hovered = rect.collidepoint(mouse_pos)
            color = "yellow" if is_hovered else "white"

            y_offset = math.sin(self.timer * 2) * 8 if is_hovered else 0

            text_surface = self.font.render(text, True, color)
            screen.blit(text_surface, (rect.x, rect.y + y_offset))