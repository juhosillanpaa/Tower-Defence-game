import pygame
from ..MapItem.mapitem import MapItem


class Grass(MapItem):
    def __init__(self, x, y, width, height):
        self.scaled_image = pygame.transform.scale(
            pygame.image.load("utility/images/grass-pixel.png"),
            (width, height)
        )
        super().__init__(x, y, width, height, 0, self.scaled_image)
