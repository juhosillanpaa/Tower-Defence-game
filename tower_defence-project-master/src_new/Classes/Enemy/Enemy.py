import pygame
import numpy as np
import math
from ..GameObject.GameObject import GameObject
from ..Explosion.Explosion import Explosion
from ..HealthBar.HealthBar import HealthBar


BROKEN_DELAY = 5

class Enemy(GameObject):
    def __init__(self, path, width, height, velocity, max_health, norm_vec, image_url, broken_image_url, bounty, game= None):
        self.velocity = velocity
        self.max_health = max_health
        self.health = max_health
        self.health_bar = HealthBar(0, 0, max_health, width*0.8,)
        self.path = path
        self.target_path_point_index = 1
        self.distance_travelled = 0
        self.show_bullet_hit = False
        self.show_explosion = False
        self.show_broken = 0
        self.norm_vec = norm_vec
        self.image_url = image_url
        self.broken_image_url = broken_image_url
        self.game = game
        self.bounty = bounty
        super().__init__(
            path[0][0],
            path[0][1],
            width=width,
            height=height,
            rotation=0,
            url=self.image_url
        )

    def set_game(self, game):
        self.game = game

    def update_hp_bar_position(self):
        x_pad = self.width*0.1
        self.health_bar.update_position(self.x - self.width//2 + x_pad, self.y + self.height//2)

    def get_direction_vector(self):
        x_dif = self.target_path_point[0] - self.x
        y_dif = self.target_path_point[1] - self.y
        return x_dif, y_dif

    def is_alive(self):
        return True if self.health > 0 else False

    def move(self, castle, dist_already_moved=0):
        if not self.is_alive(): # dead
            return

        dist_to_move = self.velocity - dist_already_moved
        target_point = self.path[self.target_path_point_index]
        path_vec = (target_point[0] - self.x, target_point[1] - self.y)
        dist_to_point = np.linalg.norm(path_vec)
        super().update_rotation(path_vec, self.norm_vec)

        if dist_to_point > dist_to_move:
            # The enemy moves towards the point but doesnt reach it
            unit_path_vec = path_vec / dist_to_point
            travel_vec = dist_to_move * unit_path_vec
            self.x = self.x + travel_vec[0]
            self.y = self.y + travel_vec[1]
        else:
            #The enemy moves to next target point and then continues moving towards next target point
            self.x = target_point[0]
            self.y = target_point[1]
            if self.target_path_point_index < len(self.path) - 1:
                # The point it just reached is not the final point   => update index and call this function again
                self.target_path_point_index += 1
                dist_to_move = dist_to_move - dist_to_point
                if dist_to_move > 0:
                    self.move(castle, dist_already_moved + dist_to_point)
            else:
                castle.reduce_health(5)
                self.health = 0
                self.show_explosion = True
        self.update_hp_bar_position()

    def reduce_health(self, damage):
        if not self.is_alive():     # do nothing if enemy is already dead
            return
        self.health -= damage
        if self.is_alive():
            self.show_bullet_hit = True
        else:
            self.show_explosion = True
            self.show_broken = BROKEN_DELAY
            self.game.add_money(self.bounty)

    def draw(self, window):
        if self.is_alive():
            self.health_bar.draw(window, self.health)
            super().draw(window)
            if self.show_bullet_hit:
                self.show_bullet_hit = False
                explosion = Explosion(self.x, self.y, 1)
                super().draw(window)
                explosion.draw(window)

        elif self.show_broken > 0:
            broken_image = super().get_scaled_image(self.broken_image_url)
            super().draw(window, image=broken_image)
            self.show_broken -= 1

        if self.show_explosion:
            explosion = Explosion(self.x, self.y, 2)
            explosion.draw(window)
            self.show_explosion = False




