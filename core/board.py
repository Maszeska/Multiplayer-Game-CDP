import pygame
from settings import *

#----------------------------------------------------
# Game Board - Just a tile grid and the core space for the game
#----------------------------------------------------

class Board:
    def __init__(self, map_index):
        self.grid = BOARDS[map_index]
        self.tile_size = min(WIDTH / len(self.grid[0]), HEIGHT / len(self.grid))
        self.offset_x = (WIDTH - (len(self.grid[0]) * self.tile_size)) / 2
        self.offset_y = (HEIGHT - (len(self.grid) * self.tile_size)) / 2

        # --- Loading every tile variant for the board tiles ---
        self.tile_images = []
        for path in TILE_PATHS[map_index]:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (int(self.tile_size), int(self.tile_size)))
            self.tile_images.append(img)

        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self._pre_render_board()


    def _pre_render_board(self):
        board_width = int(len(self.grid[0]) * self.tile_size)
        board_height = int(len(self.grid) * self.tile_size)

        # For the cosmetic purpose the transparent background is sized down
        shrink_amount = 4
        bg_width = board_width - shrink_amount
        bg_height = board_height - shrink_amount

        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 191))  # black surface 75% transparency

        draw_x = self.offset_x + (shrink_amount // 2)
        draw_y = self.offset_y + (shrink_amount // 2)
        self.surface.blit(bg_surface, (draw_x, draw_y))

        # drawing tiles
        num_tiles = len(self.tile_images)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    tile_x = int(j * self.tile_size + self.offset_x)
                    tile_y = int(i * self.tile_size + self.offset_y)

                    # Simulating random-like tile placement ( same for every player )
                    tile_index = (i * 37 + j * 11) % num_tiles
                    chosen_tile = self.tile_images[tile_index]

                    self.surface.blit(chosen_tile, (tile_x, tile_y))

        # Black border around whole board
        border_rect = pygame.Rect(self.offset_x, self.offset_y, board_width, board_height)
        pygame.draw.rect(self.surface, (255, 255, 255), border_rect, 5)


    def draw(self, screen):
        screen.blit(self.surface, (0, 0))


    # Collision player <-> wall
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