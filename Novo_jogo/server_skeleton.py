import socket
from game_mechanics import GameMechanics
from constantes import *
from typing import Union
import json


class SkeletonServer:

    def __init__(self, gm: GameMechanics):
        self.gm = gm
        self.s = socket.socket()
        self.s.bind((SERVER_ADDRESS, PORT))
        self.s.listen()
        # ------------------------------------------
        # Added timeout
        self.s.settimeout(ACCEPT_TIMEOUT)
        # ------------------------------------------
        self.keep_running = True
        self.socket_client = None

    def accept(self) -> Union['Socket', None]:
        """
        A new definition of accept() to provide a return if a timeout occurs.
        """
        try:
            client_connection, address = self.s.accept()
            logging.info("o cliente com endereço " + str(address) + " ligou-se!")

            return client_connection
        except socket.timeout:
            return None

    def send_counter(self):
        counter = self.gm.counter
        self.socket_client.send(counter.to_bytes(N_BYTES, byteorder="big", signed=True))

    def send_players(self):
        player = self.gm.player
        msg = json.dumps(player)
        dim = len(msg)
        self.socket_client.send(dim.to_bytes(N_BYTES, byteorder="big", signed=True))
        self.socket_client.send(msg.encode(STR_COD))

    def send_asteroids(self):
        asteroids = self.gm.asteroids
        msg = json.dumps(asteroids)
        dim = len(msg)
        self.socket_client.send(dim.to_bytes(N_BYTES, byteorder="big", signed=True))
        self.socket_client.send(msg.encode(STR_COD))

    def send_lasers(self):
        lasers = self.gm.lasers
        msg = json.dumps(lasers)
        print(msg)
        dim = len(msg)
        self.socket_client.send(dim.to_bytes(N_BYTES, byteorder="big", signed=True))
        self.socket_client.send(msg.encode(STR_COD))

    def update_positions(self, msg):
        self.gm.update_positions(msg)

    def run(self):
        logging.info("a escutar no porto " + str(PORT))
        while self.keep_running:
            self.socket_client = self.accept()
            if self.socket_client is not None:
                while True:
                    self.gm.clock.tick(self.gm.FPS)

                    if len(self.gm.asteroids) == 0:
                        self.gm.create_asteroids()

                    self.gm.check_collisions()

                    data_recv: bytes = self.socket_client.recv(MSG_SIZE)
                    msg = data_recv.decode(STR_COD)
                    if msg == GET_COUNTER:
                        self.send_counter()
                    if msg == GET_PLAYERS:
                        self.send_players()
                    if msg == GET_AST:
                        self.send_asteroids()
                    if msg == GET_LASERS:
                        self.send_lasers()
                    if msg == LEFT or msg == RIGHT or msg == UP:
                        self.update_positions(msg)


        self.s.close()


logging.basicConfig(filename=LOG_FILE_NAME,
                    level=LOG_LEVEL,
                    format='%(asctime)s (%(levelname)s): %(message)s')