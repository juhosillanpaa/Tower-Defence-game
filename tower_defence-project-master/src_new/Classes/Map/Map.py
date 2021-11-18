import pygame
import math
from ..MapTile.Road import Road
from ..MapTile.Grass import Grass
from ..Castle.Castle import Castle

class Map:
    def __init__(self, filename, width, height, game_surface):
        self.filename = filename
        self.width = width
        self.height = height
        self.game_surface = game_surface
        self.tile_size = 64
        self.tile_map = self.read_map_from_file()
        self.path = self.make_path()
        self.castle = self.place_castle()


    def read_map_from_file(self):
        file = open(self.filename, "r")
        map_matrix = []
        y = 0
        for row in file:        #Read until map
            if row[0:4] == "#map":
                break

        for row in file:
            if row[0] == "#":   # end of map section
                break
            x = 0
            map_row = []
            txt = row.rstrip().split(",")
            for key in txt:
                if key == "0":
                    map_row.append(Grass(x , y, self.tile_size, self.tile_size))
                elif key != "":
                    map_row.append(Road(x, y, int(key), self.tile_size, self.tile_size))
                x += self.tile_size
            map_matrix.append(map_row)
            y += self.tile_size
        return map_matrix



    def make_path(self):
        #Create a array of tuples that represent the path the enemy units walk
        road_tiles = []
        path = []
        for row in self.tile_map:
            for item in row:
                if isinstance(item, Road):
                    road_tiles.append(item)
        road_tiles.sort(key=lambda x: x.index)
        prev = road_tiles[0]
        # Check intermediate points by adding the middle of each tile into path-array
        for index, item in enumerate(road_tiles):
            if index == 0:
                # add the beginning of the first tile as starting point
                path.append((prev.x, prev.y + prev.height // 2))
            path.append((item.x + item.width // 2, item.y + item.height // 2))
            if index + 1 == len(road_tiles):
                # add the end point as the edge of last tile
                path.append((item.x + item.width, item.y + prev.height // 2))

        return path

    def place_castle(self):
        x, y = self.path[len(self.path) - 1]
        castle = Castle(x, y, 64, 64)
        return castle

    def draw_map(self):
        for row in self.tile_map:
            for item in row:
                item.draw(self.game_surface)
        self.castle.draw(self.game_surface)

    def draw_path(self):
        prev = (0, 0)
        black = (0, 0, 0)
        for index, point in enumerate(self.path):
            if index == 0:
                prev = point
                continue
            pygame.draw.line(self.game_surface, black, prev, point)
            prev = point

    def is_grass(self, pos):
        x, y = pos
        x_index = math.floor(x / self.tile_size)
        y_index = math.floor(y / self.tile_size)
        if x_index > 7 or y_index > 7:      # dummy way, make better
            return False
        item = self.tile_map[y_index][x_index]

        if isinstance(item, Grass):
            return True
        else:
            return False

    def get_hp(self):
        return self.castle.health