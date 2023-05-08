import pygame


class Rocket:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.laser_x = -300
        self.laser_y = -300

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def draw_laser(self, window):
        window.blit(self.laser_img, (self.laser_x, self.laser_y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def get_laser_width(self):
        return self.laser_img.get_width()

    def get_laser_height(self):
        return self.laser_img.get_height()

    def shape(self):
        return pygame.Rect(self.x, self.y, self.get_width(), self.get_height())

    def shape_laser(self):
        return pygame.Rect(self.laser_x, self.laser_y, self.get_laser_width(), self.get_laser_height())


