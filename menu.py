import math
from settings import *

class MainMenu:
    def __init__(self):
        self.bg_image = pygame.image.load(BG_IMAGE_MENU).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        self.font = pygame.font.SysFont(MENU_FONT_PATH, 35, bold=False)
        self.text = "P R E S S  E N T E R  T O  P L A Y"

        self.timer = 0.0

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        self.timer += 0.06
        # adjusting text to the middle
        # font.size(char)[0] Width of the letters in pixels
        total_width = sum([self.font.size(char)[0] for char in self.text])
        start_x = (WIDTH - total_width) / 2
        base_y = HEIGHT * 0.8

        current_x = start_x

        for i, char in enumerate(self.text):
            # MAGIA ANIMACJI XD:
            # math.sin(self.timer) makes the wave
            # + i * 0.5 next letter is later than the one before
            # * 15 pixels up and down
            y_offset = math.sin(self.timer + i * 0.5) * 15
            letter_surface = self.font.render(char, True, 'white')
            screen.blit(letter_surface, (current_x, base_y + y_offset))
            current_x += self.font.size(char)[0]
