from board import Board
from settings import *
from player import Player
from menu import MainMenu

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

main_menu = MainMenu()

game_state = "menu"


active_bombs = []

# game loop

running = True
while running:
    timer.tick(FPS)
    is_moving = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_RETURN:
                    game_state = "shaking"

            elif game_state == "playing":
                if event.key == pygame.K_SPACE and len(active_bombs) < 2:
                    new_bomb = player.drop_bomb(game_board)
                    active_bombs.append(new_bomb)

    if game_state == "menu":
        main_menu.draw(screen)


    else:
        game_board.draw(screen)

        for bomb in active_bombs:
            bomb.update()
            bomb.draw(screen)

        active_bombs = [bomb for bomb in active_bombs if bomb.state != "done"]

        if game_state == "shaking":
            if player.shake_timer >= SHAKE_DURATION:
                game_state = "hatching"
        elif game_state == "hatching":
            if int(player.hatch_frame_index) >= len(player.hatch_frames):
                game_state = "playing"
        elif game_state == "playing":
            is_moving = player.move(game_board)
        player.draw(screen, game_state, is_moving)

    pygame.display.flip()

pygame.quit()