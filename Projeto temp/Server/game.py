from Server import *
from pygame import time as time


class Game:

    def __init__(self):
        self.run = True
        self.FPS = FPS
        self.lives = 5
        self.player_vel = 5
        self.laser_vel = 3
        self.asteroids = []
        self.wave_length = 5
        self.asteroid_vel = 1
        self.clock = time.Clock()
        self.lost = False

    def run(self):
        self.clock.tick(self.FPS)

        if self.lives <= 0:
            self.lost = True


