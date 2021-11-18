import pygame
from ..MapItem.mapitem import MapItem


class Road(MapItem):
    def __init__(self, x, y, index, width, height):
        self.index = index
        self.scaled_image = pygame.transform.scale(
            pygame.image.load("utility/images/sand-pixel.png"),
            (width, height)
        )

        super().__init__(x, y, width, height, 0, self.scaled_image)
