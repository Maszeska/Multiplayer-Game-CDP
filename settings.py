import pygame

# ==========================================
# 1. server configuration
# ==========================================
SERVER_IP = "100.124.158.27"  # Twoje IP lokalne
SERVER_PORT = 5555

# ==========================================
# 2. screen settings
# ==========================================
WIDTH, HEIGHT = 1200, 714
FPS = 60

# ==========================================
# 3. colors and fonts
# ==========================================
BG_COLOR = 'black'
BOARD_COLOR = 'blue'
BORDER_COLOR = 'white'
FONT_SIZE = 30

# ==========================================
# 4. gameplay settings
# ==========================================
# --- (Player) ---
PLAYER_SPEED = 3
PLAYER_FRAME_W = 24
PLAYER_FRAME_H = 24
HITBOX_BUFFER_SIDE = 7.5
HITBOX_BUFFER_TOP = 7.5
HITBOX_BUFFER_BOTTOM = 3.75
PLAYER_HP = 3
PLAYER_JUMP_FRAMES = 4

# --- (Bomb) ---
BOMB_FRAME_W = 64
BOMB_FRAME_H = 64
EXPLOSION_DURATION = 1
BOMB_RANGE = 2

# --- (Blast effect) ---
# --- Dodane do settings.py ---
BLAST_EFFECT_PATH = "assets/bombs/explosion_effecy_1.png"
BLAST_FRAME_W = 32
BLAST_FRAME_H = 32
BLAST_FRAMES_NUM = 14

# ==========================================
# 5. Animation parameters
# ==========================================
ANIMATION_SPEED = 0.1
HATCH_SPEED = 0.05
SHAKE_ANIM_SPEED = 0.2
SHAKE_DURATION = 120  # Egg shaking animation in frames
PODIUM_ANIM_SPEED = 0.15

# ==========================================
# 6. Paths to assets
# ==========================================
# --- Sounds ---
MUSIC_PATH = "sounds/stateside_zara_larsson_sound.ogg"
BOOM_SOUND_PATH = "sounds/boom.wav"

# --- UI Graphics ---
ICON_PATH = "assets/bombs/bomb_icon.png"
BG_TITLE_PATH = "assets/background/bg_title.png"
OVERLAY = "assets/background/bg_menu_overlay.png"
INSTRUCTION = "assets/other/Buttons_Instructions.png"
MENU_FONT_PATH = "assets/fonts/CyberpunkCraftpixPixel.otf"

# --- Entities Graphics ---
BOMB_IDLE_PATH = "assets/bombs/bomb_character_o_idle.png"
BOMB_EXPLOSION_PATH = "assets/bombs/bomb_character_o_explode.png"
DINO_BG_PATH = "assets/player_images/player_0/player_0_move.png"

# --- Layer Config ---
LAYER_CONFIG = [
    {"path": "assets/background/bg_layer_1.png", "speed": 0.4},
    {"path": "assets/background/bg_layer_2.png", "speed": 0.0},
    {"path": "assets/background/bg_layer_3.png", "speed": 2.5}
]

LAYER_CONFIG_MAP_0 = [
    {"path": "assets/maps/map_0/bg-back.png", "speed": 0.6},
    {"path": "assets/maps/map_0/bg-stars.png", "speed": 0.4},
    {"path": "assets/maps/map_0/bg-planet.png", "speed": 0.0}
]

LAYER_CONFIG_MAP_1 = [
    {"path": "assets/maps/map_1/background.png", "speed": 0.1},
    {"path": "assets/maps/map_1/back-walls.png", "speed": 0.2}
]

LAYER_CONFIG_MAP_2 = [
    {"path": "assets/maps/map_2/back.png", "speed": 0.1},
    {"path": "assets/maps/map_2/middle.png", "speed": 0.2},
    {"path": "assets/maps/map_2/near.png", "speed": 0.3}
]


MAP_BACKGROUNDS = [LAYER_CONFIG_MAP_0, LAYER_CONFIG_MAP_1, LAYER_CONFIG_MAP_2]

TILE_PATHS = [["assets/maps/map_0/asteroid-1.png", "assets/maps/map_0/asteroid-2.png",  "assets/maps/map_0/asteroid-3.png",  "assets/maps/map_0/asteroid-4.png"],
              ["assets/maps/map_1/rock.png", "assets/maps/map_1/stone.png", "assets/maps/map_1/stone-head.png", "assets/maps/map_1/plant-small.png"],
              ["assets/maps/map_2/plant-1.png", "assets/maps/map_2/plant-2.png", "assets/maps/map_2/crystal-1.png",
               "assets/maps/map_2/crystal-2.png",  "assets/maps/map_2/plant-2.png", "assets/maps/map_2/bush.png",
               "assets/maps/map_2/trunk.png", "assets/maps/map_2/tree-pink.png", "assets/maps/map_2/tree-orange.png"],
              "assets/maps/map_2/rock.png",  "assets/maps/map_2/sign.png"]

# ==========================================
# 7. Boards
# ==========================================
BOARD_1 = [
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

BOARD_2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
BOARD_3 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

]
BOARDS = [BOARD_1, BOARD_2, BOARD_3]