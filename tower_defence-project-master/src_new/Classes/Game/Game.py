import pygame
import numpy as np
from ..Map.Map import Map
from ..Enemy.RedEnemy import RedEnemy
from ..Level.Level import Level
WIDTH, HEIGHT = 900, 640
pygame.display.set_caption("Tower defense")
WHITE = (255, 255, 255)
FPS = 10


class Game:
    def __init__(self, config_path, game_surface):
        self.config_path = config_path
        self.game_surface = game_surface
        self.fps = 10
        self.map = Map(config_path, WIDTH, HEIGHT, game_surface)
        self.towers = []
        self.enemies = []
        self.levels = self.read_levels()
        self.current_level = 0
        self.level_started = False
        self.money = 100
        self.won = False
        self.lost = False


    def start_round(self):
        self.level_started = True

    def check_if_level_is_completed(self):
        alive_enemies = self.get_alive_enemies()
        current_level = self.levels[self.current_level]
        if len(alive_enemies) == 0 and current_level.have_all_spawned():
            return True
        else:
            return False

    def get_alive_enemies(self):
        filtered = filter(lambda x: x.is_alive(), self.enemies)
        return list(filtered)

    def draw_all(self):
        self.game_surface.fill(WHITE)
        self.map.draw_map()
        self.map.draw_path()
        self.draw_enemies()
        self.draw_towers()

    def update_all(self):
        self.levels[self.current_level].spawn_enemies(self)
        self.move_enemies()
        self.fire_towers()

    def run_iteration(self):
        if self.get_hp() <= 0:
            self.lost = True
            return
        if self.won:
            return

        if self.level_started and self.check_if_level_is_completed():
            #user completed last level => start new level or let user know he won
            if self.current_level +1 == len(self.levels):
                self.won = True
                return
            else:
                self.level_started = False
                self.current_level += 1

        if self.level_started:
            self.update_all()

        self.draw_all()

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move(self.map.castle)

    def fire_towers(self):
        for tower in self.towers:
            tower.shoot(self.enemies)
            for bullet in tower.bullets:
                bullet.move()

    def draw_towers(self):
        for tower in self.towers:
            tower.draw(self.game_surface)
            for bullet in tower.bullets:
                bullet.draw(self.game_surface)

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.game_surface)


    def append_enemy(self, new_enemy):
        self.enemies.append(new_enemy)

    def read_levels(self):
        file = open(self.config_path, "r")
        levels = []
        level = 1
        for row in file:
            if row[0:7] == "#levels":
                break
        for row in file:
            level_desc = row.rstrip().split(",")
            action_arr = []
            for action in level_desc:
                if action.isnumeric():
                    action_arr.append(int(action))
                elif action == 'e':
                    enemy = RedEnemy(self.map.path)
                    action_arr.append(enemy)
            new_level = Level(level=level, action_arr=action_arr)
            levels.append(new_level)
            level += 1
        return levels

    def set_towers(self, towers):
        self.towers = towers


    def can_place_tower(self, pos):
        if self.game_surface.get_rect().collidepoint(pos):
            if self.map.is_grass(pos):
                for t in self.towers:
                    pos2 = t.get_position()
                    if np.linalg.norm((pos[0]-pos2[0], pos[1] - pos2[1])) < t.radius:
                        return False
                return True
        return False



    def add_tower(self, tower):
        self.towers.append(tower)

    def get_current_level_number(self):
        return self.current_level + 1

    def get_hp(self):
        return self.map.get_hp()

    def can_afford(self, price):
        if self.money >= price:
            return True
        else:
            return False

    def reduce_money(self, amount):
        self.money -= amount

    def add_money(self, amount):
        self.money += amount
