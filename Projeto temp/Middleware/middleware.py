import json


class GameMiddleware:

    def __init__(self):
        self.players = []
        self.game_state = {}

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def start_game(self):
        # por os dados do jogador neste dict
        self.game_state = {
            'lives': {player.name: 5 for player in self.players}
        }

    def process_input(self, player, data):
        print(f"Received from {player.name}: {data}")
        self.notify_players()

    def notify_players(self, player=None):
        # mandar os dados a cada jogador
        if player is None:
            game_state_json = json.dumps(self.game_state)
            for player in self.players:
                player.socket.send(game_state_json.encode())
        else:
            game_state_json = json.dumps(self.game_state)
            for player in self.players:
                if player.name == player:
                    player.socket.send(game_state_json.encode())

    def player_notification(self, player=None):
        #a fazer este
        if player is None:
            for player in self.players:
                data = json.loads(player.socket.recv(1024).decode())
        else:
            game_state_json = json.dumps(self.game_state)
            for player in self.players:
                if player.name == player:
                    player.socket.send(game_state_json.encode())

    def send_msg(self, player_name, message: str):
        for player in self.players:
            if player == player_name:
                player.socket.send(message.encode())

    def receive_msg(self, player_name):
        message = ""
        for player in self.players:
            if player == player_name:
                message = player.socket.recv(1024).decode()
        return message


class Player:
    def __init__(self, name, socket):
        self.name = name
        self.socket = socket

