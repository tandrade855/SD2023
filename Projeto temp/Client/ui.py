from Client import *
import pygame
import os


class Ui:

    def __init__(self, stub):
        self.stub = stub
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroid Destroyer")
        self.background = pygame.transform.scale(pygame.image.load(os.path.join
                                                                   ("images", "background-black.png")), (WIDTH, HEIGHT))
        self.player_img = pygame.image.load(os.path.join("images", "spaceRocket.png"))
        self.laser_img = pygame.image.load(os.path.join("images", "red_laser.png"))
        self.asteroid_small_img = pygame.image.load(os.path.join("images", "asteroid50.png"))
        self.asteroid_medium_img = pygame.image.load(os.path.join("images", "asteroid75.png"))
        self.asteroid_big_img = pygame.image.load(os.path.join("images", "asteroid100.png"))

    def draw_player(self, x: int, y: int):
        """
        Draws the player spaceship on the map
        :param x: Location X of the player on the map
        :param y: Location Y of the player on the map
        """
        pygame.mask.from_surface(self.player_img)
        self.win.blit(self.player_img, (x, y))

    def draw_laser(self, x: int, y: int):
        """
        Draws the laser on the map
        :param x: Location X of the laser on the map
        :param y: Location Y of the laser on the map
        """
        pygame.mask.from_surface(self.laser_img)
        self.win.blit(self.laser_img, (x, y))

    def draw_asteroid_small(self, x: int, y: int):
        """
        Draws a small asteroid on the map
        :param x: Location X of the asteroid on the map
        :param y: Location Y of the asteroid on the map
        """
        pygame.mask.from_surface(self.asteroid_small_img)
        self.win.blit(self.asteroid_small_img, (x, y))

    def draw_asteroid_medium(self, x: int, y: int):
        """
        Draws a medium asteroid on the map
        :param x: Location X of the asteroid on the map
        :param y: Location Y of the asteroid on the map
        """
        pygame.mask.from_surface(self.asteroid_medium_img)
        self.win.blit(self.asteroid_medium_img, (x, y))

    def draw_asteroid_big(self, x: int, y: int):
        """
        Draws a big asteroid on the map
        :param x: Location X of the asteroid on the map
        :param y: Location Y of the asteroid on the map
        """
        pygame.mask.from_surface(self.asteroid_big_img)
        self.win.blit(self.asteroid_big_img, (x, y))

    def shape_player(self, x: int, y: int):
        """
        Defines the shape of the player on the map
        :param x: Location X of the player on the map
        :param y: Location Y of the player on the map
        :return: The defined shape of the player on the map
        """
        return pygame.Rect(x, y, self.player_img.get_width(), self.player_img.get_height())

    def shape_laser(self, x: int, y: int):
        """
        Defines the shape of the laser on the map
        :param x: Location X of the laser on the map
        :param y: Location Y of the laser on the map
        :return: The defined shape of the laser on the map
        """
        return pygame.Rect(x, y, self.laser_img.get_width(), self.laser_img.get_height())

    def shape_asteroid_small(self, x: int, y: int):
        """
        Defines the shape of a small asteroid on the map
        :param x: Location X of the asteroid on the map
        :param y: Location Y of the steroid on the map
        :return: The defined shape of a small asteroid on the map
        """
        return pygame.Rect(x, y, self.asteroid_small_img.get_width(), self.asteroid_small_img.get_height())

    def shape_asteroid_medium(self, x: int, y: int):
        """
        Defines the shape of a medium asteroid on the map
        :param x: Location X of the asteroid on the map
        :param y: Location Y of the steroid on the map
        :return: The defined shape of a medium asteroid on the map
        """
        return pygame.Rect(x, y, self.asteroid_medium_img.get_width(), self.asteroid_medium_img.get_height())

    def shape_asteroid_big(self, x: int, y: int):
        """
        Defines the shape of a big asteroid on the map
        :param x: Location X of the asteroid on the map
        :param y: Location Y of the steroid on the map
        :return: The defined shape of a big asteroid on the map
        """
        return pygame.Rect(x, y, self.asteroid_big_img.get_width(), self.asteroid_big_img.get_height())

    def draw_lives(self, lives: int):
        """
        Draws the lives text
        :param lives: number of lives to display
        """
        lives_label = pygame.font.SysFont("comicsans", 40).render(f"Vidas: {lives}", 1, LIVES_COLOR)
        self.win.blit(lives_label, LIVES_POSITION)


