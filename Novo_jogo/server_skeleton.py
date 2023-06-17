import socket
from game_mechanics import GameMechanics
from constantes import *
from typing import Union
from client_session_manager import ClientSession


class SkeletonServer:

    def __init__(self, gm: GameMechanics):
        self.gm = gm
        self.s = socket.socket()
        self.s.bind((SERVER_ADDRESS, PORT))
        self.s.listen(2)
        # ------------------------------------------
        # Added timeout
        self.s.settimeout(ACCEPT_TIMEOUT)
        # ------------------------------------------
        self.keep_running = True
        self.socket_client = None
        self.player_positions = [[2, 14], [7, 14]]
        self.players = []

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

    def run(self):
        logging.info("a escutar no porto " + str(PORT))
        while self.keep_running:
            self.socket_client = self.accept()
            if self.socket_client is not None:
                print("Game Started. Players in game: ", len(self.players))
                print(self.player_positions)

                self.gm.add_player(self.player_positions[0])
                self.gm.players.append(self.player_positions[0])

                self.players.append(self.player_positions[0])
                self.player_positions.remove(self.player_positions[0])

                ClientSession(self.socket_client, self.gm).start()

        self.s.close()


logging.basicConfig(filename=LOG_FILE_NAME,
                    level=LOG_LEVEL,
                    format='%(asctime)s (%(levelname)s): %(message)s')