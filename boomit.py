from board import Board
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
game_board = Board(BOARD)

start_x = game_board.offset_x + game_board.tile_size
start_y = game_board.offset_y + game_board.tile_size
player = Player(start_x, start_y, game_board.tile_size)

game_state = "shaking"

# Functions
running = True
while running:
    timer.tick(FPS)
    game_board.draw(screen)
    is_moving = False


    if game_state == "shaking":
        if player.shake_timer >= SHAKE_DURATION:
            game_state = "hatching"

    elif game_state == "hatching":
        if int(player.hatch_frame_index) >= len(player.hatch_frames):
            game_state = "playing"

    elif game_state == "playing":
        player_center = (player.x + player.size / 2, player.y + player.size / 2)
        move_allowed = game_board.check_position(player_center, player.size)
        is_moving = player.move(move_allowed)

    player.draw(screen, game_state, is_moving)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
