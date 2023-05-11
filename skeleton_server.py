import socket
import logging
import constante
from game import *
import pygame


class SkeletonServer:

    def __init__(self, op: GameOps):
        self.op = op
        self.s = socket.socket()
        self.s.bind((constante.ENDERECO_SERVIDOR, constante.PORTO))
        self.s.listen()
        self.clock = pygame.time.Clock
        self.lost = False
        self.wave_length = self.op.wave_length
        self.collision = False
        self.FPS = self.op.FPS

    def run(self):
        logging.info("a escutar no porto " + str(constante.PORTO))
        socket_client, endereco = self.s.accept()

        logging.info("o cliente com endereço " + str(endereco) + " ligou-se!")

        dados: str = ""

        while dados != constante.FIM:
            dados_recebidos: bytes = socket_client.recv(constante.TAMANHO_MENSAGEM)
            dados = dados_recebidos.decode(constante.CODIFICACAO_STR)

            logging.debug("o cliente enviou: \"" + dados + "\"")

            self.clock.tick(self.FPS)

            if self.op.lives <= 0:
                self.lost = True

            if len(self.op.asteroids) == 0:
                self.op.wave_length += 5
                for i in range(self.wave_length):
                    asteroid = Asteroid(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                                        random.choice(["small", "medium", "big"]))
                    self.op.asteroids.append(asteroid)

            self.choices(dados, socket_client)

            self.op.player.laser_y -= 1
            if self.op.player.laser_y < 0:
                self.op.player.laser_y = - 300  # temporário, tirar quando se resolver os diferentes lasers

            for asteroid in self.op.asteroids[:]:
                asteroid.move(self.op.asteroid_vel)
                if asteroid.y + asteroid.get_height() > HEIGHT:
                    self.op.lives -= 1
                    self.op.asteroids.remove(asteroid)
                if not self.collision:
                    self.op.lives -= 1
                    self.op.asteroids.remove(asteroid)
                    self.collision = False
                if not self.collision and self.op.player.laser_x > 0:
                    self.op.asteroids.remove(asteroid)
                    self.op.player.laser_y = -300
                    self.collision = False

    def choices(self, choice, socket_client):
        if choice == "esquerda" or choice == "direita":
            operation = self.op.verify_movement(choice, "ship")
            socket_client.send(operation.encode(constante.CODIFICACAO_STR))
        if choice == "laser":
            operation = self.op.verify_movement("cima", "laser")
            socket_client.send(operation.encode(constante.CODIFICACAO_STR))
        if choice == "vidas":
            socket_client.send(str(self.op.life).encode(constante.CODIFICACAO_STR))
        if choice == "asteroides":
            socket_client.send(str(len(self.op.asteroids())).encode(constante.CODIFICACAO_STR))
            asteroids = self.op.asteroids()
            ast = []
            for asteroid in asteroids:
                ast_aux = asteroid.x, asteroid.y
                ast.append(str(ast_aux))
            socket_client.send(str(ast).encode(constante.CODIFICACAO_STR))
        if choice == "colidiu":
            self.collision = True
            socket_client.send("apagar asteroide")
        if choice == "jogador":
            player = self.op.player()
            socket_client.send(str(player.x, player.y).encode(constante.CODIFICACAO_STR))


logging.basicConfig(filename=constante.NOME_FICHEIRO_LOG,
                    level=constante.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')