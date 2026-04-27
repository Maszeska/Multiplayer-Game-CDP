import pygame
from settings import *
from ui.base_menu import BaseMenu
# Importujemy GameObject tutaj, aby mieć dostęp do klasy
from entities.game_object import GameObject

#----------------------------------------------------
# End Screen - results of match shown with dinosaurs on podium
#----------------------------------------------------

class EndScreen(BaseMenu):
    def __init__(self, change_scene_callback, ranking):
        super().__init__()
        self.change_scene = change_scene_callback
        self.ranking = ranking  # Ranking of players

        self.font_title = pygame.font.Font(MENU_FONT_PATH, 60)
        self.font_info = pygame.font.Font(MENU_FONT_PATH, 30)

        btn_w, btn_h = self.font_max.size("BACK TO MENU")
        self.create_vertical_buttons(
            button_texts=["BACK TO MENU"],
            start_y=HEIGHT * 0.8,
            x_pos=(WIDTH // 2) - (btn_w // 2)
        )

        self.player_jump_animations = {}
        self.animation_indices = {1: 0.0, 2: 0.0, 3: 0.0}

        for i, pid in enumerate(self.ranking):
            if i >= 3: break
            rank_place = i + 1

            try:
                path = f"assets/player_images/player_{pid}/player_{pid}_jump.png"
                temp_loader = GameObject(0, 0, 120)

                scaled_frames = temp_loader.load_animation(
                    path,
                    PLAYER_JUMP_FRAMES,
                    PLAYER_FRAME_W,
                    PLAYER_FRAME_H
                )

                self.player_jump_animations[pid] = scaled_frames

                self.animation_indices[rank_place] = i * 2.0

            except Exception as e:
                print(f"Błąd ładowania animacji dla P{pid}: {e}")
                surf = pygame.Surface((120, 120))
                surf.fill((200, 0, 0))
                self.player_jump_animations[pid] = [surf]

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        action = self.handle_button_event(event, mouse_pos)

        if action == "BACK TO MENU":
            self.change_scene("menu")

    def update(self):
        for rank_place in self.animation_indices:
            self.animation_indices[rank_place] += PODIUM_ANIM_SPEED

    def draw(self, screen):
        self.parallax_bg.draw(screen)
        mouse_pos = pygame.mouse.get_pos()

        title_surf = self.font_title.render("MATCH RESULTS", True, (255, 255, 0))
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 80))

        center_x = WIDTH // 2
        base_y = HEIGHT * 0.7

        podium_data = [
            {"rank": 1, "x": center_x, "h": 200, "color": (255, 215, 0)},  # Złoto
            {"rank": 2, "x": center_x - 160, "h": 140, "color": (192, 192, 192)},  # Srebro
            {"rank": 3, "x": center_x + 160, "h": 90, "color": (205, 127, 50)}  # Brąz
        ]

        for i, p_info in enumerate(podium_data):
            if i < len(self.ranking):
                pid = self.ranking[i]
                rank_place = i + 1

                rect_x = p_info["x"] - 60
                rect_y = base_y - p_info["h"]
                pygame.draw.rect(screen, p_info["color"], (rect_x, rect_y, 120, p_info["h"]))
                pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, 120, p_info["h"]), 4)

                rank_text = self.font_title.render(str(p_info["rank"]), True, (255, 255, 255))
                screen.blit(rank_text, (p_info["x"] - rank_text.get_width() // 2, rect_y + 15))

                if pid in self.player_jump_animations:
                    frames = self.player_jump_animations[pid]
                    current_idx = int(self.animation_indices[rank_place]) % len(frames)
                    img = frames[current_idx]

                    img_x = p_info["x"] - img.get_width() // 2
                    img_y = rect_y - img.get_height() + 10

                    screen.blit(img, (img_x, img_y))

                    p_text = self.font_info.render(f"PLAYER {pid}", True, (255, 255, 255))
                    screen.blit(p_text, (p_info["x"] - p_text.get_width() // 2, img_y - 30))

        self.draw_buttons(screen, mouse_pos)