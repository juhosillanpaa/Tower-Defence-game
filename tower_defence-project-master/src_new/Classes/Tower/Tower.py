import pygame
import numpy as np
import math
from ..GameObject.GameObject import GameObject
from ..Bullet.Bullet import Bullet

class Tower(GameObject):
    def __init__(self, x, y, width, height,
                 fire_rate,
                 firing_distance,
                 barrel_length,
                 damage,
                 norm_vec,
                 image_url,
                 firing_image_url,
                 price
                 ):
        self.fire_rate = fire_rate
        self.firing = False
        self.firing_cd = 0
        self.radius = 32
        self.firing_distance = firing_distance
        self.barrel_length = barrel_length
        self.damage = damage
        self.bullets = []
        self.norm_vec = norm_vec
        self.target_enemy = None
        self.image_url = image_url
        self.firing_image_url = firing_image_url
        self.price = price

        super().__init__(
            x,
            y,
            width=width,
            height=height,
            rotation=0,
            url=self.image_url,
        )

    def get_direction_vector(self):
        if self.target_enemy is not None:
            path_vec = ( self.target_enemy.x - self.x, self.target_enemy.y - self.y)
            distance = np.linalg.norm(path_vec)
            unit_vec = path_vec / distance
            return unit_vec
        else:
            return self.norm_vec

    def clear_bullet_list(self):
        bullets = filter(lambda x: not x.has_reached_enemy and x.target_enemy.is_alive(), self.bullets)
        self.bullets = bullets

    def shoot(self, enemies):
        # If the tower is ready to fire, it will fire a target
        # if its previous target is dead or it is no longer in range, it will find new target
        # In case the tower is not ready to fire, it will update its direction and keep tracking its target.
        self.firing = False
        if self.firing_cd <= 0:     # if possible, shoot enemy
            self.find_target_enemy(enemies)
            if self.target_enemy is not None:
                self.shoot_target_enemy()

        if self.target_enemy is not None:   # keep tracking the target even if tower cannot fire yet
            dir_vec = self.get_direction_vector()
            super().update_rotation(dir_vec, self.norm_vec)

        self.firing_cd -= 1

    def find_target_enemy(self, enemies):
        # Finds the target enemy for the tower
        # if the tower already has target, which is still alive and is in range, it keeps it as target
        # else if finds a new target for the tower
        if self.target_enemy is not None:
            if self.target_enemy.is_alive() and self.is_enemy_in_range(self.target_enemy):
                return

        target = None
        for enemy in enemies:
            if enemy.is_alive():
                dist = np.linalg.norm((self.x - enemy.x, self.y - enemy.y))
                if dist <= self.firing_distance:
                    if target is None:
                        target = enemy
                    elif enemy.distance_travelled > target.distance_travelled:
                        target = enemy
        self.target_enemy = target

    def is_enemy_in_range(self, enemy):
        if self.target_enemy is None:
            return False
        dist = np.linalg.norm((self.x - enemy.x, self.y - enemy.y))
        if dist <= self.firing_distance:
            return True
        else:
            return False

    def shoot_target_enemy(self):
        x, y = self.get_bullet_starting_point()
        bullet = Bullet(
            x,
            y,
            self.target_enemy,
            self.damage
        )
        self.bullets.append(bullet)
        self.firing_cd = self.fire_rate
        self.firing = True

    def get_bullet_starting_point(self):
        unit_dir_vec = self.get_direction_vector()
        travel_vec = unit_dir_vec * self.barrel_length
        x = self.x + travel_vec[0]
        y = self.y + travel_vec[1]
        return x, y

    def draw(self, window):
        if self.firing:
            firing_image = super().get_scaled_image(self.firing_image_url)
            super().draw(window, image=firing_image)
        else:
            super().draw(window)
    def set_position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_position(self):
        return self.x, self.y