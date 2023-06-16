from Client import *
import pygame
import os
from stub import GameStub


class Ui:

    def __init__(self, stub: GameStub):
        pygame.font.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroid Destroyer")
        self.background = pygame.transform.scale(pygame.image.load(os.path.join
                                                                   ("images", "background-black.png")), (WIDTH, HEIGHT))
        self.player_img = pygame.image.load(os.path.join("images", "spaceRocket.png"))
        self.laser_img = pygame.image.load(os.path.join("images", "red_laser.png"))
        self.asteroid_small_img = pygame.image.load(os.path.join("images", "asteroid50.png"))
        self.asteroid_medium_img = pygame.image.load(os.path.join("images", "asteroid75.png"))
        self.asteroid_big_img = pygame.image.load(os.path.join("images", "asteroid100.png"))
        self.stub = stub
        self.stub.connect(HOST, PORT)

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

    def redraw_window(self, lives, asteroids, player, laser):
        print(lives, asteroids, player, laser)
        self.win.blit(self.background, (0, 0))
        lives_label = pygame.font.SysFont("comicsans", 40).render(f"Vidas: {lives}", 1, (255, 255, 255))
        self.win.blit(lives_label, (580, 10))

        for asteroid in asteroids:
            if asteroid[2] == "small":
                self.draw_asteroid_small(asteroid[0], asteroid[1])
            if asteroid[2] == "medium":
                self.draw_asteroid_medium(asteroid[0], asteroid[1])
            if asteroid[2] == "big":
                self.draw_asteroid_big(asteroid[0], asteroid[1])

        self.draw_player(player[0], player[1])
        self.draw_laser(laser[0], laser[1])

        pygame.display.update()

    def run(self):
        print(self.stub.player_id)
        # sending sprite image info to the server
        self.stub.send_data_server([self.player_img.get_width(), self.player_img.get_height()])
        self.stub.receive_msg_server()

        run = True
        while run:
            self.stub.send_msg_server("lives")
            lives = self.stub.receive_data_server()
            print(lives)

            self.stub.send_msg_server("player_location")
            player = self.stub.receive_data_server()
            print(player)

            self.stub.send_msg_server("asteroids")
            asteroids = self.stub.receive_data_server()
            print(asteroids)

            self.stub.send_msg_server("laser")
            laser = self.stub.receive_data_server()
            print(laser)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.stub.send_msg_server("left")
                player[1] = self.stub.receive_data_server()
            if keys[pygame.K_d]:
                self.stub.send_msg_server("right")
                player[1] = self.stub.receive_data_server()
            if keys[pygame.K_SPACE]:
                self.stub.send_msg_server("up")
                laser = self.stub.receive_data_server()

            self.redraw_window(lives, asteroids, player, laser)

            for asteroid in asteroids[:]:
                if asteroid.shape().colliderect(self.shape_player(player[0], player[1])) or\
                        asteroid.colliderect(self.shape_laser(laser[0], laser[1])):
                    self.stub.send_msg_server("collision")
                    self.stub.receive_msg_server()
                    self.stub.send_data_server(asteroid)
                    lives = self.stub.receive_msg_server()

            if lives <= 0:
                run = False
                end_label = pygame.font.SysFont("comicsans", 60).render("Perdeu!!", 1, (255, 255, 255))
                self.win.blit(end_label, (WIDTH / 2 - end_label.get_width() / 2, 350))


if __name__ == "__main__":
    stub = GameStub()
    ui = Ui(stub)
    ui.run()










