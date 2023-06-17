from Middleware.middleware import GameMiddleware, Player
from game import Game
from Server import *
import socket
import threading


class GameSkeleton:

    def __init__(self, server):
        self.middleware = GameMiddleware()
        self.server_socket = None
        self.server = server

    def start(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)

        print("Server started. Waiting for connections...")

        while len(self.middleware.players) < 1:
            client_socket, client_address = self.server_socket.accept()
            print(f"Player connected: {client_address}")

            player = Player(client_socket, client_address, "player " + str(len(self.middleware.players) + 1))
            self.middleware.add_player(player)
            print(self.middleware.players[0].name)
        self.handle_player(self.middleware.players[0])

    def handle_player(self, player):
        data = self.middleware.player_data("player 1")
        print(data)
        self.middleware.send_msg("processing...", "player 1")
        print(data)
        player_width = data[0]
        player_height = data[1]
        while True:
            self.server.tick()
            data = self.middleware.receive_msg()
            if data == "lives":
                self.middleware.send_data(self.server.lives, "player 1")
            if data == "player location":
                self.middleware.send_data(PLAYER1, "player 1")
            if data == "asteroids":
                self.server.create_asteroids()
                self.middleware.send_data(self.server.asteroids, "player  1")
            if data == "laser":
                self.middleware.send_data(self.server.laser, "player 1")
            if data == "left" or data == "right" or data == "up":
                self.server.update_positions(data, "Player 1", player_width, player_height)
                self.middleware.send_msg("processing...", "player 1")
            if data == "collision":
                self.middleware.send_msg("processing...")
                asteroid = self.middleware.player_data("player 1")
                self.server.asteroids.remove(asteroid)
                self.middleware.send_data(self.server.lives, "player 1")
            if data == "quit":
                break
        player.socket.close()
        print(f"Player disconnected: {player.address}")
        self.middleware.players.remove(player)


if __name__ == "__main__":
    server = Game()
    run = GameSkeleton(server)
    run.start(SERVER_ADDRESS, PORT)
