import pygame
from Player_basics import *
from board import boards

pygame.init()
pygame.mixer.init() # music & sounds

# background music
try:
    pygame.mixer.music.load("sounds/stateside_zara_larsson_sound.mp3")
    pygame.mixer.music.play(-1)
except pygame.error:
    print("Nie znaleziono pliku muzycznego, gra uruchomi się bez dźwięku.")

# basic stuff
WIDTH, HEIGHT = 935, 714
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont("comicsans", 30)
level = boards
direction = 0
move_allowed = [False, False, False, False] # Left, Right, Up, Down

# player related
# loading the player
sprite_sheet = pygame.image.load("assets/player_images/loki_idle.png").convert_alpha()
FRAME_W = 24
FRAME_H = 24
player_speed = 2
player_size = min(WIDTH / len(level[0]), HEIGHT / len(level))
# initial player position for now
player_x = (WIDTH - (len(level[0]) * player_size)) / 2 + player_size
player_y = (HEIGHT - (len(level) * player_size)) / 2 + player_size

def get_frame(sheet, x, y, width, height):
    frame = pygame.Surface((width, height), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x, y, width, height))
    return frame

idle_frames = []
for i in range(3):
    frame = get_frame(sprite_sheet, i, 0, FRAME_W, FRAME_H)
    frame = pygame.transform.scale(frame, (player_size, player_size))
    idle_frames.append(frame)

walk_sprite_sheet = pygame.image.load("assets/player_images/loki_move.png").convert_alpha()

walk_frames = []
for i in range(6): # Loop 5 times for the 5 frames
    frame = get_frame(walk_sprite_sheet, i * FRAME_W, 0, FRAME_W, FRAME_H)
    frame = pygame.transform.scale(frame, (player_size, player_size))
    walk_frames.append(frame)

# --- Add this where you load your other animations ---
hatch_sprite_sheet = pygame.image.load("assets/player_images/loki_hatch.png").convert_alpha()

hatch_frames = []
for i in range(3): # Loop 3 times for the 3 frames
    frame = get_frame(hatch_sprite_sheet, i * FRAME_W, 0, FRAME_W, FRAME_H)
    frame = pygame.transform.scale(frame, (player_size, player_size))
    hatch_frames.append(frame)

# Variables to control the intro sequence
is_hatching = True       # The game starts in the hatching state
hatch_frame_index = 0    # Tracks the hatching animation progress
hatch_speed = 0.05       # Slower speed so we can see the egg hatch!

# Animation variables
current_frame = 0       # Keeps track of which frame we are on
animation_speed = 0.1   # How fast the animation plays (adjust to your liking)

# --- 1. Load the shaking frames ---
shake_sprite_sheet = pygame.image.load("assets/player_images/loki_egg_move.png").convert_alpha()

shake_frames = []
for i in range(4): # Adjust this if your shake sprite has more/fewer frames
    frame = get_frame(shake_sprite_sheet, i * FRAME_W, 0, FRAME_W, FRAME_H)
    frame = pygame.transform.scale(frame, (player_size, player_size))
    shake_frames.append(frame)

# --- 2. Setup our State Machine variables ---
game_state = "shaking"   # The game now starts in the "shaking" state

# Variables for the shaking phase
shake_frame_index = 0
shake_anim_speed = 0.2
shake_timer = 0
shake_duration = 120


hatch_frame_index = 0
hatch_speed = 0.05


def draw_board():
    # Find the smallest size that fits both width and height
    tile_size = min(WIDTH / len(level[0]), HEIGHT / len(level))
    # (Total Width - Width of all tiles) / 2
    offset_x = (WIDTH - (len(level[0]) * tile_size)) / 2
    offset_y = (HEIGHT - (len(level) * tile_size)) / 2
    #line size
    line_size = 1
    #color of the board
    color = 'blue'

    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.rect(screen,color,
              (int(j * tile_size + offset_x), # Horizontal pos
                    int(i * tile_size + offset_y), # Vertical pos
                    int(tile_size),     # Width
                    int(tile_size)      # Height
                    ),line_size)
            elif level[i][j] == 3:
                pygame.draw.line(
                    screen,
                    color,
                    (int(j * tile_size + offset_x), int(i * tile_size + offset_y)),  # top-right of tile
                    (int(j * tile_size + offset_x), int(i * tile_size + tile_size + offset_y)),  # bottom-right of tile
                    line_size
                )
            elif level[i][j] == 4:
                pygame.draw.line(
                    screen,
                    color,
                    (int(j * tile_size + offset_x), int(i * tile_size + offset_y)),
                    (int(j * tile_size + tile_size + offset_x), int(i * tile_size + offset_y)),
                    line_size
                )
            elif level[i][j] == 5:
                pygame.draw.line(
                    screen,
                    color,
                    (int(j * tile_size + tile_size + offset_x - line_size), int(i * tile_size + offset_y)),  # top-right of tile
                    (int(j * tile_size + tile_size + offset_x - line_size), int(i * tile_size + tile_size + offset_y)),  # bottom-right of tile
                    line_size
                )
            elif level[i][j] == 6:
                pygame.draw.line(
                    screen,
                    color,
                    (int(j * tile_size + offset_x), int(i * tile_size + tile_size + offset_y)),
                    (int(j * tile_size + tile_size + offset_x), int(i * tile_size + tile_size + offset_y)),
                    line_size
                )


def player_render(is_moving):
    global current_frame

    if is_moving:
        active_anim_list = walk_frames
    else:
        active_anim_list = idle_frames

    frame_index = int(current_frame) % len(active_anim_list)
    current_image = active_anim_list[frame_index]

    # 0-Left 1-Right 2-Up 3-Down
    if direction == 0:
        screen.blit(pygame.transform.flip(current_image, True, False), (player_x, player_y))
    elif direction == 1:
        screen.blit(current_image, (player_x, player_y))
    elif direction == 2:
        screen.blit(current_image, (player_x, player_y))
    elif direction == 3:
        screen.blit(current_image, (player_x, player_y))

def check_position(center):
    move_allowed = [False, False, False, False]  # 0: Left, 1: Right, 2: Up, 3: Down
    tile_size = min(WIDTH / len(level[0]), HEIGHT / len(level))
    fudge_factor = player_size / 2

    # offsets
    offset_x = (WIDTH - (len(level[0]) * tile_size)) / 2
    offset_y = (HEIGHT - (len(level) * tile_size)) / 2

    # Grid
    grid_x = center[0] - offset_x
    grid_y = center[1] - offset_y

    # Left
    row = int(grid_y // tile_size)
    col = int((grid_x - fudge_factor) // tile_size)
    if 0 <= row < len(level) and 0 <= col < len(level[0]) and level[row][col] != 1:
        move_allowed[0] = True

    # Right
    row = int(grid_y // tile_size)
    col = int((grid_x + fudge_factor) // tile_size)
    if 0 <= row < len(level) and 0 <= col < len(level[0]) and level[row][col] != 1:
        move_allowed[1] = True

    # Up
    row = int((grid_y - fudge_factor) // tile_size)
    col = int(grid_x // tile_size)
    if 0 <= row < len(level) and 0 <= col < len(level[0]) and level[row][col] != 1:
        move_allowed[2] = True

    # 3: Down
    row = int((grid_y + fudge_factor) // tile_size)
    col = int(grid_x // tile_size)
    if 0 <= row < len(level) and 0 <= col < len(level[0]) and level[row][col] != 1:
        move_allowed[3] = True


    margin = 5  # margines błędu przy trafianiu w alejkę

    if direction == 2 or direction == 3:
        if (tile_size / 2 - margin) <= grid_x % tile_size <= (tile_size / 2 + margin):
            row_down = int((grid_y + tile_size) // tile_size)
            col_center = int(grid_x // tile_size)
            if 0 <= row_down < len(level) and 0 <= col_center < len(level[0]) and level[row_down][col_center] != 1:
                move_allowed[3] = True

            row_up = int((grid_y - tile_size) // tile_size)
            if 0 <= row_up < len(level) and 0 <= col_center < len(level[0]) and level[row_up][col_center] != 1:
                move_allowed[2] = True

    if direction == 0 or direction == 1:
        # Sprawdzamy czy gracz jest w osi Y blisko środka alejki
        if (tile_size / 2 - margin) <= grid_y % tile_size <= (tile_size / 2 + margin):
            row_center = int(grid_y // tile_size)

            col_left = int((grid_x - tile_size) // tile_size)
            if 0 <= row_center < len(level) and 0 <= col_left < len(level[0]) and level[row_center][col_left] != 1:
                move_allowed[0] = True

            col_right = int((grid_x + tile_size) // tile_size)
            if 0 <= row_center < len(level) and 0 <= col_right < len(level[0]) and level[row_center][col_right] != 1:
                move_allowed[1] = True

    return move_allowed

def player_move(player_position_x, player_position_y):
    keys = pygame.key.get_pressed()
    tile_size = min(WIDTH / len(level[0]), HEIGHT / len(level))

    board_left = (WIDTH - (len(level[0]) * tile_size)) / 2 + tile_size
    board_right = board_left + ((len(level[0])-3) * tile_size)
    board_top = (HEIGHT - (len(level) * tile_size)) / 2 + tile_size
    board_bottom = board_top + (len(level) * tile_size) - tile_size * 2

    moving = False

    if keys[pygame.K_a] and move_allowed[0]:
        if player_position_x - player_speed >= board_left:
            player_position_x -= player_speed
            moving = True

    if keys[pygame.K_d] and move_allowed[1]:
        if player_position_x + player_speed <= board_right:
            player_position_x += player_speed
            moving = True

    if keys[pygame.K_w] and move_allowed[2]:
        if player_position_y - player_speed >= board_top:
            player_position_y -= player_speed
            moving = True

    if keys[pygame.K_s] and move_allowed[3]:
        if player_position_y + player_size + player_speed <= board_bottom:
            player_position_y += player_speed
            moving = True

    return player_position_x, player_position_y, moving


# game loop
running = True

while running:
    timer.tick(fps)
    screen.fill('black')

    draw_board()

    # --- THE STATE MACHINE ---

    if game_state == "shaking":
        shake_frame_index += shake_anim_speed
        shake_timer += 1  # Increase the timer by 1 every frame (tick)

        # Loop the shaking animation using modulo (%)
        frame_idx = int(shake_frame_index) % len(shake_frames)
        current_image = shake_frames[frame_idx]
        screen.blit(current_image, (player_x, player_y))

        # Check if the egg has shaken long enough
        if shake_timer >= shake_duration:
            game_state = "hatching"  # Move to the next state!

    elif game_state == "hatching":
        hatch_frame_index += hatch_speed

        # Play the hatch animation ONCE (no looping)
        if int(hatch_frame_index) < len(hatch_frames):
            current_image = hatch_frames[int(hatch_frame_index)]
            screen.blit(current_image, (player_x, player_y))
        else:
            game_state = "playing"  # Animation done, start the game!
            current_frame = 0  # Reset the player's animation tracker

    elif game_state == "playing":
        current_frame += animation_speed

        player_center = player_x + player_size / 2, player_y + player_size / 2
        move_allowed = check_position(player_center)

        player_x, player_y, is_moving = player_move(player_x, player_y)
        player_render(is_moving)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Only allow key presses if we are in the "playing" state
        if game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    direction = 0
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    direction = 1
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    direction = 2
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    direction = 3

    pygame.display.flip()

pygame.quit()