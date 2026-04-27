from settings import *
from ui.base_menu import BaseMenu

#----------------------------------------------------
# How to play screen - just controls
#----------------------------------------------------

class HowToPlayMenu(BaseMenu):
    def __init__(self):
        super().__init__()

        self.instructions_img = pygame.image.load(INSTRUCTION).convert_alpha()
        target_width = int(WIDTH * 0.7)
        aspect_ratio = self.instructions_img.get_height() / self.instructions_img.get_width()
        target_height = int(target_width * aspect_ratio)

        self.instructions_img = pygame.transform.smoothscale(self.instructions_img, (target_width, target_height))
        self.img_rect = self.instructions_img.get_rect(center=(WIDTH // 2, HEIGHT * 0.45))

        self.create_vertical_buttons(button_texts=["GO BACK"], start_y=HEIGHT * 0.80)

    def handle_event(self, event):
        return self.handle_button_event(event, pygame.mouse.get_pos())

    def draw(self, screen):
        self.parallax_bg.draw(screen)
        if self.instructions_img:
            screen.blit(self.instructions_img, self.img_rect)
        self.draw_buttons(screen, pygame.mouse.get_pos())