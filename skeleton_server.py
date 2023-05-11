import socket
import logging
import constante
from game import *


class SkeletonServer:

    def __init__(self, op: GameOps):
        self.op = op
        self.s = socket.socket()
        self.s.bind((constante.ENDERECO_SERVIDOR, constante.PORTO))
        self.s.listen()

    def run(self):
        logging.info("a escutar no porto " + str(constante.PORTO))
        socket_client, endereco = self.s.accept()

        logging.info("o cliente com endereço " + str(endereco) + " ligou-se!")

        dados: str = ""

        while dados != constante.FIM:
            dados_recebidos: bytes = socket_client.recv(constante.TAMANHO_MENSAGEM)
            dados = dados_recebidos.decode(constante.CODIFICACAO_STR)

            logging.debug("o cliente enviou: \"" + dados + "\"")
            if dados == "esquerda" or dados == "direita":
                operation = self.op.verify_movement(dados, "ship")
                socket_client.send(operation.encode(constante.CODIFICACAO_STR))
            if dados == "laser":
                operation = self.op.verify_movement("cima", "laser")
                socket_client.send(operation.encode(constante.CODIFICACAO_STR))
            if dados == "vidas":
                socket_client.send(str(self.op.life).encode(constante.CODIFICACAO_STR))
            if dados == "asteroides":
                socket_client.send(str(len(self.op.asteroids())).encode(constante.CODIFICACAO_STR))
                asteroids = self.op.asteroids()
                for asteroid in asteroids:
                    ast = asteroid.x, asteroid.y
                    socket_client.send(str(ast).encode(constante.CODIFICACAO_STR))
            if dados == "jogador":
                player = self.op.player()
                socket_client.send(str(player.x, player.y).encode(constante.CODIFICACAO_STR))


logging.basicConfig(filename=constante.NOME_FICHEIRO_LOG,
                    level=constante.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')