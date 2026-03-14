from settings import *
from game_object import GameObject
from bomb import Bomb


class Player(GameObject):
    def __init__(self, x, y, size, player_id):
        super().__init__(x, y, size)
        self.id = player_id
        self.direction = 0  # 0: Left, 1: Right, 2: Up, 3: Down
        self.facing_left = False

        player_idle= f"assets/player_images/player_{self.id}/player_{self.id}_idle.png"
        player_move = f"assets/player_images/player_{self.id}/player_{self.id}_move.png"
        player_death = f"assets/player_images/player_{self.id}/player_{self.id}_dead.png"
        player_hatch = f"assets/player_images/player_{self.id}/player_{self.id}_hatch.png"
        egg_shake = f"assets/player_images/player_{self.id}/player_{self.id}_egg_move.png"

        # Animations
        self.idle_frames = self.load_animation(player_idle, 3, PLAYER_FRAME_W, PLAYER_FRAME_H)
        self.walk_frames = self.load_animation(player_move, 6, PLAYER_FRAME_W, PLAYER_FRAME_H)
        self.hatch_frames = self.load_animation(player_hatch, 3, PLAYER_FRAME_W, PLAYER_FRAME_H)
        self.shake_frames = self.load_animation(egg_shake, 4, PLAYER_FRAME_W, PLAYER_FRAME_H)
        self.death_frames = self.load_animation(player_death, 5, PLAYER_FRAME_W, PLAYER_FRAME_H)

        # Counters for frames
        self.shake_timer = 0
        self.hatch_frame_index = 0
        self.shake_frame_index = 0
        self.death_frame_index = 0

        self.lives = PLAYER_HP
        self.invulnerable_timer = 0

    def move(self, board):
        keys = pygame.key.get_pressed()
        is_moving = False


        if keys[pygame.K_a]:
            self.facing_left = True
            if board.check_position(self.get_hitbox(self.x - PLAYER_SPEED, self.y)):
                self.x -= PLAYER_SPEED
                is_moving = True

        if keys[pygame.K_d]:
            self.facing_left = False
            if board.check_position(self.get_hitbox(self.x + PLAYER_SPEED, self.y)):
                self.x += PLAYER_SPEED
                is_moving = True

        if keys[pygame.K_w]:
            if board.check_position(self.get_hitbox(self.x, self.y - PLAYER_SPEED)):
                self.y -= PLAYER_SPEED
                is_moving = True

        if keys[pygame.K_s]:
            if board.check_position(self.get_hitbox(self.x, self.y + PLAYER_SPEED)):
                self.y += PLAYER_SPEED
                is_moving = True

        return is_moving

    def get_grid_pos(self, board):
        center_x = self.x + (self.size / 2)
        center_y = self.y + (self.size / 2)

        col = int((center_x - board.offset_x) // board.tile_size)
        row = int((center_y - board.offset_y) // board.tile_size)

        return row, col

    def take_damage(self):
        if self.invulnerable_timer <= 0:
            self.lives -= 1
            print(f"Ouch! Zostało żyć: {self.lives}")
            self.invulnerable_timer = FPS * 2

    def update_timers(self):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def draw(self, screen, game_state, is_moving):
        if game_state == "game_over":
            return
        if self.invulnerable_timer > 0 and self.invulnerable_timer % 10 < 5 and game_state == "playing":
            return
        # Choosing animation based on game state
        if game_state == "shaking":
            self.shake_frame_index += SHAKE_ANIM_SPEED
            self.shake_timer += 1
            img = self.shake_frames[int(self.shake_frame_index) % len(self.shake_frames)]

        elif game_state == "hatching":
            self.hatch_frame_index += HATCH_SPEED
            idx = min(int(self.hatch_frame_index), len(self.hatch_frames) - 1)
            img = self.hatch_frames[idx]

        elif game_state == "dying" or game_state == "game_over":
            if game_state == "dying":
                self.death_frame_index += ANIMATION_SPEED  # lub inna prędkość, np. 0.1
            idx = min(int(self.death_frame_index), len(self.death_frames) - 1)
            img = self.death_frames[idx]

        else:  # "playing"
            self.current_frame += ANIMATION_SPEED
            frames = self.walk_frames if is_moving else self.idle_frames
            img = frames[int(self.current_frame) % len(frames)]

        # Flipping sprite when turning left
        flip_x = self.facing_left
        screen.blit(pygame.transform.flip(img, flip_x, False), (self.x, self.y))

    def get_hitbox(self, x, y):

        player_rect_left = x + HITBOX_BUFFER_SIDE
        player_rect_width = self.size - (2 * HITBOX_BUFFER_SIDE)
        player_rect_top = y + HITBOX_BUFFER_TOP
        player_rect_height = self.size - HITBOX_BUFFER_TOP - HITBOX_BUFFER_BOTTOM

        return pygame.Rect(player_rect_left, player_rect_top, player_rect_width, player_rect_height)

    def drop_bomb(self, board):
        center_x = self.x + (self.size / 2)
        center_y = self.y + (self.size / 2)

        # how does it work: we get the x/y position of player
        # after subtracting from it the offset and dividing by
        # the tile size, we get the concrete column/row
        col = int((center_x - board.offset_x) // board.tile_size)
        row = int((center_y - board.offset_y) // board.tile_size)

        bomb_x = (col * board.tile_size) + board.offset_x
        bomb_y = (row * board.tile_size) + board.offset_y

        return Bomb(bomb_x, bomb_y, board.tile_size)