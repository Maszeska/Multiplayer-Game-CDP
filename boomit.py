from board import boards
from settings import *
from player import Player

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boomit!")

try:
    game_icon = pygame.image.load(ICON_PATH).convert_alpha()
    pygame.display.set_icon(game_icon)
except pygame.error:
    print("Nie udało się załadować ikonki okna.")

timer = pygame.time.Clock()


# background music
try:
    pygame.mixer.music.load("sounds/stateside_zara_larsson_sound.mp3")
    pygame.mixer.music.play(-1)
except pygame.error:
    print("Nie znaleziono pliku muzycznego, gra uruchomi się bez dźwięku.")

# board logic
level = boards
tile_size = min(WIDTH / len(level[0]), HEIGHT / len(level))

start_x = (WIDTH - (len(level[0]) * tile_size)) / 2 + tile_size
start_y = (HEIGHT - (len(level) * tile_size)) / 2 + tile_size
player = Player(start_x, start_y, tile_size)

game_state = "shaking"

# Functions
# drawing board
def draw_board(tile):
    offset_x = (WIDTH - (len(level[0]) * tile)) / 2
    offset_y = (HEIGHT - (len(level) * tile)) / 2

    line_size = 1

    for i in range(len(level)):
        for j in range(len(level[i])):
            tile_x = int(j * tile + offset_x)
            tile_y = int(i * tile + offset_y)
            t_size = int(tile)

            # Case 1: Full Square
            if level[i][j] == 1:
                pygame.draw.rect(screen, BOARD_COLOR, (tile_x, tile_y, t_size, t_size), line_size)

            # Case 3: Vertical line on the LEFT side of the tile
            elif level[i][j] == 3:
                pygame.draw.line(screen, BOARD_COLOR,
                                 (tile_x, tile_y),
                                 (tile_x, tile_y + t_size), line_size)

            # Case 4: Horizontal line on the TOP side of the tile
            elif level[i][j] == 4:
                pygame.draw.line(screen, BOARD_COLOR,
                                 (tile_x, tile_y),
                                 (tile_x + t_size, tile_y), line_size)

            # Case 5: Vertical line on the RIGHT side of the tile
            elif level[i][j] == 5:
                pygame.draw.line(screen, BOARD_COLOR,
                                 (tile_x + t_size - line_size, tile_y),
                                 (tile_x + t_size - line_size, tile_y + t_size), line_size)

            # Case 6: Horizontal line on the BOTTOM side of the tile
            elif level[i][j] == 6:
                pygame.draw.line(screen, BOARD_COLOR,
                                 (tile_x, tile_y + t_size - line_size),
                                 (tile_x + t_size, tile_y + t_size - line_size), line_size)

# collision mechanic
def check_position(center):
    new_move_allowed = [False, False, False, False]
    offset_x = (WIDTH - (len(level[0]) * tile_size)) / 2
    offset_y = (HEIGHT - (len(level) * tile_size)) / 2
    grid_x, grid_y = center[0] - offset_x, center[1] - offset_y

    fudge = 20 # idk TODO naprawić to jak sie w ściany wbija

    for i, (dx, dy) in enumerate([(-fudge, 0), (fudge, 0), (0, -fudge), (0, fudge)]):
        row = int((grid_y + dy) // tile_size)
        col = int((grid_x + dx) // tile_size)
        if 0 <= row < len(level) - 1 and 0 <= col < len(level[0]) - 1 and row > 0 and col > 0 and level[row][col] != 1:
            new_move_allowed[i] = True
    return new_move_allowed

# game loop
running = True
while running:
    timer.tick(FPS)
    screen.fill(BG_COLOR)
    draw_board(tile_size)
    is_moving = False

    if game_state == "shaking":
        if player.shake_timer >= SHAKE_DURATION:
            game_state = "hatching"

    elif game_state == "hatching":
        if int(player.hatch_frame_index) >= len(player.hatch_frames):
            game_state = "playing"

    elif game_state == "playing":
        # Checking for collisions
        player_center = (player.x + player.size / 2, player.y + player.size / 2)
        move_allowed = check_position(player_center)
        # Moving player
        is_moving = player.move(move_allowed)

    # Class decides on animation style
    player.draw(screen, game_state, is_moving)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
