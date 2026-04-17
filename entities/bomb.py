from settings import *
from entities.game_object import GameObject
import pygame


class Bomb(GameObject):
    sound_loaded = False
    explosion_sound = None

    animations_loaded = False
    shared_idle_frames = []
    shared_explosion_frames = []
    shared_blast_frames = []  # NOWE: Pamięć podręczna dla klatek ognia

    def __init__(self, x, y, size):
        super().__init__(x, y, size)

        # Ładowanie animacji tylko raz dla wszystkich bomb
        if not Bomb.animations_loaded:
            Bomb.shared_idle_frames = self.load_animation(BOMB_IDLE_PATH, 2, BOMB_FRAME_W, BOMB_FRAME_H)
            Bomb.shared_explosion_frames = self.load_animation(BOMB_EXPLOSION_PATH, 3, BOMB_FRAME_W, BOMB_FRAME_H)
            # Ładujemy nową animację ognia
            Bomb.shared_blast_frames = self.load_animation(BLAST_EFFECT_PATH, BLAST_FRAMES_NUM, BLAST_FRAME_W,
                                                           BLAST_FRAME_H)
            Bomb.animations_loaded = True

        if not Bomb.sound_loaded:
            try:
                Bomb.explosion_sound = pygame.mixer.Sound(BOOM_SOUND_PATH)
                Bomb.explosion_sound.set_volume(0.4)
                Bomb.sound_loaded = True
            except pygame.error:
                print("Nie udało się załadować pliku .wav z wybuchem.")
                Bomb.sound_loaded = True

        self.idle_frames = Bomb.shared_idle_frames
        self.explosion_frames = Bomb.shared_explosion_frames
        self.blast_frames = Bomb.shared_blast_frames  # Przypisanie klatek ognia do bomby

        self.state = "ticking"
        self.timer = EXPLOSION_DURATION * FPS
        self.blast_tiles = []

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
            self.current_frame += ANIMATION_SPEED
            if self.timer <= 0:
                self.state = "exploding"
                self.current_frame = 0
                self.calculate_blast_tiles(board)

                if Bomb.explosion_sound:
                    Bomb.explosion_sound.play()

        elif self.state == "exploding":
            self.current_frame += 0.30
            if int(self.current_frame) >= len(self.blast_frames) - 1:
                self.state = "done"

    def draw(self, screen, board):
        if self.state == "done":
            return

        # Draw blast effect tiles when exploding
        if self.state == "exploding":
            frame_idx = min(int(self.current_frame), len(self.blast_frames) - 1)
            blast_img = self.blast_frames[frame_idx]

            for row, col in self.blast_tiles:
                rect_x = (col * board.tile_size) + board.offset_x
                rect_y = (row * board.tile_size) + board.offset_y
                screen.blit(blast_img, (rect_x, rect_y))

        # Draw the bomb itself
        if self.state == "ticking":
            img = self.idle_frames[int(self.current_frame) % len(self.idle_frames)]
        else:  # "exploding" state
            frame_idx_bomb = min(int(self.current_frame), len(self.explosion_frames) - 1)
            img = self.explosion_frames[frame_idx_bomb]

        screen.blit(img, (self.x, self.y))