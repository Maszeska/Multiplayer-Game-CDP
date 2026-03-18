import pygame
from settings import *
from parallax_background import ParallaxBackground
from bomb import Bomb


class OptionsMenu:
    def __init__(self):
        self.parallax_bg = ParallaxBackground(LAYER_CONFIG)

        self.font_max = pygame.font.Font(MENU_FONT_PATH, 45)
        self.font_labels = pygame.font.Font(MENU_FONT_PATH, 40)

        if not Bomb.sound_loaded:
            try:
                Bomb.explosion_sound = pygame.mixer.Sound(BOOM_SOUND_PATH)
                Bomb.sound_loaded = True
            except pygame.error:
                print("Nie udało się załadować pliku z dźwiękiem wybuchu.")

        self.music_volume = 50
        self.bomb_volume = 50

        self._apply_volumes()

        self.timer = 0.0
        self.buttons = []

        self.slider_x = 520
        self.slider_width = 300
        self.slider_height = 10
        self.handle_radius = 15

        self.music_y = HEIGHT * 0.3 + 20
        self.bomb_y = HEIGHT * 0.45 + 20

        self.dragging_music = False
        self.dragging_bomb = False

        self._calculate_buttons()

    def _apply_volumes(self):
        pygame.mixer.music.set_volume(self.music_volume / 100.0)
        if Bomb.explosion_sound:
            Bomb.explosion_sound.set_volume(self.bomb_volume / 100.0)

    def _calculate_buttons(self):
        self.buttons = []
        temp_font = pygame.font.Font(MENU_FONT_PATH, 45)

        left_x = 130
        bottom_y = HEIGHT * 0.70

        reset_w, reset_h = temp_font.size("RESET")
        goback_w, goback_h = temp_font.size("GO BACK")

        btn_reset = pygame.Rect(left_x, bottom_y, reset_w, reset_h)
        btn_goback = pygame.Rect(left_x, bottom_y + 80, goback_w, goback_h)

        self._add_button("RESET", "RESET", btn_reset)
        self._add_button("GO BACK", "GO BACK", btn_goback)

    def _add_button(self, action, text, rect):
        self.buttons.append({
            "action": action,
            "text": text,
            "rect": rect,
            "centery": rect.centery,
            "scale": 0.83
        })

    def _update_volume_from_mouse(self, mouse_x, slider_type):
        relative_x = mouse_x - self.slider_x

        percentage = max(0, min(100, int((relative_x / self.slider_width) * 100)))

        if slider_type == "music":
            self.music_volume = percentage
            pygame.mixer.music.set_volume(self.music_volume / 100.0)
        elif slider_type == "bomb":
            self.bomb_volume = percentage
            if Bomb.explosion_sound:
                Bomb.explosion_sound.set_volume(self.bomb_volume / 100.0)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["action"] == "RESET":
                        self.music_volume = 50
                        self.bomb_volume = 50
                        self._apply_volumes()
                    elif button["action"] == "GO BACK":
                        return "GO BACK"

            music_hitbox = pygame.Rect(self.slider_x, self.music_y - 20, self.slider_width, 40)
            if music_hitbox.collidepoint(mouse_pos):
                self.dragging_music = True
                self._update_volume_from_mouse(mouse_pos[0], "music")

            bomb_hitbox = pygame.Rect(self.slider_x, self.bomb_y - 20, self.slider_width, 40)
            if bomb_hitbox.collidepoint(mouse_pos):
                self.dragging_bomb = True
                self._update_volume_from_mouse(mouse_pos[0], "bomb")

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_music = False

            if self.dragging_bomb:
                self.dragging_bomb = False
                if Bomb.explosion_sound:
                    Bomb.explosion_sound.play()

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_music:
                self._update_volume_from_mouse(mouse_pos[0], "music")
            if self.dragging_bomb:
                self._update_volume_from_mouse(mouse_pos[0], "bomb")

        return None

    def _draw_slider(self, screen, y_pos, volume, is_dragging, mouse_pos):

        hitbox = pygame.Rect(self.slider_x, y_pos - 20, self.slider_width, 40)
        is_hovered = hitbox.collidepoint(mouse_pos)

        bg_rect = pygame.Rect(self.slider_x, y_pos - self.slider_height // 2, self.slider_width, self.slider_height)
        pygame.draw.rect(screen, (80, 80, 80), bg_rect, border_radius=5)

        fill_width = int((volume / 100.0) * self.slider_width)
        fill_rect = pygame.Rect(self.slider_x, y_pos - self.slider_height // 2, fill_width, self.slider_height)
        pygame.draw.rect(screen, (52, 107, 211), fill_rect, border_radius=15)


        handle_x = self.slider_x + fill_width
        color = "white"
        pygame.draw.circle(screen, color, (handle_x, y_pos), self.handle_radius)

    def draw(self, screen):
        self.parallax_bg.draw(screen)

        self.timer += 0.1
        mouse_pos = pygame.mouse.get_pos()

        left_x = 120

        music_label = self.font_labels.render("MUSIC VOLUME:", True, "white")
        bomb_label = self.font_labels.render("BOMB VOLUME:", True, "white")

        music_val = self.font_labels.render(f"{self.music_volume}%", True, "white")
        bomb_val = self.font_labels.render(f"{self.bomb_volume}%", True, "white")

        screen.blit(music_label, (left_x, HEIGHT * 0.3))
        screen.blit(bomb_label, (left_x, HEIGHT * 0.45))

        screen.blit(music_val, (self.slider_x + self.slider_width + 30, HEIGHT * 0.3))
        screen.blit(bomb_val, (self.slider_x + self.slider_width + 30, HEIGHT * 0.45))

        self._draw_slider(screen, self.music_y, self.music_volume, self.dragging_music, mouse_pos)
        self._draw_slider(screen, self.bomb_y, self.bomb_volume, self.dragging_bomb, mouse_pos)

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