from Server import *
from pygame import time as time
import random


class Game:

    def __init__(self):
        self.FPS = FPS
        self.lives = 5
        self.player_vel = 5
        self.laser_vel = 3
        self.asteroids = []
        self.wave_length = 5
        self.asteroid_vel = 1
        self.clock = time.Clock()
        self.lost = False
        self.laser = [WIDTH + 1500, HEIGHT + 1500, "laser"]
        self.players = {"Player 1": PLAYER1,
                        "Player 2": PLAYER2
                        }

    def tick(self):
        self.clock.tick(FPS)

    def check_lost(self):
        if self.lives <= 0:
            self.lost = True

    def create_asteroids(self):
        if len(self.asteroids) == 0:
            self.wave_length += 5
            for i in range(self.wave_length):
                asteroid = [random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                            random.choice(["small asteroid", "medium asteroid", "big asteroid"])]
                self.asteroids.append(asteroid)

    def update_positions(self, choice: str, player_name: str, player_width, player_height):
        if choice == "left" and self.players[player_name][0] - self.player_vel > 0: #left
            self.players[player_name][0] -= self.player_vel
        if choice == "right" and self.players[player_name][0] + self.player_vel + player_width < WIDTH: #right
            self.players[player_name][0] += self.player_vel
        if choice == "shoot":
            self.laser[0] = self.players[player_name][0] + 3
            self.laser[1] = self.players[player_name][1] - player_height/2 - 10

        self.laser[1] -= self.laser_vel

        if self.laser[1] <= 0:
            self.laser[1] = -300



