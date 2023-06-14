import socket
import threading
import json
from Middleware.middleware import GameMiddleware


class GameStub:

    def __init__(self):
        self.client_socket = None
        self.middleware = GameMiddleware()

    def connect(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        print("Connected to the server.")

        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

        self.send_data()

    def receive_data(self):
        data = json.loads(self.client_socket.recv(1024).decode())
        return data

    def send_data(self):
        data = input("Enter your input: ")
