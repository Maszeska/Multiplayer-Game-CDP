import pygame
from settings import WIDTH, HEIGHT, MAP_BACKGROUNDS

#----------------------------------------------------
# Map background -  paralax backgrounds for map purposes
#----------------------------------------------------

class MapBackground:
    def __init__(self, map_index):
        self.bg_layers = []
        config = MAP_BACKGROUNDS[map_index]

        for layer_data in config:
            img = pygame.image.load(layer_data["path"]).convert_alpha()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            speed = layer_data.get("speed", 0.0)

            self.bg_layers.append({
                "image": img,
                "x": 0,
                "speed": speed
            })

    def draw(self, screen):
        for layer in self.bg_layers:
            layer["x"] -= layer["speed"]
            if layer["x"] <= -WIDTH:
                layer["x"] = 0
            screen.blit(layer["image"], (layer["x"], 0))
            if layer["speed"] > 0:
                screen.blit(layer["image"], (layer["x"] + WIDTH, 0))