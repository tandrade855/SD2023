import socket
import threading
from Middleware.middleware import GameMiddleware


class GameStub:

    def __init__(self, player_name):
        self.client_socket = None
        self.middleware = GameMiddleware()
        self.player_name = player_name

    def connect(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        print("Connected to the server.")

        receive_thread = threading.Thread(target=self.receive_data_server)
        receive_thread.start()

        self.send_data_server(self.player_name)

    def receive_data_server(self):
        return self.middleware.player_data(self.player_name)

    def send_data_server(self, data):
        self.middleware.send_data(data)

    def send_msg_server(self, msg):
        self.middleware.send_msg(self.player_name, msg)

    def receive_msg_server(self):
        return self.middleware.receive_msg(self.player_name)

