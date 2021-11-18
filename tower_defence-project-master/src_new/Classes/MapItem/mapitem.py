import os
import pygame


class MapItem:
    def __init__(self, x, y, height, width, rotation, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.image = image

    def draw(self, window):
        final_image = pygame.transform.rotate(
            self.image, self.rotation
        )
        window.blit(final_image, (self.x, self.y))


    def update_rotation(self, rotation):
        self.rotation = rotation

