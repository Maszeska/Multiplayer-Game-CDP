from entities.game_object import GameObject
from settings import *

#----------------------------------------------------
# Just cosmetic for background in menu
#----------------------------------------------------

class BackgroundDino(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)

        self.frames = self.load_animation(DINO_BG_PATH, num_frames=6, frame_w=PLAYER_FRAME_W, frame_h=PLAYER_FRAME_H)

        self.animation_speed = 0.2

    def update_and_draw(self, screen):
        self.current_frame += self.animation_speed

        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        frame_to_draw = self.frames[int(self.current_frame)]
        screen.blit(frame_to_draw, (self.x, self.y))