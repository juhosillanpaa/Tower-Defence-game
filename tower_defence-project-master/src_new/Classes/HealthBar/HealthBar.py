import pygame

GREEN = (0, 255, 0)
BASE = (171, 171, 171)


class HealthBar:
    def __init__(self, x, y, max_health, width=64, height=8,):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.width = width
        self.height = height

    def draw(self, window, health):
        base_rect = (self.x, self.y, self.width, self.height)
        hp_width = health /self.max_health * self.width
        hp_rect = (self.x, self.y, hp_width, self.height)
        pygame.draw.rect(window, BASE, base_rect)
        pygame.draw.rect(window, GREEN, hp_rect)

    def update_position(self, x, y):
        self.x = x
        self.y = y