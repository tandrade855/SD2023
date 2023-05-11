import socket
import ast
from ui import Ui
import constante


# ----------
# This is the stub for the eco.
# Eco is going to be called in server's side.
# This eco is called by user interface to send the eco message to server.
# ----------

class StubClient:
    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((constante.ENDERECO_SERVIDOR, constante.PORTO))
        self.lost = False
        self.player = None
        self.asteroids = []
        self.lives = None
        self.laser = None

    def send_recv(self, msg: str):
        self.s.send(msg.encode(constante.CODIFICACAO_STR))
        dados_recebidos: bytes = self.s.recv(constante.TAMANHO_MENSAGEM)
        return dados_recebidos.decode(constante.CODIFICACAO_STR)

    @staticmethod
    def decode(literal: str):
        try:
            res = ast.literal_eval(literal)
        except (ValueError, SyntaxError):
            res = literal
        return res

    def initial_data(self):
        #pedir os dados dos objetos aos servidor
        self.player = self.decode(self.send_recv("jogador"))
        aux = self.decode(self.send_recv("asteroides"))
        for item in aux:
            self.asteroids.append(self.decode(item))
        self.laser = self.decode(self.send_recv("laser"))
        self.lives = self.decode(self.send_recv("vidas"))





