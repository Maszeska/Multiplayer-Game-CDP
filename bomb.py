from settings import *
from game_object import GameObject
import pygame


class Bomb(GameObject):
    sound_loaded = False
    explosion_sound = None

    animations_loaded = False
    shared_idle_frames = []
    shared_explosion_frames = []

    def __init__(self, x, y, size):
        super().__init__(x, y, size)

        if not Bomb.animations_loaded:
            Bomb.shared_idle_frames = self.load_animation(BOMB_IDLE_PATH, 2, BOMB_FRAME_W, BOMB_FRAME_H)
            Bomb.shared_explosion_frames = self.load_animation(BOMB_EXPLOSION_PATH, 3, BOMB_FRAME_W, BOMB_FRAME_H)
            Bomb.animations_loaded = True

        self.idle_frames = Bomb.shared_idle_frames
        self.explosion_frames = Bomb.shared_explosion_frames
        self.explosion_surface = None

        self.state = "ticking"
        self.timer = EXPLOSION_DURATION * FPS

        self.blast_tiles = []

        if not Bomb.sound_loaded:
            try:
                Bomb.explosion_sound = pygame.mixer.Sound(BOOM_SOUND_PATH)
                Bomb.sound_loaded = True
            except pygame.error:
                print("Nie udało się załadować pliku .wav z wybuchem.")
                Bomb.sound_loaded = True

    def calculate_blast_tiles(self, board):
        self.blast_tiles = []
        start_col = int((self.x - board.offset_x) // board.tile_size)
        start_row = int((self.y - board.offset_y) // board.tile_size)

        blast_range = BOMB_RANGE
        self.blast_tiles.append((start_row, start_col))
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for d_row, d_col in directions:
            for step in range(1, blast_range + 1):
                check_row = start_row + (d_row * step)
                check_col = start_col + (d_col * step)

                if check_row < 0 or check_row >= len(board.grid) or check_col < 0 or check_col >= len(board.grid[0]):
                    break

                if board.grid[check_row][check_col] == 1:
                    break

                self.blast_tiles.append((check_row, check_col))

    def update(self, board):
        if self.state == "ticking":
            self.timer -= 1
            if self.timer <= 0:
                self.state = "exploding"
                self.current_frame = 0 # explosion starts from the 1st frame of animation

                self.calculate_blast_tiles(board)

                self.explosion_surface = pygame.Surface((board.tile_size, board.tile_size), pygame.SRCALPHA)
                self.explosion_surface.fill((255, 0, 0, 100))

                if Bomb.explosion_sound:
                    Bomb.explosion_sound.play()

        elif self.state == "exploding":
            if int(self.current_frame) >= len(self.explosion_frames) - 1:
                self.state = "done"

    def draw(self, screen, board):
        if self.state == "done":
            return

        if self.state == "exploding":
            for row, col in self.blast_tiles:
                rect_x = (col * board.tile_size) + board.offset_x
                rect_y = (row * board.tile_size) + board.offset_y

                screen.blit(self.explosion_surface, (rect_x, rect_y))

        if self.state == "ticking":
            self.current_frame += ANIMATION_SPEED
            frames = self.idle_frames
            img = frames[int(self.current_frame) % len(frames)]
        else:
            self.current_frame += ANIMATION_SPEED
            frames = self.explosion_frames
            img = frames[int(self.current_frame) % len(frames)]

        screen.blit(img, (self.x, self.y))