import pygame
import numpy as np
import math


class GameObject:
    def __init__(self, x, y, width, height, rotation, url):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.image = self.get_scaled_image(url)

    def get_scaled_image(self, url):
        image = pygame.transform.scale(
            pygame.image.load(url),
            (self.width, self.height))
        return image

    def update_rotation(self, dir_vec, norm_vec):
        # updates the rotation of the item based on direction vector and vector displaying its images direction

        signed_angle = math.atan2(norm_vec[1], norm_vec[0]) - math.atan2(dir_vec[1], dir_vec[0])
        signed_angle = signed_angle * 180 / math.pi
        self.rotation = signed_angle

    def draw(self, window, image=None):
        # Draw the object based on its rotation
        if image is not None:
            final_image = pygame.transform.rotate(image, self.rotation)
        else:
            final_image = pygame.transform.rotate(self.image, self.rotation)
        window.blit(final_image, (self.x - final_image.get_width() // 2, self.y - final_image.get_height() //2))


