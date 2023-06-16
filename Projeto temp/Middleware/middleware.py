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
        print(data)
        if player is None:
            game_state_json = pickle.dumps(data)
            for player in self.players:
                player.socket.sendall()
        else:
            game_state_json = pickle.dumps(data)
            for players in self.players:
                if players.name == player.name:
                    player.socket.sendall()

    def player_data(self, player=None):
        data = {}
        if player is None:
            for player in self.players:
                data = pickle.loads(player.socket.recv(1024).decode())
        else:
            for players in self.players:
                if players.name == player.name:
                    pickle.loads(player.socket.recv(1024).decode())
        return data

    def send_msg(self, message: str, player=None):
        if player is None:
            for player in self.players:
                player.socket.send(message.encode())
        elif player in self.players:
            player.socket.send(message.encode())

    def receive_msg(self, player=None):
        message = ""
        if player is None:
            for player in self.players:
                message = player.socket.recv(1024).decode()
        elif player in self.players:
            player.socket.recv(1024).decode()
        return message

