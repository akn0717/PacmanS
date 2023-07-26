# adapted from https://realpython.com/python-sockets/
from multiprocessing import Queue
import socket
import threading
from game.game_sprites import Pacman
from game.global_constants import Message_Type
import game.global_constants as global_constants
import game.global_variables as global_variables
import numpy as np
from network.utils import *


class Game_Client:
    def __init__(self):
        # socket.SOCK_STREAM is TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendDataToServer(self, message):
        self.sendAndFlush(message)

    def startListener(self):
        self.listening_thread = threading.Thread(target=self.__listen)
        self.listening_thread.start()

    def sendAndFlush(self, message):
        self.socket.sendall(message)
        flush(self.socket)

    def __listen(self):
        bufferQueue = Queue()
        while True:
            recv_data = self.socket.recv(
                global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
            )
            if recv_data:
                data = splitBuffer(recv_data)
                for i in range(len(data)):
                    bufferQueue.put(data[i])

            while not (bufferQueue.empty()):
                token = int(bufferQueue.get())
                if token == Message_Type.INITIAL_BOARD.value:
                    data = [
                        int(bufferQueue.get())
                        for _ in range(
                            2
                            + global_constants.CANVAS_SIZE[0]
                            * global_constants.CANVAS_SIZE[1]
                        )
                    ]
                    with global_variables.MUTEX_CANVAS:
                        global_variables.CANVAS.board_data = np.reshape(
                            np.asarray(data[2:]), (data[0], data[1])
                        )
                elif token == Message_Type.PLAYER_POSITION.value:
                    data = [bufferQueue.get() for _ in range(3)]
                    player_id = int(data[0])
                    player_position = (int(data[1]), int(data[2]))
                    with global_variables.MUTEX_PLAYERS[player_id]:
                        global_variables.PLAYERS[player_id].position = player_position
                        global_variables.PLAYERS[player_id].movingRequest = False
                elif token == Message_Type.PLAYER_SCORE.value:
                    data = [str(bufferQueue.get()) for _ in range(2)]
                    player_id = int(data[0])
                    player_score = int(data[1])
                    with global_variables.MUTEX_PLAYERS[player_id]:
                        global_variables.PLAYERS[player_id].score = player_score
                elif token == Message_Type.PLAYER_JOIN.value:
                    data = [str(bufferQueue.get()) for _ in range(2)]
                    player_id = int(data[0])
                    name = str(data[1])
                    with global_variables.MUTEX_PLAYERS_LIST:
                        global_variables.PLAYERS[player_id] = Pacman(player_id, name)
                elif token == Message_Type.HOST_GAME_STARTED.value:
                    with global_variables.GAME_STARTED_LOCK:
                        global_variables.GAME_STARTED = True

    def connect(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        # establish TCP connection to the server
        # Host menu initialize game server
        # Client menu initialize game client

        try:
            self.socket.connect((self.host_ip, int(self.host_port)))

            while True:
                player_id = self.socket.recv(
                    global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
                )
                if player_id:
                    # print(player_id)
                    # print(player_id.decode())
                    with global_variables.MUTEX_PLAYER_ID:
                        global_variables.PLAYER_ID = int(player_id.decode())
                    break
            self.startListener()
            print("Connected to server")
        except Exception as e:
            print(e)
            return -1
        return 0

    def close_socket(self):
        self.socket.close()
        print("Closed socket.")


if __name__ == "__main__":
    host_ip = "127.0.0.1"
    host_port = 5555

    client = Game_Client(host_ip, host_port)

    # Send messages to the server
    while True:
        message = input("Send message to server: ")
        client.sendDataToServer(message)

    client.close_socket()
