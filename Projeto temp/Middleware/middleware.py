import pickle


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

    def send_data(self, data, player=None):
        # mandar os dados a cada jogador
        if player is None:
            game_state_json = pickle.dumps(data)
            for player in self.players:
                player.socket.sendall(game_state_json)
        else:
            game_state_json = pickle.dumps(data)
            for players in self.players:
                if players.name == player:
                    print(type(players.socket))
                    players.socket.sendall(game_state_json)

    def player_data(self, player=None):
        data = {}
        if player is None:
            for player in self.players:
                data = pickle.loads(player.socket.recv(1024).decode())
        else:
            for players in self.players:
                if players.name == player:
                    data = b"" + players.socket.recv(1024).decode()
                    pickle.loads(data)
        return data

    def send_msg(self, message: str, player=None):
        if player is None:
            for player in self.players:
                player.socket.send(message.encode())
        else:
            for players in self.players:
                if players.name == player:
                    players.socket.send(message.encode())

    def receive_msg(self, player=None):
        message = "pp"
        if player is None:
            for player in self.players:
                message = player.socket.recv(1024).decode()
        else:
            for players in self.players:
                if players.name == player:
                    players.socket.recv(1024).decode()
        print(message)
        print(self.players)
        return message


class Player:
    def __init__(self, socket_, address, name: str):
        self.socket = socket_
        self.address = address
        self.name = name
