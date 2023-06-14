from client_stub import StubClient
import pygame
import os
import time
import random
import constante

pygame.font.init()


WIDTH, HEIGHT = 750, 750
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Destroyer")


# Load Images

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images",
                                                                   "background-black.png")), (WIDTH, HEIGHT))

SPACE_SHIP = pygame.image.load(os.path.join("images", "spaceRocket.png"))
RED_LASER = pygame.image.load(os.path.join("images", "red_laser.png"))

SMALL = pygame.image.load(os.path.join("images", "asteroid50.png"))
MEDIUM = pygame.image.load(os.path.join("images", "asteroid75.png"))
BIG = pygame.image.load(os.path.join("images", "asteroid100.png"))

class Ui:
    def __init__(self, stb_obj: StubClient):
        self.stb_obj = stb_obj

    def run(self):
        dados: str = ""
        self.stb_obj.initial_data()
        player = self.stb_obj.player
        asteroids = self.stb_obj.asteroids
        laser = self.stb_obj.laser
        lives = self.stb_obj.lives
        self.laser()
        self.asteroid()
        self.ship()
        while dados != constante.FIM:
            self.redraw_window()

    def redraw_window(self, player, asteroids, lives, laser):
        win.blit(BACKGROUND, (0, 0))
        lives_label = pygame.font.SysFont("comicsans", 40).render(f"Vidas: {lives}", 1, (255, 255, 255))
        win.blit(lives_label, (580, 10))

        for asteroid in asteroids:
            win.blit(SPACE_SHIP, (asteroid[0], asteroid[1]))

        win.blit(SPACE_SHIP, (player[0], player[1]))
        player.laser(win)

        if self.lost:
            end_label = pygame.font.SysFont("comicsans", 60).render("Perdeu!!", 1, (255, 255, 255))
            win.blit(end_label, (WIDTH/2 - end_label.get_width()/2, 350))

        pygame.display.update()

    def ship(self):
        ship_img = SPACE_SHIP
        pygame.mask.from_surface(ship_img)

    def laser(self):
        laser_img = RED_LASER
        pygame.mask.from_surface(laser_img)

    def asteroid(self, size):
        size_map = {
            "small": SMALL,
            "medium": MEDIUM,
            "big": BIG
        }
        ast = size_map[size]
        pygame.mask.from_surface(ast)