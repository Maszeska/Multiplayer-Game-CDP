from settings import *


class Board:
    def __init__(self, level_data):
        self.level = level_data
        self.tile_size = min(WIDTH / len(self.level[0]), HEIGHT / len(self.level))
        self.offset_x = (WIDTH - (len(self.level[0]) * self.tile_size)) / 2
        self.offset_y = (HEIGHT - (len(self.level) * self.tile_size)) / 2

        # Creating surface
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.fill(BG_COLOR)  # Background color
        self._pre_render_board()

    def _pre_render_board(self):
        line_size = 1
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                tile_x = int(j * self.tile_size + self.offset_x)
                tile_y = int(i * self.tile_size + self.offset_y)
                t_size = int(self.tile_size)

                if self.level[i][j] == 1:
                    pygame.draw.rect(self.surface, BOARD_COLOR, (tile_x, tile_y, t_size, t_size), line_size)
                elif self.level[i][j] == 3:
                    pygame.draw.line(self.surface, BOARD_COLOR, (tile_x, tile_y), (tile_x, tile_y + t_size), line_size)
                elif self.level[i][j] == 4:
                    pygame.draw.line(self.surface, BOARD_COLOR, (tile_x, tile_y), (tile_x + t_size, tile_y), line_size)
                elif self.level[i][j] == 5:
                    pygame.draw.line(self.surface, BOARD_COLOR, (tile_x + t_size - line_size, tile_y),
                                     (tile_x + t_size - line_size, tile_y + t_size), line_size)
                elif self.level[i][j] == 6:
                    pygame.draw.line(self.surface, BOARD_COLOR, (tile_x, tile_y + t_size - line_size),
                                     (tile_x + t_size, tile_y + t_size - line_size), line_size)

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def check_position(self, center, player_size):
        new_move_allowed = [False, False, False, False]
        grid_x, grid_y = center[0] - self.offset_x, center[1] - self.offset_y

        # Hitbox
        fudge = player_size / 2

        for i, (dx, dy) in enumerate([(-fudge, 0), (fudge, 0), (0, -fudge), (0, fudge)]):
            row = int((grid_y + dy) // self.tile_size)
            col = int((grid_x + dx) // self.tile_size)
            if 0 <= row < len(self.level) - 1 and 0 <= col < len(self.level[0]) - 1 and row > 0 and col > 0 and \
                    self.level[row][col] != 1:
                new_move_allowed[i] = True
        return new_move_allowed