import pygame

# --- Screen config ---
WIDTH, HEIGHT = 935, 714
FPS = 60

# --- Colors/ Fonts etc. ---
BG_COLOR = 'black'
BOARD_COLOR = 'blue'
BORDER_COLOR = 'white'
FONT_SIZE = 30

# --- Player ---
PLAYER_SPEED = 3
PLAYER_FRAME_W = 24
PLAYER_FRAME_H = 24
HITBOX_BUFFER_SIDE = 7.5
HITBOX_BUFFER_TOP = 7.5
HITBOX_BUFFER_BOTTOM = 3.75

# --- Bomb ---
BOMB_FRAME_W = 64
BOMB_FRAME_H = 64
EXPLOSION_DURATION = 1

# --- Boards ---
BOARD = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1],
    [1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1],
    [1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1],
    [1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1],
    [1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1],
    [1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# --- Paths to assets ---
# Music
MUSIC_PATH = "sounds/stateside_zara_larsson_sound.mp3"

# Graphics
PLAYER_IDLE_PATH = "assets/player_images/player_0/player_0_idle.png"
PLAYER_MOVE_PATH = "assets/player_images/player_0/player_0_move.png"
PLAYER_HATCH_PATH = "assets/player_images/player_0/player_0_hatch.png"
EGG_SHAKE_PATH = "assets/player_images/player_0/player_0_egg_move.png"
BOMB_IDLE_PATH = "assets/bombs/bomb_character_o_idle.png"
BOMB_EXPLOSION_PATH = "assets/bombs/bomb_character_o_explode.png"

# game
ICON_PATH = "assets/bombs/bomb_icon.png"
BG_IMAGE_MENU = "assets/background/boomit_main_menu.png"
MENU_FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"

# --- Animation parameters ---
ANIMATION_SPEED = 0.1
HATCH_SPEED = 0.05
SHAKE_ANIM_SPEED = 0.2
SHAKE_DURATION = 120 # Egg shaking animation in frames