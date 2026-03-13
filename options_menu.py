from settings import *
import math

class OptionsMenu:
    def __init__(self):
        self.bg_image = pygame.image.load(BG_IMAGE_MENU).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        self.font = pygame.font.SysFont(MENU_FONT_PATH, 50, bold=True)
        self.small_font = pygame.font.SysFont(MENU_FONT_PATH, 35, bold=True)

        self.volume = 50
        self.timer = 0.0

        pygame.mixer.music.set_volume(self.volume / 100.0)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        action = button["action"]

                        if action == "MINUS" and self.volume > 0:
                            self.volume -= 10
                            self.update_volume()
                        elif action == "PLUS" and self.volume < 100:
                            self.volume += 10
                            self.update_volume()
                        elif action == "BACK":
                            return "BACK"
        return None

    def update_volume(self):
        vol_float = self.volume / 100.0
        pygame.mixer.music.set_volume(vol_float)

        from bomb import Bomb
        if Bomb.explosion_sound:
            Bomb.explosion_sound.set_volume(vol_float)

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        self.timer += 0.1
        mouse_pos = pygame.mouse.get_pos()
        self.buttons = []

        vol_text = f"VOLUME: {self.volume}%"
        vol_surface = self.font.render(vol_text, True, 'white')
        vol_x = (WIDTH - vol_surface.get_width()) // 2
        screen.blit(vol_surface, (vol_x, HEIGHT * 0.4))

        minus_text = "[ - ]"
        minus_surface = self.font.render(minus_text, True, 'yellow' if self._is_hovered(mouse_pos, vol_x, HEIGHT * 0.55,
                                                                                        minus_text) else 'white')
        minus_rect = screen.blit(minus_surface, (vol_x, HEIGHT * 0.55))
        self.buttons.append({"action": "MINUS", "rect": minus_rect})

        plus_text = "[ + ]"
        plus_surface = self.font.render(plus_text, True,
                                        'yellow' if self._is_hovered(mouse_pos, vol_x + 150, HEIGHT * 0.55,
                                                                     plus_text) else 'white')
        plus_rect = screen.blit(plus_surface, (vol_x + 150, HEIGHT * 0.55))
        self.buttons.append({"action": "PLUS", "rect": plus_rect})

        back_text = "BACK"
        back_x = (WIDTH - self.font.size(back_text)[0]) // 2
        back_y = HEIGHT * 0.8

        is_back_hovered = self._is_hovered(mouse_pos, back_x, back_y, back_text)
        y_offset = math.sin(self.timer * 2) * 8 if is_back_hovered else 0

        back_surface = self.font.render(back_text, True, 'yellow' if is_back_hovered else 'white')
        back_rect = screen.blit(back_surface, (back_x, back_y + y_offset))
        self.buttons.append({"action": "BACK", "rect": pygame.Rect(back_x, back_y, back_rect.width, back_rect.height)})

    def _is_hovered(self, mouse_pos, x, y, text):
        rect = pygame.Rect(x, y, self.font.size(text)[0], self.font.size(text)[1])
        return rect.collidepoint(mouse_pos)