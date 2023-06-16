from Middleware.middleware import GameMiddleware
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

        while len(self.middleware.players) < 2:
            client_socket, client_address = self.server_socket.accept()
            print(f"Player connected: {client_address}")

            player = Player(client_socket, client_address, "player " + str(len(self.middleware.players) + 1))
            self.middleware.add_player(player)
            print(self.middleware.players[0].name)

            thread = threading.Thread(target=self.handle_player, args=(player,))
            thread.start()

        self.middleware.start_game()

    def handle_player(self, player):
        temp = self.middleware.receive_msg()
        print(temp)
        self.middleware.send_data(self.middleware.players[0], self.middleware.players[0])

        data = self.middleware.player_data(self.middleware.players[0])
        self.middleware.send_msg("processing...")
        print(data)
        player_width = data[0]
        player_height = data[1]
        while True:
            self.server.tick()
            data = self.middleware.receive_msg()
            if data == "lives":
                self.middleware.send_data(self.server.lives, self.middleware.players[0])
            if data == "player location":
                self.middleware.send_data(PLAYER1, self.middleware.players[0])
            if data == "asteroids":
                self.server.create_asteroids()
                self.middleware.send_data(self.server.asteroids, self.middleware.players[0])
            if data == "laser":
                self.middleware.send_data(self.server.laser, self.middleware.players[0])
            if data == "left" or data == "right" or data == "up":
                self.server.update_positions(data, "Player 1", player_width, player_height)
                self.middleware.send_msg("processing...", self.middleware.players[0])
            if data == "collision":
                self.middleware.send_msg("processing...")
                asteroid = self.middleware.player_data(self.middleware.players[0])
                self.server.asteroids.remove(asteroid)
                self.middleware.send_data(self.server.lives, self.middleware.players[0])
            if not data:
                break

            # Pass player input to the game middleware

        player.socket.close()
        print(f"Player disconnected: {player.address}")
        self.middleware.players.remove(player)


class Player:
    def __init__(self, socket_, address, name: str):
        self.socket = socket_
        self.address = address
        self.name = name


if __name__ == "__main__":
    server = Game()
    run = GameSkeleton(server)
    run.start(SERVER_ADDRESS, PORT)
