import socket
from constantes import *
import json


class StubClient:

    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((SERVER_ADDRESS, PORT))

    def get_asteroids(self):
        msg = GET_AST
        self.s.send(msg.encode(STR_COD))
        value = self.s.recv(N_BYTES)
        dim = int.from_bytes(value, byteorder='big', signed=True)
        ast_dict = self.s.recv(dim)
        asteroids = json.loads(ast_dict)
        return asteroids

    def get_counter(self):
        msg = GET_COUNTER
        self.s.send(msg.encode(STR_COD))
        data_recv = self.s.recv(N_BYTES)
        counter = int.from_bytes(data_recv, byteorder="big", signed=True)
        return counter

    def get_player(self):
        msg = GET_PLAYERS
        self.s.send(msg.encode(STR_COD))
        value = self.s.recv(N_BYTES)
        dim = int.from_bytes(value, byteorder='big', signed=True)
        player_dict = self.s.recv(dim)
        player = json.loads(player_dict)
        return player

    def get_all_players(self):
        msg = ALL_PLAYERS
        self.s.send(msg.encode(STR_COD))
        value = self.s.recv(N_BYTES)
        dim = int.from_bytes(value, byteorder='big', signed=True)
        players_dict = self.s.recv(dim)
        players = json.loads(players_dict)
        return players

    def get_lasers(self):
        msg = GET_LASERS
        self.s.send(msg.encode(STR_COD))
        value = self.s.recv(N_BYTES)
        dim = int.from_bytes(value, byteorder='big', signed=True)
        laser_dict = self.s.recv(dim)
        lasers = json.loads(laser_dict)
        return lasers

    def remove_player(self, order):
        if order == 1:
            msg = REM_PLAYER1
            self.s.send(msg.encode(STR_COD))
        if order == 2:
            msg = REM_PLAYER2
            self.s.send(msg.encode(STR_COD))

    def action(self, choice):
        msg = choice
        self.s.send(msg.encode(STR_COD))

    def start(self):
        msg = START
        self.s.send(msg.encode(STR_COD))
        data_recv = self.s.recv(N_BYTES)
        start = int.from_bytes(data_recv, byteorder="big", signed=True)
        return start
