import logging

WIDTH, HEIGHT = 750, 750
GRID_SIZE = 50
PLAYER_H = 50
NUM_ROWS = HEIGHT // GRID_SIZE
NUM_COLS = WIDTH // GRID_SIZE
HOST = '127.0.0.1'
PORT = 5001
SERVER_ADDRESS = '127.0.0.1'
LEFT =        "left       "
RIGHT =       "right      "
UP =          "up         "
END =         "end        "

GET_COUNTER = "get counter"
ADD_PLAYER =  "add player "
GET_PLAYERS = "get players"
GET_AST    =  "get ast    "
REM_PLAYER1=  "rem player1"
REM_PLAYER2=  "rem player2"
GET_LASERS =  "get lasers "
ALL_PLAYERS = "all players"
START       = "start      "

MSG_SIZE = 11
N_BYTES = 2
ACCEPT_TIMEOUT = 1
BIG_MSG_SIZE = 100
STR_COD = 'utf-8'
LOG_FILE_NAME = "game-server.log"
LOG_LEVEL = logging.DEBUG
