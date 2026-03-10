import pygame

# --- Screen config ---
WIDTH, HEIGHT = 935, 714
FPS = 60

# --- Colors/ Fonts etc. ---
BG_COLOR = 'black'
BOARD_COLOR = 'blue'
FONT_SIZE = 30

# --- Player ---
PLAYER_SPEED = 3
FRAME_W = 24
FRAME_H = 24

# --- Paths to assets ---
# Music
MUSIC_PATH = "sounds/stateside_zara_larsson_sound.mp3"

# Graphics
PLAYER_IDLE_PATH = "assets/player_images/loki_idle.png"
PLAYER_MOVE_PATH = "assets/player_images/loki_move.png"
PLAYER_HATCH_PATH = "assets/player_images/loki_hatch.png"
EGG_SHAKE_PATH = "assets/player_images/loki_egg_move.png"

# game
ICON_PATH = "assets/bombs/img.png"

# --- Animation parameters ---
ANIMATION_SPEED = 0.1
HATCH_SPEED = 0.05
SHAKE_ANIM_SPEED = 0.2
SHAKE_DURATION = 120 # Egg shaking animation in frames