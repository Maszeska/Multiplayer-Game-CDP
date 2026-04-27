from settings import *
from ui.base_menu import BaseMenu

#----------------------------------------------------
# Lobby - choosing map and synchronising players start time
#----------------------------------------------------

class Lobby(BaseMenu):
    def __init__(self, change_scene_callback, network):
        super().__init__()
        self.change_scene = change_scene_callback
        self.network = network

        self.font_info = pygame.font.Font(MENU_FONT_PATH, 30)
        self.font_prev = pygame.font.Font(MENU_FONT_PATH, 40)

        # --- Player state ---
        self.is_ready = False
        self.map_vote = None  # default -> no vote

        self.create_vertical_buttons(
            button_texts=["VOTE MAP 1", "VOTE MAP 2", "VOTE MAP 3", "GO BACK"],
            start_y=HEIGHT * 0.3
        )

        self.map_previews = []
        target_preview_height = int(HEIGHT * 0.45)

        for i in range(1, 4):
            try:
                path = f"assets/other/map_{i}.png"
                img = pygame.image.load(path).convert_alpha()

                aspect_ratio = img.get_width() / img.get_height()
                target_width = int(target_preview_height * aspect_ratio)
                scaled_img = pygame.transform.smoothscale(img, (target_width, target_preview_height))

                self.map_previews.append(scaled_img)
            except pygame.error:
                print(f"Błąd: Nie znaleziono pliku podglądu mapy: {path}")
                self.map_previews.append(pygame.Surface((100, 100)))

        self.preview_rect = self.map_previews[0].get_rect(topright=(WIDTH - 50, HEIGHT * 0.25))

        # --- Load players icons ---
        self.player_icons = []
        for i in range(4):
            try:
                path = f"assets/player_images/player_{i}/player_{i}_idle.png"
                img = pygame.image.load(path).convert_alpha()
                icon = img.subsurface((0, 0, PLAYER_FRAME_W, PLAYER_FRAME_H))
                icon = pygame.transform.scale(icon, (40, 40))
                self.player_icons.append(icon)
            except:
                surf = pygame.Surface((40, 40))
                surf.fill((100, 100, 100))
                self.player_icons.append(surf)

    def reset_map_selection(self):
        # --- Reset the map selection state for a new round. ---
        self.is_ready = False
        self.map_vote = None

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        action = self.handle_button_event(event, mouse_pos)

        if action == "VOTE MAP 1":
            self.map_vote = 0
            self.is_ready = True
        elif action == "VOTE MAP 2":
            self.map_vote = 1
            self.is_ready = True
        elif action == "VOTE MAP 3":
            self.map_vote = 2
            self.is_ready = True
        elif action == "GO BACK":
            # if player leaves lobby -> not ready
            self.is_ready = False
            self.map_vote = None

            disconnect_data = {
                'in_lobby': False,
                'is_ready': False,
                'map_vote': None
            }

            self.network.send(disconnect_data)
            self.change_scene("menu")

        return None

    def update(self):
        my_lobby_data = {
            'in_lobby': True,
            'is_ready': self.is_ready,
            'map_vote': self.map_vote
        }
        self.network.send(my_lobby_data)

        all_data = self.network.all_players_data
        connected_count = self.network.connected_players_count

        ready_count = 0
        votes = {0: 0, 1: 0, 2: 0}

        if all_data:
            for data in all_data:
                if data and data.get('in_lobby'):
                    if data.get('is_ready'):
                        ready_count += 1
                        vote = data.get('map_vote')
                        if vote is not None and vote in votes:
                            votes[vote] += 1

        if ready_count == connected_count and connected_count > 0:
            # Find the maximum vote count
            max_votes = max(votes.values())
            # Count how many maps have this max vote count
            maps_with_max_votes = [map_id for map_id, vote_count in votes.items() if vote_count == max_votes]

            # ---------------------------------------------------------------
            # Only start if ONE map has the most votes (dominance, no ties)
            # ---------------------------------------------------------------

            if len(maps_with_max_votes) == 1:
                winning_map_index = maps_with_max_votes[0]
                print(f"Startujemy! Wygrała mapa: {winning_map_index}")
                self.change_scene("game", winning_map_index)
            else:
                print(f"Tie detected: Maps {maps_with_max_votes} have equal votes. Waiting for dominance...")

    def draw(self, screen):
        self.parallax_bg.draw(screen)
        mouse_pos = pygame.mouse.get_pos()

        self.draw_buttons(screen, mouse_pos)
        all_data = self.network.all_players_data
        if all_data:
            offset_counters = {0: 0, 1: 0, 2: 0}

            for i, data in enumerate(all_data):
                if data and data.get('in_lobby') and data.get('map_vote') is not None:
                    vote_idx = data.get('map_vote')

                    if vote_idx in [0, 1, 2]:
                        target_button_rect = self.buttons[vote_idx]["rect"]
                        icon_x = target_button_rect.right + 15 + (offset_counters[vote_idx] * 45)
                        icon_y = target_button_rect.centery - 20

                        screen.blit(self.player_icons[i], (icon_x, icon_y))
                        label = self.font_info.render(f"P{i + 1}", True, "white")
                        screen.blit(label, (icon_x + 5, icon_y + 35))

                        offset_counters[vote_idx] += 1

        status_color = "green" if self.is_ready else "white"

        ready_players = sum([1 for d in self.network.all_players_data if d and d.get('is_ready')])
        info_surf = self.font_info.render(f"PLAYERS READY: {ready_players}/{self.network.connected_players_count}",
                                          True, "white")
        screen.blit(info_surf, (30, 30))

        if self.is_ready:
            status_text = "STATUS: READY!"
        else:
            status_text = "STATUS: CHOOSE MAP"

        status_surf = self.font_info.render(status_text, True, status_color)
        screen.blit(status_surf, (30, 70))

        hovered_map_index = None

        for i, button in enumerate(self.buttons):
            if button["rect"].collidepoint(mouse_pos):
                action = button["action"]
                if "VOTE MAP" in action:
                    if "1" in action:
                        hovered_map_index = 0
                    elif "2" in action:
                        hovered_map_index = 1
                    elif "3" in action:
                        hovered_map_index = 2

        display_index = hovered_map_index
        if display_index is None and self.is_ready:
            display_index = self.map_vote

        if display_index is not None and display_index < len(self.map_previews):
            preview_img = self.map_previews[display_index]
            screen.blit(preview_img, self.preview_rect)

            if display_index == self.map_vote and hovered_map_index is None:
                prev_text = self.font_prev.render(f"YOUR VOTE: MAP {display_index + 1}", True, "green")
                pygame.draw.rect(screen, "green", self.preview_rect.inflate(10, 10), 3, border_radius=10)
            else:
                prev_text = self.font_prev.render(f"PREVIEW: MAP {display_index + 1}", True, "white")

            text_rect = prev_text.get_rect(centerx=self.preview_rect.centerx, bottom=self.preview_rect.top - 15)
            screen.blit(prev_text, text_rect)
