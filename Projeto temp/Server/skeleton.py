from Middleware.middleware import GameMiddleware
from game import Game
import socket
import threading


class GameSkeleton:

    def __init__(self):
        self.middleware = GameMiddleware()
        self.server_socket = None
        self.server = None
        self.players = []

    def start(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)

        print("Server started. Waiting for connections...")

        while len(self.players) < 2:
            client_socket, client_address = self.server_socket.accept()
            print(f"Player connected: {client_address}")

            player = Player(client_socket, client_address)
            self.players.append(player)

            thread = threading.Thread(target=self.handle_player, args=(player,))
            thread.start()

        self.middleware.start_game()

    def handle_player(self, player):
        while True:
            data = player.socket.recv(1024).decode()

            if not data:
                break

            # Pass player input to the game middleware
            self.middleware.process_input(player, data)

        player.socket.close()
        print(f"Player disconnected: {player.address}")
        self.players.remove(player)


class Player:
    def __init__(self, socket_, address):
        self.socket = socket_
        self.address = address
