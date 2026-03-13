from settings import *
from game_object import GameObject

class Bomb(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)

        # Animations
        self.idle_frames = self.load_animation(BOMB_IDLE_PATH, 2, BOMB_FRAME_W, BOMB_FRAME_H)
        self.explosion_frames = self.load_animation(BOMB_EXPLOSION_PATH, 3, BOMB_FRAME_W, BOMB_FRAME_H)

        self.state = "ticking"
        self.timer = EXPLOSION_DURATION * FPS  # example: if 2 seconds (2 * 60 = 120 fps)

    def update(self):
        if self.state == "ticking":
            self.timer -= 1
            if self.timer <= 0:
                self.state = "exploding"
                self.current_frame = 0 # explosion starts from the 1st frame of animation

        elif self.state == "exploding":
            if int(self.current_frame) >= len(self.explosion_frames) - 1:
                self.state = "done"

    def draw(self, screen):
        if self.state == "done":
            return
        else:
            if self.state == "ticking":
                self.current_frame += ANIMATION_SPEED
                frames = self.idle_frames
                img = frames[int(self.current_frame) % len(frames)]
            else:
                self.current_frame += ANIMATION_SPEED
                frames = self.explosion_frames
                img = frames[int(self.current_frame) % len(frames)]
            screen.blit(img, (self.x, self.y))