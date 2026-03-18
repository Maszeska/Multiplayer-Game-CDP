from settings import *


class Board:
    def __init__(self, grid_data):
        self.grid = grid_data
        self.tile_size = min(WIDTH / len(self.grid[0]), HEIGHT / len(self.grid))
        self.offset_x = (WIDTH - (len(self.grid[0]) * self.tile_size)) / 2
        self.offset_y = (HEIGHT - (len(self.grid) * self.tile_size)) / 2

        # Creating surface
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.fill(BG_COLOR)  # Background color
        self._pre_render_board()

    def _pre_render_board(self):
        line_size = 1
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                tile_x = int(j * self.tile_size + self.offset_x)
                tile_y = int(i * self.tile_size + self.offset_y)
                t_size = int(self.tile_size)

                if self.grid[i][j] == 1: # Blocks
                    pygame.draw.rect(self.surface, BOARD_COLOR, (tile_x, tile_y, t_size, t_size)) # Inside
                    pygame.draw.rect(self.surface, BORDER_COLOR, (tile_x, tile_y, t_size, t_size), line_size)  # Border


    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def check_position(self, player_rect):
        # Player position block
        start_col = int((player_rect.x - self.offset_x) // self.tile_size)
        start_row = int((player_rect.y - self.offset_y) // self.tile_size)

        # Check blocks near the player
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
                        # Collision with block
                        if player_rect.colliderect(tile_rect):
                            return False
        return True