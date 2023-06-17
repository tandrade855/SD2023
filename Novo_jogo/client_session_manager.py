from threading import Thread
from GameMechanics import GameMech
import CONSTANT
import json
import logging

# shr: shared.SharedServerState,


class ClientSession(Thread):
    """Maintains a session with the client"""

    def __init__(self, socket_client: int,  game_mech: GameMech):
        """
        Constructs a thread to hold a session with the client
        """
        Thread.__init__(self)
        self.socket_client = socket_client
        self.gm = game_mech

    def process_x_max(self, s_c):
        # pedir ao gm o tamanho do jogo
        x_max = self.gm.get_x_max()
        # enviar a mensagem com esse valor
        s_c.send(x_max.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))

    def process_y_max(self, s_c):
        # pedir ao gm o tamanho do jogo
        y_max = self.gm.get_y_max()
        # enviar a mensagem com esse valor
        s_c.send(y_max.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))

    def process_direction(self, s_c):
        # receber dados necessários
        dados_recebidos: bytes = s_c.recv(CONSTANT.N_BYTES)
        direction = int.from_bytes(dados_recebidos, byteorder="big", signed=True)
        dados_recebidos: bytes = s_c.recv(CONSTANT.N_BYTES)
        nr_player = int.from_bytes(dados_recebidos, byteorder="big", signed=True)
        # mudar a direção de acordo com o input
        self.gm.execute(direction, "player", int(nr_player))

    def process_get_players(self, s_c):
        # obter o dicionário de jogadores
        pl = self.gm.get_players()
        msg = json.dumps(pl)
        # calcular a dimensão do dicionário
        dim = len(msg)
        print(f"dim: {dim}")
        # enviar a dimensão
        s_c.send(dim.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))
        # enviar o dicionário
        s_c.send(msg.encode(CONSTANT.CODIFICACAO_STR))

    def process_get_nr_players(self, s_c):
        # obter o número de jogadores
        nr_pl = self.gm.get_nr_players()
        # enviar esse valor
        s_c.send(nr_pl.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))

    def process_add_player(self, s_c):
        # obter o nome do novo jogador
        data_rcv: bytes = s_c.recv(CONSTANT.MSG_SIZE)
        name = data_rcv.decode(CONSTANT.CODIFICACAO_STR)
        # adicionar o novo jogador ao mundo
        number = self.gm.add_player(name, 5, 1)
        # enviar o número do novo jogador
        s_c.send(number.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))

    def process_get_obstacles(self, s_c):
        # obter dicionário de obstáculos
        ob = self.gm.get_obstacles()
        msg = json.dumps(ob)
        # calcular dimensão do dicinário
        dim = len(msg)
        # enviar dimensão
        s_c.send(dim.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))
        # enviar dados do dicionário
        s_c.send(msg.encode(CONSTANT.CODIFICACAO_STR))

    def process_get_nr_obstacles(self, s_c):
        # obter o número de obstáculos
        nr_ob = self.gm.nr_obstacles
        # enviar esse valor
        s_c.send(nr_ob.to_bytes(CONSTANT.N_BYTES, byteorder="big", signed=True))

    def process_move_player(self, s_c):
        # receber o número do player a mover
        data_rcv: bytes = s_c.recv(CONSTANT.N_BYTES)
        nr_player = int.from_bytes(data_rcv, byteorder="big", signed=True)
        # mover o player
        result = self.gm.move_player(nr_player)
        # enviar resultado
        s_c.send(result.encode(CONSTANT.CODIFICACAO_STR))

    def process_add_first_apple(self, s_c):
        # adicionar primeira maçã
        self.gm.add_apple()

    def dispatch_request(self, socket_client) -> bool:
        """
        :return:
        """
        fim = False
        dados_recebidos: bytes = socket_client.recv(CONSTANT.COMMAND_SIZE)
        msg = dados_recebidos.decode(CONSTANT.CODIFICACAO_STR)
        # logging.debug("o cliente enviou: \"" + msg + "\"")

        if msg == CONSTANT.X_MAX:
            self.process_x_max(socket_client)
        elif msg == CONSTANT.Y_MAX:
            self.process_y_max(socket_client)
        elif msg == CONSTANT.CHANGE_DIR:
            self.process_direction(socket_client)
        elif msg == CONSTANT.GET_PLAYERS:
            self.process_get_players(socket_client)
        elif msg == CONSTANT.NR_PLAYERS:
            self.process_get_nr_players(socket_client)
        elif msg == CONSTANT.ADD_PLAYER:
            self.process_add_player(socket_client)
        elif msg == CONSTANT.GET_OBST:
            self.process_get_obstacles(socket_client)
        elif msg == CONSTANT.NR_OBST:
            self.process_get_nr_obstacles(socket_client)
        elif msg == CONSTANT.MOVE_PLAYER:
            self.process_move_player(socket_client)
        elif msg == CONSTANT.ADD_APPLE:
            self.process_add_first_apple(socket_client)
        elif msg == CONSTANT.END:
            socket_client.send(CONSTANT.END.encode(CONSTANT.CODIFICACAO_STR))
            fim = True
        return fim

    def run(self):
        """Maintains a session with the client, following the established protocol"""
        #logging.debug("Client " + str(client.peer_addr) + " just connected")
        last_request = False
        while not last_request:
            last_request = self.dispatch_request(self.socket_client)
        logging.debug("Client " + str(self.socket_client.peer_addr) + " disconnected")