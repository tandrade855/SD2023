import pygame
from constantes import *
import os


SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("images", "spaceRocket.png")),
                                    (GRID_SIZE, GRID_SIZE))
RED_LASER = pygame.transform.scale(pygame.image.load(os.path.join("images", "red_laser.png")),
                                   (GRID_SIZE // 2, GRID_SIZE))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (WIDTH, HEIGHT))


class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.laser_x = -300
        self.laser_y = -300

    def draw(self, window):
        window.blit(self.ship_img, (self.x * GRID_SIZE, self.y * GRID_SIZE))

    def draw_laser(self, window):
        window.blit(self.laser_img, (self.laser_x, self.laser_y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def get_laser_width(self):
        return self.laser_img.get_width()

    def get_laser_height(self):
        return self.laser_img.get_height()

    def shape(self):
        return pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, self.get_width(), self.get_height())

    def shape_laser(self):
        return pygame.Rect(self.laser_x, self.laser_y, self.get_laser_width(), self.get_laser_height())

    def check_collision(self, obj):
        return self.shape_laser().colliderect(obj.shape())


class Player(Rocket):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = SPACE_SHIP
        self.laser_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.mask = pygame.mask.from_surface(self.laser_img)
        #print(f"Starting Position: ({self.x}, {self.y})")
