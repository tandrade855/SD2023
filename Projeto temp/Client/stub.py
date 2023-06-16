import socket
import threading
from Middleware.middleware import GameMiddleware


class GameStub:

    def __init__(self):
        self.client_socket = None
        self.middleware = GameMiddleware()
        self.player_id = None

    def connect(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        print("Connected to the server.")

        receive_thread = threading.Thread(target=self.tryout)
        receive_thread.start()

    def receive_data_server(self):
        return self.middleware.player_data(self.player_id)

    def send_data_server(self, data):
        self.middleware.send_data(data, self.player_id)

    def send_msg_server(self, msg):
        self.middleware.send_msg(msg, self.player_id)

    def receive_msg_server(self):
        return self.middleware.receive_msg(self.player_id)

    def tryout(self):
        # get player identification
        self.send_msg_server("get player")
        self.player_id = self.receive_msg_server()





