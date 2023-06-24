import pygame
from constantes import *
from client_player import Player
from client_asteroid import Asteroid
import os
from client_stub import StubClient
import time

pygame.font.init()
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (WIDTH, HEIGHT))


class Ui:

    def __init__(self, stub: StubClient, player_order=0):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroid Destroyer")
        self.run = True
        self.player_order = player_order
        self.player = Player(100 // GRID_SIZE, (NUM_ROWS - 1))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("comicsans", 40)
        self.lost = False
        self.stub = stub
        self.players = []

    def update_positions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.player_order == 1:
                self.stub.action(LEFT1)
            elif self.player_order == 2:
                self.stub.action(LEFT2)
        if keys[pygame.K_d]:
            if self.player_order == 1:
                self.stub.action(RIGHT1)
            elif self.player_order == 2:
                self.stub.action(RIGHT2)
        if keys[pygame.K_SPACE]:
            if self.player_order == 1:
                self.stub.action(UP1)
            elif self.player_order == 2:
                self.stub.action(UP2)

    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.win, pygame.Color("white"), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.win, pygame.Color("white"), (0, y), (WIDTH, y))

    def redraw_window(self, asteroids, counter, lasers):
        """
        Esta função desenha todos os elementos na janela
        """
        self.win.blit(BACKGROUND, (0, 0))

        self.draw_grid()  # Draw the grid

        for asteroid in asteroids:
            ast = Asteroid(asteroid[0], asteroid[1])
            ast.draw(self.win)

        for laser in lasers:
            laser_x, laser_y = laser
            pygame.draw.rect(self.win, pygame.Color("red"), (laser_x, laser_y, GRID_SIZE // 2, GRID_SIZE // 2))
            grid_x = laser_x // GRID_SIZE  # Convert x-coordinate to grid coordinate
            grid_y = laser_y // GRID_SIZE  # Convert y-coordinate to grid coordinate

        for player in self.players:
            player.draw(self.win)

        counter_text = self.font.render(f"Counter: {counter}/6", True, pygame.Color("white"))
        self.win.blit(counter_text, (10, 10))

        pygame.display.update()

    def run_game(self):
        player = self.stub.get_player()
        self.player = Player(player[0], player[1])
        self.players = self.stub.get_all_players()
        self.player_order = len(self.players)

        while self.run:
            self.players = self.stub.get_all_players()
            for player in range(len(self.players)):
                self.players[player] = Player(self.players[player][0], self.players[player][1])

            self.update_positions()
            time.sleep(0.05)

            counter = self.stub.get_counter()
            lasers = self.stub.get_lasers()
            self.player.lasers = lasers
            asteroids = self.stub.get_asteroids()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stub.remove_player(self.player_order)
                    self.run = False

            if counter == 6:
                self.lost = True

            self.redraw_window(asteroids, counter, lasers)

            if self.lost:
                pygame.time.delay(2000)
                self.run = False
                if counter >= 6:
                    print("Congratulations! You destroyed 6 asteroids!")
                else:
                    print("Game Over! You didn't destroy 10 asteroids.")

        pygame.quit()
        self.stub.s.close()



