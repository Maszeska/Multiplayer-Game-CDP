import pygame
from settings import *


class Board:
    def __init__(self, map_index):
        self.grid = BOARDS[map_index]
        self.tile_size = min(WIDTH / len(self.grid[0]), HEIGHT / len(self.grid))
        self.offset_x = (WIDTH - (len(self.grid[0]) * self.tile_size)) / 2
        self.offset_y = (HEIGHT - (len(self.grid) * self.tile_size)) / 2

        # --- Wczytywanie wszystkich wariantów płytek dla danej mapy ---
        self.tile_images = []
        for path in TILE_PATHS[map_index]:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (int(self.tile_size), int(self.tile_size)))
            self.tile_images.append(img)

        # Creating surface z obsługą przezroczystości (SRCALPHA)
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self._pre_render_board()

    def _pre_render_board(self):
        # 1. Obliczamy całkowitą szerokość i wysokość planszy
        board_width = int(len(self.grid[0]) * self.tile_size)
        board_height = int(len(self.grid) * self.tile_size)

        # 2. Zmniejszamy prostokąt tła o 4 piksele (czyli po 2 piksele z każdego boku)
        shrink_amount = 4
        bg_width = board_width - shrink_amount
        bg_height = board_height - shrink_amount

        # 3. Tworzymy główny prostokąt (półprzezroczysty czarny)
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 191))  # Czarny kolor z 75% przezroczystością

        # 4. Rysujemy prostokąt tła, przesuwając go lekko do środka (o 2 piksele)
        draw_x = self.offset_x + (shrink_amount // 2)
        draw_y = self.offset_y + (shrink_amount // 2)
        self.surface.blit(bg_surface, (draw_x, draw_y))

        # 5. Rysujemy na wierzchu ściany (klocki o wartości 1) ze zróżnicowaniem płytek
        num_tiles = len(self.tile_images)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    tile_x = int(j * self.tile_size + self.offset_x)
                    tile_y = int(i * self.tile_size + self.offset_y)

                    # Deterministyczny wybór płytki na podstawie pozycji!
                    tile_index = (i * 37 + j * 11) % num_tiles
                    chosen_tile = self.tile_images[tile_index]

                    self.surface.blit(chosen_tile, (tile_x, tile_y))

        # --- DODANA LINIA: Rysowanie czarnego obrysu wokół całej planszy ---
        # Tworzymy prostokąt definiujący granice planszy
        border_rect = pygame.Rect(self.offset_x, self.offset_y, board_width, board_height)
        # Rysujemy obrys (kolor czarny, grubość 2 piksele)
        pygame.draw.rect(self.surface, (255, 255, 255), border_rect, 5)

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def check_position(self, player_rect):
        start_col = int((player_rect.x - self.offset_x) // self.tile_size)
        start_row = int((player_rect.y - self.offset_y) // self.tile_size)

        for row in range(start_row - 1, start_row + 2):
            for col in range(start_col - 1, start_col + 2):
                if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                    if self.grid[row][col] == 1:
                        tile_rect = pygame.Rect(
                            col * self.tile_size + self.offset_x,
                            row * self.tile_size + self.offset_y,
                            self.tile_size,
                            self.tile_size
                        )
                        if player_rect.colliderect(tile_rect):
                            return False
        return True