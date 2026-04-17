from settings import *
from ui.base_menu import BaseMenu


class Lobby(BaseMenu):
    def __init__(self, change_scene_callback, network):
        super().__init__()
        self.change_scene = change_scene_callback
        self.network = network

        # --- Czcionki ---
        self.font_info = pygame.font.Font(MENU_FONT_PATH, 30)
        self.font_prev = pygame.font.Font(MENU_FONT_PATH, 40)

        # --- Stan lokalnego gracza ---
        self.is_ready = False
        self.map_vote = None  # Domyślnie brak głosu i brak gotowości

        # --- Tworzenie przycisków kolumny ---
        self.create_vertical_buttons(
            button_texts=["VOTE MAP 1", "VOTE MAP 2", "VOTE MAP 3", "GO BACK"],
            start_y=HEIGHT * 0.3
        )

        # --- ŁADOWANIE PODGLĄDÓW MAP ---
        self.map_previews = []
        target_preview_height = int(HEIGHT * 0.45)  # Podgląd zajmie 45% wysokości ekranu

        # Zakładamy, że masz 3 mapy w settings.MAPS i odpowiadające im PNG
        for i in range(1, 4):  # Pętla dla map_1, map_2, map_3
            try:
                # 1. Ładujemy obraz
                path = f"assets/other/map_{i}.png"
                img = pygame.image.load(path).convert_alpha()

                # 2. Skalujemy go z zachowaniem proporcji
                aspect_ratio = img.get_width() / img.get_height()
                target_width = int(target_preview_height * aspect_ratio)
                scaled_img = pygame.transform.smoothscale(img, (target_width, target_preview_height))

                self.map_previews.append(scaled_img)
            except pygame.error:
                print(f"Błąd: Nie znaleziono pliku podglądu mapy: {path}")
                self.map_previews.append(pygame.Surface((100, 100)))

        self.preview_rect = self.map_previews[0].get_rect(topright=(WIDTH - 50, HEIGHT * 0.25))

    def reset_map_selection(self):
        """Reset the map selection state for a new round."""
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
            # Jeśli gracz wychodzi, cofamy jego gotowość
            self.is_ready = False
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
            winning_map_index = max(votes, key=votes.get)
            print(f"Startujemy! Wygrała mapa: {winning_map_index}")
            self.change_scene("game", winning_map_index)

    def draw(self, screen):
        self.parallax_bg.draw(screen)
        mouse_pos = pygame.mouse.get_pos()

        # Rysowanie przycisków z BaseMenu
        self.draw_buttons(screen, mouse_pos)

        # --- INFORMACJE W LEWYM GÓRNYM ROGU (BIAŁE) ---
        # 1. Licznik gotowych graczy
        ready_players = sum([1 for d in self.network.all_players_data if d and d.get('is_ready')])
        info_surf = self.font_info.render(f"PLAYERS READY: {ready_players}/{self.network.connected_players_count}",
                                          True, "white")
        screen.blit(info_surf, (30, 30))

        # 2. Status gotowości lokalnego gracza
        if self.is_ready:
            status_text = "STATUS: READY!"
        else:
            status_text = "STATUS: CHOOSE MAP"

        status_surf = self.font_info.render(status_text, True, "white")
        screen.blit(status_surf, (30, 70))

        # --- LOGIKA PODGLĄDU MAPY (HOVER ORAZ ZAPISANY GŁOS) ---
        hovered_map_index = None

        # Iterujemy po przyciskach w BaseMenu, żeby znaleźć ten, na który najeżdżamy
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

        # Wyświetlamy mapę, na którą najeżdżamy. Jeśli na nic nie najeżdżamy, pokazujemy wybraną mapę.
        display_index = hovered_map_index
        if display_index is None and self.is_ready:
            display_index = self.map_vote

        # --- RYSOWANIE PODGLĄDU ---
        # 1. Rysujemy ramkę dla podglądu
        pygame.draw.rect(screen, (50, 50, 50), self.preview_rect.inflate(10, 10), border_radius=10)  # Ramka
        pygame.draw.rect(screen, "black", self.preview_rect.inflate(10, 10), 2, border_radius=10)  # Obwódka ramki

        if display_index is not None and display_index < len(self.map_previews):
            # 2. Rysujemy podgląd mapy (najeżdżanej lub wybranej)
            preview_img = self.map_previews[display_index]
            screen.blit(preview_img, self.preview_rect)

            # Zmieniamy tekst w zależności od tego, czy to tylko podgląd, czy ostateczny głos
            if display_index == self.map_vote and hovered_map_index is None:
                prev_text = self.font_prev.render(f"YOUR VOTE: MAP {display_index + 1}", True, "green")
            else:
                prev_text = self.font_prev.render(f"PREVIEW: MAP {display_index + 1}", True, "white")

            text_rect = prev_text.get_rect(centerx=self.preview_rect.centerx, bottom=self.preview_rect.top - 15)
            screen.blit(prev_text, text_rect)
        else:
            # 3. Jeśli nie najeżdżamy i jeszcze NIE ZAGŁOSOWALIŚMY, rysujemy szary pytajnik
            pygame.draw.rect(screen, (80, 80, 80), self.preview_rect, border_radius=5)
            q_surf = self.font_prev.render("?", True, (150, 150, 150))
            q_rect = q_surf.get_rect(center=self.preview_rect.center)
            screen.blit(q_surf, q_rect)