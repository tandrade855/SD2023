from player import Player
from asteroid import Asteroid
import os
import time
import random


WIDTH, HEIGHT = 750, 750


class GameOps:

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.FPS = 60
        self.lives = 5
        self.player_vel = 5
        self.laser_vel = 3
        self.asteroids = []
        self.wave_length = 5
        self.asteroid_vel = 1
        self.player = Player(300, 650)
        self.lost = False

    def verify_movement(self, direction, obj):
        if direction == "esquerda" and obj == "ship" and self.player.x - self.player_vel > 0:
            self.player.x -= self.player_vel
            return str(self.player.x - self.player_vel)
        elif direction == "direita" and obj == "ship" and self.player.x + self.player_vel + \
                self.player.get_width() < self.width:
            self.player.x += self.player_vel
            return str(self.player.x + self.player_vel)
        elif direction == "cima" and obj == "laser":
            self.player.laser_x = self.player.x + 3
            self.player.laser_y = self.player.y - self.player.get_height() / 2 - 10
            return str(self.player.laser_x, self.player.laser_y)
        else:
            return ""

    def update_ast(self, col=False):
        for asteroid in self.asteroids[:]:
            asteroid.move(self.asteroid_vel)
            if asteroid.y + asteroid.get_height() > HEIGHT:
                self.lives -= 1
                self.asteroids.remove(asteroid)
            if not col:
                self.lives -= 1
                self.asteroids.remove(asteroid)

    def player(self):
        return self.player

    def life(self):
        return self.lives

    def asteroids(self):
        return self.asteroids

    def laser(self):
        return self.player.laser_x, self.player.laser_y
