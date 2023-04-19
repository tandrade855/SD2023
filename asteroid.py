from rocket import Rocket
import pygame
import os

SMALL = pygame.image.load(os.path.join("images", "asteroid50.png"))
MEDIUM = pygame.image.load(os.path.join("images", "asteroid75.png"))
BIG = pygame.image.load(os.path.join("images", "asteroid100.png"))


class Asteroid(Rocket):
    SIZE_MAP = {
                "small": SMALL,
                "medium": MEDIUM,
                "big": BIG
    }

    def __init__(self, x, y, size, health=100):
        super().__init__(x, y, health)
        self.ship_img = self.SIZE_MAP[size]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

