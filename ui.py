from player import Player
from asteroid import Asteroid
import pygame
import os
import time
import random
pygame.font.init()


WIDTH, HEIGHT = 750, 750
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Destroyer")


# Load Images

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images",
                                                                   "background-black.png")), (WIDTH, HEIGHT))

class Ui:
    def __init__(self):
        self.run = True
        self.FPS = 60
        self.lives = 5
        self.player_vel = 5
        self.laser_vel = 3
        self.asteroids = []
        self.wave_lenght = 5
        self.asteroid_vel = 1
        self.player = Player(300, 650)
        self.clock = pygame.time.Clock()
        self.lost = False

    def update_positions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            #manda para o servidor "esquerda"
        if keys[pygame.K_d] and self.player.x + self.player_vel + self.player.get_width() < WIDTH:  # right
            self.player.x += self.player_vel
        if keys[pygame.K_SPACE]:
            self.player.laser_x = self.player.x + 3
            self.player.laser_y = self.player.y - self.player.get_height() / 2 - 10

        self.player.laser_y -= self.laser_vel

        if self.player.laser_y < 0:
            self.player.laser_y = - 300  # temporário, tirar quando se resolver os diferentes lasers

        for asteroid in self.asteroids[:]:
            asteroid.move(self.asteroid_vel)
            if asteroid.y + asteroid.get_height() > HEIGHT:
                self.lives -= 1
                self.asteroids.remove(asteroid)
            if asteroid.shape().colliderect(self.player.shape()):
                self.lives -= 1
                self.asteroids.remove(asteroid)
            if asteroid.shape().colliderect(self.player.shape_laser()):
                self.asteroids.remove(asteroid)
                self.player.laser_y = -300