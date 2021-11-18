import pygame
import numpy as np
import math
from ..GameObject.GameObject import GameObject


class Bullet():
    def __init__(self, x, y, target_enemy, damage, width=1, height=1, velocity=10, ):
        self.velocity = velocity
        self.target_enemy = target_enemy
        self.damage = damage
        self.has_reached_enemy = False
        self.x = x
        self.y = y

    def move(self):
        # update the position of the bullet if its target is still alive and it hasnt reached it yet
        if self.has_reached_enemy or not self.target_enemy.is_alive:
            return
        path_vec = (self.target_enemy.x - self.x, self.target_enemy.y - self.y)
        distance = np.linalg.norm(path_vec)
        black = (0, 0, 0)
        if distance > self.velocity:
            unit_path_vec = path_vec / distance
            travel_vec = self.velocity * unit_path_vec
            self.x = self.x + travel_vec[0]
            self.y = self.y + travel_vec[1]
        else:
            # bullet collides with enemy
            self.has_reached_enemy = True
            self.target_enemy.reduce_health(self.damage)

    def draw(self, window):
        # draw bullet if it hasnt reached enemy and enemy is still alive
        black = (0, 0, 0)
        if not self.has_reached_enemy and self.target_enemy.is_alive():
            pygame.draw.rect(window, black, (self.x, self.y, 3, 3))
