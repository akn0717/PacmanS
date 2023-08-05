# adapted from https://realpython.com/python-sockets/
import errno
import socket
import threading
from game.game_sprites import Pacman
from game.global_constants import Message_Type, Move_Operation, Direction, Block_Type
import game.global_constants as global_constants
import game.global_variables as global_variables
import numpy as np
from network.utils import *


class Game_Client:
    def __init__(self):
        # create TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_thread = None

    def sendDataToServer(self, message):
        self.sendAndFlush(message)

    def startListener(self):
        # start a thread to listen for incoming messages from the server
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
                    # if the client has quit game, close the socket
                    self.close_socket()
            try:
                recv_data = self.socket.recv(
                    global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
                )

                if recv_data:
                    # if data is recieved, split the incoming message using the delimiter. If the message has extra data, store the rest
                    # of the data as remainder to be used as prefix when the entire message comes in.
                    messages, remainder = splitBuffer(
                        bufferRemainder + recv_data.decode()
                    )
                    bufferRemainder = remainder
                    # push a full message into the messagequeue for further processing
                    for i in range(len(messages)):
                        messageQueue.append(messages[i])

                # if the received data is empty buffer meaning the host connection is lost
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
                    # if disconnected from host, stop listening to the socket
                    with global_variables.DISCONNECTED_FROM_HOST_LOCK:
                        global_variables.DISCONNECTED_FROM_HOST = True
                    return

            # process message one by one
            while len(messageQueue) > 0:
                # pop the message from the queue
                message = messageQueue.pop(0)
                # parse the message, splitting it up into the token and data
                data = [int(arg) for arg in parseMessage(message)]
                token = data[0]
                data = data[1:]

                # update the local canvas into the board sent by the server
                if token == Message_Type.INITIAL_BOARD.value:
                    with global_variables.MUTEX_CANVAS:
                        global_variables.CANVAS.board_data = np.reshape(
                            np.asarray(data[2:]), (data[0], data[1])
                        )
                # update the player position with the player id
                elif token == Message_Type.PLAYER_POSITION.value:
                    # parse the player_id and player_position from the message
                    player_id = int(data[0])
                    player_position = (int(data[1]), int(data[2]))
                    with global_variables.MUTEX_PLAYERS[player_id]:

                        # calculate the direction of the session players, except the local player which is set by keyboard
                        direction_op = (
                            player_position[0]
                            - global_variables.PLAYERS[player_id].position[0],
                            player_position[1]
                            - global_variables.PLAYERS[player_id].position[1],
                        )
                        # according to movement, we calculated direction, change the direction of the online player on the board, this is for visualizing direction of other players
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
                        # after move of the player is successful, turn off moving request.
                        global_variables.MOVING_REQUEST = False

                    # if cell contains small dot or big dot player will eat the dot
                    # and transform the cell into an empty cell
                    if (
                        global_variables.CANVAS.board_data[
                            global_variables.PLAYERS[player_id].position[0]
                        ][global_variables.PLAYERS[player_id].position[1]]
                        == Block_Type.DOT.value
                        or global_variables.CANVAS.board_data[
                            global_variables.PLAYERS[player_id].position[0]
                        ][global_variables.PLAYERS[player_id].position[1]]
                        == Block_Type.BIG_DOT.value
                    ):
                        global_variables.CANVAS.board_data[
                            global_variables.PLAYERS[player_id].position[0]
                        ][
                            global_variables.PLAYERS[player_id].position[1]
                        ] = Block_Type.EMPTY.value

                elif token == Message_Type.PLAYER_SCORE.value:
                    # update the local score of the player according to the
                    # player_id in the message
                    player_id = int(data[0])
                    player_score = int(data[1])
                    with global_variables.MUTEX_PLAYERS[player_id]:
                        global_variables.PLAYERS[player_id].score = player_score
                elif token == Message_Type.PLAYER_JOIN.value:
                    # if a new player has joined, create a new Pacman player locally
                    # for client with that player_id
                    player_id = int(data[0])
                    with global_variables.MUTEX_PLAYERS_DICT:
                        global_variables.PLAYERS[player_id] = Pacman(player_id)

                elif token == Message_Type.HOST_GAME_STARTED.value:
                    # if host starts the game, GAME_STARTED variable is set to true
                    # which starts gameplay in client_loading_menu
                    with global_variables.GAME_STARTED_LOCK:
                        global_variables.GAME_STARTED = True

                elif token == Message_Type.PLAYER_ID.value:
                    # client's player ID is granted by the server upon joining the game
                    with global_variables.MUTEX_PLAYER_ID:
                        global_variables.PLAYER_ID = int(data[0])
                elif token == Message_Type.PLAYER_DISCONNECT.value:
                    # if any player has disconnected, remove the player from the client's players dictionary, removing
                    # from the board as well
                    player_id = int(data[0])
                    with global_variables.MUTEX_PLAYERS_DICT:
                        global_variables.PLAYERS.pop(player_id)
                elif token == Message_Type.GAME_OVER.value:
                    # if game over message is recieved, turn global variable to game_over to true
                    # which is used by the gameplay_menu to navigate to the score_menu
                    with global_variables.GAME_OVER_LOCK:
                        global_variables.GAME_OVER = True

    def connect(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        # establish TCP connection to the server
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
        print("Closed socket!")

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
