import socket
import threading
from Middleware.middleware import GameMiddleware, Player
from Client import *
import pickle


class GameStub:

    def __init__(self):
        self.client_socket = None
        self.middleware = GameMiddleware()
        self.player_id = None
        self.run = False

    def connect(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        print("Connected to the server.")

    def receive_data_server(self):
        data = b"" + self.client_socket.recv(1024)
        deserialized_object = pickle.loads(data)
        return deserialized_object

    def send_data_server(self, data):
        serialized_object = pickle.dumps(data)
        # Send the serialized object
        self.client_socket.sendall(serialized_object)

    def send_msg_server(self, msg):
        self.client_socket.send(msg.encode())

    def receive_msg_server(self):
        return self.client_socket.recv(1024).decode()

    def tryout(self):
        # get player identification
        self.middleware.send_msg("player_id")
        self.player_id = self.middleware.receive_msg()
        print("Player id is:", self.player_id)
        player = Player(self.client_socket, PORT, self.player_id)
        self.middleware.add_player(player)
        print("estou aqui no tryout. a len de players é:", len(self.middleware.players))



