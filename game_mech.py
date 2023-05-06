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


class GameMechanics:
    def __init__(self):
        self.run = True
        self.FPS = 60
        self.lives = 5
        self.player_vel = 5
        self.asteroids = []
        self.wave_lenght = 5
        self.asteroid_vel = 1
        self.player = Player(300, 650)
        self.clock = pygame.time.Clock()
        self.lost = False

    def run_game(self):
        while self.run:
            self.clock.tick(self.FPS)

            if self.lives <= 0 or self.player.health <= 0:
                self.lost = True

            if len(self.asteroids) == 0:
                self.wave_lenght += 5
                for i in range(self.wave_lenght):
                    asteroid = Asteroid(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["small","medium","big"]))
                    self.asteroids.append(asteroid)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.update_positions()
            self.redraw_window()

    def update_positions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.player.x - self.player_vel > 0: #left
            self.player.x -= self.player_vel
        if keys[pygame.K_d] and self.player.x + self.player_vel + self.player.get_width() < WIDTH: #right
            self.player.x += self.player_vel
        if keys[pygame.K_w] and self.player.y - self.player_vel > 0: #up
            self.player.y -= self.player_vel
        if keys[pygame.K_s] and self.player.y + self.player_vel + self.player.get_height() < HEIGHT: #down
            self.player.y += self.player_vel

        for asteroid in self.asteroids[:]:
            asteroid.move(self.asteroid_vel)
            if asteroid.y + asteroid.get_height() > HEIGHT:
                self.lives -= 1
                self.asteroids.remove(asteroid)
            if asteroid.shape().colliderect(self.player.shape()):
                self.lives -= 1
                self.asteroids.remove(asteroid)

    def redraw_window(self):
        win.blit(BACKGROUND, (0, 0))
        lives_label = pygame.font.SysFont("comicsans", 40).render(f"Vidas: {self.lives}", 1, (255,255,255))
        win.blit(lives_label, (580, 10))

        for asteroid in self.asteroids:
            asteroid.draw(win)

        self.player.draw(win)

        if self.lost:
            end_label = pygame.font.SysFont("comicsans", 60).render("Perdeu!!", 1, (255,255,255))
            win.blit(end_label, (WIDTH/2 - end_label.get_width()/2, 350))

        pygame.display.update()

