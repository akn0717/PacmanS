# adapted from https://realpython.com/python-sockets/
import errno
import socket
import threading
from game.game_sprites import Pacman
from game.global_constants import Message_Type, Move_Operation, Direction
import game.global_constants as global_constants
import game.global_variables as global_variables
import numpy as np
from network.utils import *


class Game_Client:
    def __init__(self):
        # socket.SOCK_STREAM is TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.listening_thread = None

    def sendDataToServer(self, message):
        self.sendAndFlush(message)

    def startListener(self):
        self.socket.setblocking(0)
        self.listening_thread = threading.Thread(target=self.__listen)
        self.listening_thread.start()

    def sendAndFlush(self, message):
        try:
            self.socket.sendall(message)
        except:
            # with global_variables.GAME_OVER_LOCK:
            #     global_variables.GAME_OVER = True
            with global_variables.DISCONNECTED_FROM_HOST_LOCK:
                global_variables.DISCONNECTED_FROM_HOST = True

    def __listen(self):
        messageQueue = []
        bufferRemainder = ""
        while True:
            with global_variables.QUIT_GAME_LOCK:
                if global_variables.QUIT_GAME:
                    self.close_socket()
            try:
                recv_data = self.socket.recv(
                    global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
                )
                if recv_data:
                    messages, remainder = splitBuffer(
                        bufferRemainder + recv_data.decode()
                    )
                    bufferRemainder = remainder
                    for i in range(len(messages)):
                        messageQueue.append(messages[i])

                if recv_data == b"":
                    with global_variables.DISCONNECTED_FROM_HOST_LOCK:
                        global_variables.DISCONNECTED_FROM_HOST = True
                    return
            except socket.error as e:
                err = e.args[0]
                if (
                    err == errno.EAGAIN or err == errno.EWOULDBLOCK
                ):  # normal error dealing with non-blocking socket
                    continue
                else:
                    with global_variables.DISCONNECTED_FROM_HOST_LOCK:
                        global_variables.DISCONNECTED_FROM_HOST = True
                    return

            while len(messageQueue) > 0:
                message = messageQueue.pop(0)
                data = [int(arg) for arg in parseMessage(message)]
                token = data[0]
                data = data[1:]

                if token == Message_Type.INITIAL_BOARD.value:
                    with global_variables.MUTEX_CANVAS:
                        global_variables.CANVAS.board_data = np.reshape(
                            np.asarray(data[2:]), (data[0], data[1])
                        )

                elif token == Message_Type.PLAYER_POSITION.value:
                    player_id = int(data[0])
                    player_position = (int(data[1]), int(data[2]))
                    with global_variables.MUTEX_PLAYERS[player_id]:

                        # calculate the direction of the player
                        direction_op = (
                            player_position[0]
                            - global_variables.PLAYERS[player_id].position[0],
                            player_position[1]
                            - global_variables.PLAYERS[player_id].position[1],
                        )

                        if direction_op == Move_Operation.OPERATOR_LEFT.value:
                            global_variables.PLAYERS[
                                player_id
                            ].direction = Direction.LEFT.value
                        elif direction_op == Move_Operation.OPERATOR_RIGHT.value:
                            global_variables.PLAYERS[
                                player_id
                            ].direction = Direction.RIGHT.value
                        elif direction_op == Move_Operation.OPERATOR_UP.value:
                            global_variables.PLAYERS[
                                player_id
                            ].direction = Direction.UP.value
                        elif direction_op == Move_Operation.OPERATOR_DOWN.value:
                            global_variables.PLAYERS[
                                player_id
                            ].direction = Direction.DOWN.value

                        global_variables.PLAYERS[player_id].position = player_position
                        global_variables.MOVING_REQUEST = False

                    # update board_data
                    if (
                        global_variables.CANVAS.board_data[
                            global_variables.PLAYERS[player_id].position[0]
                        ][global_variables.PLAYERS[player_id].position[1]]
                        == 2
                    ):
                        global_variables.CANVAS.board_data[
                            global_variables.PLAYERS[player_id].position[0]
                        ][global_variables.PLAYERS[player_id].position[1]] = 0
                    elif (
                        global_variables.CANVAS.board_data[
                            global_variables.PLAYERS[player_id].position[0]
                        ][global_variables.PLAYERS[player_id].position[1]]
                        == 3
                    ):
                        global_variables.CANVAS.board_data[
                            global_variables.PLAYERS[player_id].position[0]
                        ][global_variables.PLAYERS[player_id].position[1]] = 0

                elif token == Message_Type.PLAYER_SCORE.value:
                    player_id = int(data[0])
                    player_score = int(data[1])
                    with global_variables.MUTEX_PLAYERS[player_id]:
                        global_variables.PLAYERS[player_id].score = player_score
                elif token == Message_Type.PLAYER_JOIN.value:
                    player_id = int(data[0])
                    with global_variables.MUTEX_PLAYERS_DICT:
                        global_variables.PLAYERS[player_id] = Pacman(player_id)

                elif token == Message_Type.HOST_GAME_STARTED.value:
                    with global_variables.GAME_STARTED_LOCK:
                        global_variables.GAME_STARTED = True

                elif token == Message_Type.PLAYER_ID.value:
                    with global_variables.MUTEX_PLAYER_ID:
                        global_variables.PLAYER_ID = int(data[0])
                elif token == Message_Type.PLAYER_DISCONNECT.value:
                    player_id = int(data[0])
                    with global_variables.MUTEX_PLAYERS_DICT:
                        global_variables.PLAYERS.pop(player_id)
                elif token == Message_Type.GAME_OVER.value:
                    print("GAME OVER RECIEVED")
                    with global_variables.GAME_OVER_LOCK:
                        global_variables.GAME_OVER = True

    def connect(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        # establish TCP connection to the server
        # Host menu initialize game server
        # Client menu initialize game client

        try:
            self.socket.connect((self.host_ip, int(self.host_port)))
            self.startListener()
            print("Connected to server")
        except Exception as e:
            print(e)
            return -1
        return 0

    def close_socket(self):
        self.socket.close()
        # print("Closed socket!")

    def __del__(self):
        self.close_socket()
        if self.listening_thread is not None:
            self.listening_thread.join()


if __name__ == "__main__":
    host_ip = "127.0.0.1"
    host_port = 5555

    client = Game_Client(host_ip, host_port)

    # Send messages to the server
    while True:
        message = input("Send message to server: ")
        client.sendDataToServer(message)

    client.close_socket()
