import socket
from typing import Union

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

    def com(self, msg: str) -> Union[str, None]:
        self.s.send(msg.encode(constante.CODIFICACAO_STR))

        if msg != constante.FIM:
            dados_recebidos: bytes = self.s.recv(constante.TAMANHO_MENSAGEM)
            return dados_recebidos.decode(constante.CODIFICACAO_STR)
        else:
            self.s.close()
