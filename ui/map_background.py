import pygame
from settings import WIDTH, HEIGHT, MAP_BACKGROUNDS


class MapBackground:
    def __init__(self, map_index):
        self.bg_layers = []
        config = MAP_BACKGROUNDS[map_index]

        for layer_data in config:
            # Wczytanie grafiki i skalowanie do rozmiaru okna
            img = pygame.image.load(layer_data["path"]).convert_alpha()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))

            # Pobranie prędkości (domyślnie 0, jeśli nie podano)
            speed = layer_data.get("speed", 0.0)

            self.bg_layers.append({
                "image": img,
                "x": 0,
                "speed": speed
            })

    def draw(self, screen):
        for layer in self.bg_layers:
            # Przesuwanie tła
            layer["x"] -= layer["speed"]

            # Zapętlanie (jeśli obrazek zjedzie za ekran, wraca na początek)
            if layer["x"] <= -WIDTH:
                layer["x"] = 0

            # Rysowanie pierwszej części
            screen.blit(layer["image"], (layer["x"], 0))

            # Rysowanie drugiej części (doklejonej po prawej), żeby zapętlenie było płynne
            if layer["speed"] > 0:
                screen.blit(layer["image"], (layer["x"] + WIDTH, 0))