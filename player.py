from settings import *


class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.direction = 0  # 0: Left, 1: Right, 2: Up, 3: Down
        self.facing_left = False

        # Animations
        self.idle_frames = self.load_animation(PLAYER_IDLE_PATH, 3)
        self.walk_frames = self.load_animation(PLAYER_MOVE_PATH, 6)
        self.hatch_frames = self.load_animation(PLAYER_HATCH_PATH, 3)
        self.shake_frames = self.load_animation(EGG_SHAKE_PATH, 4)

        # Counters fir frames
        self.current_frame = 0
        self.shake_timer = 0
        self.hatch_frame_index = 0
        self.shake_frame_index = 0

    def load_animation(self, path, num_frames):
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(num_frames):
            frame = pygame.Surface((FRAME_W, FRAME_H), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * FRAME_W, 0, FRAME_W, FRAME_H))
            frame = pygame.transform.scale(frame, (int(self.size), int(self.size)))
            frames.append(frame)
        return frames

    def move(self, move_allowed):
        keys = pygame.key.get_pressed()
        is_moving = False

        if keys[pygame.K_a]:
            self.direction = 0
            self.facing_left = True
            if move_allowed[0]:
                self.x -= PLAYER_SPEED
                is_moving = True

        if keys[pygame.K_d]:
            self.direction = 1
            self.facing_left = False
            if move_allowed[1]:
                self.x += PLAYER_SPEED
                is_moving = True

        if keys[pygame.K_w]:
            self.direction = 2
            if move_allowed[2]:
                self.y -= PLAYER_SPEED
                is_moving = True

        if keys[pygame.K_s]:
            self.direction = 3
            if move_allowed[3]:
                self.y += PLAYER_SPEED
                is_moving = True

        return is_moving

    def draw(self, screen, game_state, is_moving):
        # Choosing animation based on game state
        if game_state == "shaking":
            self.shake_frame_index += SHAKE_ANIM_SPEED
            self.shake_timer += 1
            img = self.shake_frames[int(self.shake_frame_index) % len(self.shake_frames)]

        elif game_state == "hatching":
            self.hatch_frame_index += HATCH_SPEED
            idx = min(int(self.hatch_frame_index), len(self.hatch_frames) - 1)
            img = self.hatch_frames[idx]

        else:  # "playing"
            self.current_frame += ANIMATION_SPEED
            frames = self.walk_frames if is_moving else self.idle_frames
            img = frames[int(self.current_frame) % len(frames)]

        # Flipping sprite when turning left
        flip_x = self.facing_left
        screen.blit(pygame.transform.flip(img, flip_x, False), (self.x, self.y))