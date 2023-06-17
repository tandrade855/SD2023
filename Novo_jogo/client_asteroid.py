import pygame
from constantes import *
import os


ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join("images", "asteroid.png")), (GRID_SIZE, GRID_SIZE))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (WIDTH, HEIGHT))


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.asteroid_img = ASTEROID
        self.mask = pygame.mask.from_surface(self.asteroid_img)

    def draw(self, window):
        window.blit(self.asteroid_img, (self.x * GRID_SIZE, self.y * GRID_SIZE))

    def get_width(self):
        return self.asteroid_img.get_width()

    def get_height(self):
        return self.asteroid_img.get_height()

    def shape(self):
        return pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, self.get_width(), self.get_height())

