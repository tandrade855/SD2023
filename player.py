from rocket import Rocket
import pygame
import os

SPACE_SHIP = pygame.image.load(os.path.join("images","spaceRocket.png"))
RED_LASER = pygame.image.load(os.path.join("images","red_laser.png"))

class Player(Rocket):
    def __init__(self,x, y , health=100):
        super().__init__(x,y,health)
        self.ship_img = SPACE_SHIP
        self.laser_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

