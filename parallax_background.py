import pygame.transform
from pygame.examples.grid import TILE_SIZE

from other_objects import *


class ParallaxBackground:
    def __init__(self, layer_config):

        self.bg_layers = []

        self.overlay = pygame.image.load(OVERLAY).convert_alpha()
        self.overlay = pygame.transform.scale(self.overlay, (WIDTH, HEIGHT))
        self.overlay.set_alpha(25)

        for i, config in enumerate(layer_config):
            if i == 0:
                img = pygame.image.load(config["path"]).convert()
            else:
                img = pygame.image.load(config["path"]).convert_alpha()

            img = pygame.transform.scale(img, (WIDTH, HEIGHT))

            self.bg_layers.append({
                "image": img,
                "x": 0,
                "speed": config["speed"]
            })
        margin_right = 150
        ground_offset = 265

        dino_x = WIDTH - TILE_SIZE - margin_right
        dino_y = HEIGHT - TILE_SIZE - ground_offset

        self.dino = BackgroundDino(dino_x, dino_y, TILE_SIZE)

    def draw(self, screen):
        for layer in self.bg_layers:
            layer["x"] -= layer["speed"]

            if layer["x"] <= -WIDTH:
                layer["x"] = 0

            screen.blit(layer["image"], (layer["x"], 0))

            if layer["speed"] > 0:
                screen.blit(layer["image"], (layer["x"] + WIDTH, 0))

        self.dino.update_and_draw(screen)

        screen.blit(self.overlay, (0, 0))