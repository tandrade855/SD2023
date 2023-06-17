import pygame
import os
import random
import pygame.font

pygame.font.init()

WIDTH, HEIGHT = 750, 750
GRID_SIZE = 50
NUM_ROWS = HEIGHT // GRID_SIZE
NUM_COLS = WIDTH // GRID_SIZE

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Destroyer")

SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("images", "spaceRocket.png")),
                                    (GRID_SIZE, GRID_SIZE))
RED_LASER = pygame.transform.scale(pygame.image.load(os.path.join("images", "red_laser.png")),
                                   (GRID_SIZE // 2, GRID_SIZE))
ASTEROID = pygame.transform.scale(pygame.image.load(os.path.join("images", "asteroid.png")), (GRID_SIZE, GRID_SIZE))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (WIDTH, HEIGHT))


class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.laser_x = -300
        self.laser_y = -300

    def draw(self, window):
        window.blit(self.ship_img, (self.x * GRID_SIZE, self.y * GRID_SIZE))

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
        return pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, self.get_width(), self.get_height())

    def shape_laser(self):
        return pygame.Rect(self.laser_x, self.laser_y, self.get_laser_width(), self.get_laser_height())

    def check_collision(self, obj):
        return self.shape_laser().colliderect(obj.shape())


class Player(Rocket):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = SPACE_SHIP
        self.laser_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.mask = pygame.mask.from_surface(self.laser_img)
        print(f"Starting Position: ({self.x}, {self.y})")


class Asteroid(Rocket):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = ASTEROID
        self.mask = pygame.mask.from_surface(self.ship_img)


class GameMechanics:
    def __init__(self):
        self.run = True
        self.FPS = 15
        self.player_vel = 1  # Increased player velocity to make movement smoother
        self.laser_vel = 10
        self.asteroids = []
        self.num_asteroids = 5
        self.player = Player(100 // GRID_SIZE, (NUM_ROWS - 1))
        self.clock = pygame.time.Clock()
        self.lost = False
        self.font = pygame.font.SysFont("comicsans", 40)
        self.counter = 0

    def run_game(self):
        while self.run:
            self.clock.tick(self.FPS)

            if len(self.asteroids) == 0:
                self.create_asteroids()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.update_positions()
            self.check_collisions()
            self.redraw_window()

            if self.lost:
                pygame.time.delay(2000)  # Delay for 2 seconds
                self.run = False  # Set run flag to False to exit the game loop

                if self.counter >= 6:
                    print("Congratulations! You destroyed 6 asteroids!")
                else:
                    print("Game Over! You didn't destroy 10 asteroids.")

        pygame.quit()

    def update_positions(self):
        keys = pygame.key.get_pressed()

        grid_x = self.player.x
        grid_y = self.player.y

        if keys[pygame.K_a] and grid_x > 0:  # left
            self.player.x -= 1
        if keys[pygame.K_d] and grid_x < NUM_COLS - 1:  # right
            self.player.x += 1

        self.player.y = NUM_ROWS - 1  # Restrict the player to the last row of the grid

        if keys[pygame.K_SPACE] and self.player.cool_down_counter == 0:
            laser_x = self.player.x * GRID_SIZE + GRID_SIZE // 4
            laser_y = self.player.y * GRID_SIZE - self.player.get_height() // 2 - GRID_SIZE // 2
            self.player.lasers.append((laser_x, laser_y))
            self.player.cool_down_counter = 1

        for laser in self.player.lasers.copy():
            laser_x, laser_y = laser
            laser_y -= self.laser_vel
            if laser_y < 0:
                self.player.lasers.remove(laser)
            else:
                self.player.lasers[self.player.lasers.index(laser)] = (laser_x, laser_y)

        if self.player.cool_down_counter > 0:
            self.player.cool_down_counter += 1
        if self.player.cool_down_counter > 30:
            self.player.cool_down_counter = 0

    def check_collisions(self):
        for asteroid in self.asteroids[:]:
            if self.player.check_collision(asteroid):
                print("estou aqui")
                self.asteroids.remove(asteroid)
                break

            for laser in self.player.lasers[:]:
                laser_rect = pygame.Rect(laser[0], laser[1], GRID_SIZE // 2, GRID_SIZE // 2)
                if laser_rect.colliderect(asteroid.shape()):
                    self.player.lasers.remove(laser)
                    self.asteroids.remove(asteroid)
                    self.counter += 1  # Increment the counter when an asteroid is destroyed
                    if self.counter >= 6:  # Check if the player has destroyed 10 asteroids
                        self.lost = True
                    break

    def redraw_window(self):
        win.blit(BACKGROUND, (0, 0))

        self.draw_grid()  # Draw the grid

        for asteroid in self.asteroids:
            asteroid.draw(win)

        for laser in self.player.lasers:
            laser_x, laser_y = laser
            pygame.draw.rect(win, pygame.Color("red"), (laser_x, laser_y, GRID_SIZE // 2, GRID_SIZE // 2))
            grid_x = laser_x // GRID_SIZE  # Convert x-coordinate to grid coordinate
            grid_y = laser_y // GRID_SIZE  # Convert y-coordinate to grid coordinate
            print(f"Laser Position: ({grid_x}, {grid_y})")  # Print laser position in grid coordinates

        self.player.draw(win)

        counter_text = self.font.render(f"Counter: {self.counter}/6", True, pygame.Color("white"))
        win.blit(counter_text, (10, 10))

        pygame.display.update()

    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(win, pygame.Color("white"), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(win, pygame.Color("white"), (0, y), (WIDTH, y))

    def create_asteroids(self):
        self.asteroids = []
        for _ in range(self.num_asteroids):
            x = random.randint(0, NUM_COLS - 1)
            y = random.randint(0, min(4, NUM_ROWS - 1))
            asteroid = Asteroid(x, y)
            self.asteroids.append(asteroid)
            print(f"Asteroid Position: ({asteroid.x}, {asteroid.y})")


def main():
    game = GameMechanics()
    game.run_game()


if __name__ == "__main__":
    main()