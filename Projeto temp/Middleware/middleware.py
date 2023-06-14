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
            'score': {player.name: 0 for player in self.players}
        }

    def process_input(self, player, data):
        print(f"Received from {player.name}: {data}")
        self.notify_players()

    def notify_players(self):
        # mandar os dados a cada jogar
        for player in self.players:
            player.socket.send(str(self.game_state).encode())


class Player:
    def __init__(self, name, socket):
        self.name = name
        self.socket = socket

