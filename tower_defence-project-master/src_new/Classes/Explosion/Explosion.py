import pygame
import numpy as np
import math
from ..GameObject.GameObject import GameObject


class Explosion(GameObject):
    def __init__(self, x, y, level):
        self.width = 25 if level == 1 else 50
        self.height = 25 if level == 1 else 50
        self.url = "utility/images/explosion.png"
        super().__init__(x, y, self.width, self.height,
                         rotation=0,
                         url=self.url )