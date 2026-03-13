from settings import *

class GameObject:
    def __init__(self, x, y, size):
        # basics
        self.x = x
        self.y = y
        self.size = size
        # animation general
        self.current_frame = 0

    # universal animation function for all objects
    def load_animation(self, path, num_frames, frame_w, frame_h):
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(num_frames):
            frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * frame_w, 0, frame_w, frame_h))
            frame = pygame.transform.scale(frame, (int(self.size), int(self.size)))
            frames.append(frame)
        return frames