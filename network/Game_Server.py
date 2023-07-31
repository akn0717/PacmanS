# adapted from https://realpython.com/python-sockets/
from threading import Lock
import random
import socket
import threading
import numpy as np
from game.game_sprites import Pacman
from game.global_constants import Message_Type, Block_Type
import game.global_constants as global_constants
import game.global_variables as global_variables
from game.utils import isValidMove
from network.utils import *
import time


class Game_Server:
    def __init__(self, port):
        self.port = port
        self.connections = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mutex_server_canvas_cells = None
        self.board_data = None
        self.players = {}
        self.receiver_threads = []

    def sendAndFlush(self, conn, message):
        conn.sendall(message)

    def __listenIncommingConnection(self):
        while True:
            if self.getNumberConnections() >= 4:
                continue
            try:
                conn, _ = self.socket.accept()
            except:
                return

            # Picking a new player id for new connection
            player_id = -1
            for i in range(4):
                if i not in self.players:
                    player_id = i
                    break
            self.connections[player_id] = conn
            player = Pacman(player_id)
            self.players[player_id] = player
            print("Player", player_id + 1, "joined!")
            # send a message to current connection player to let it know its id
            message = concatBuffer(Message_Type.PLAYER_ID.value, [str(player_id)])
            self.sendAndFlush(conn, message)

            # send a message to the current player to update its initial board
            args = [
                self.board_data.shape[0],
                self.board_data.shape[1],
                *(self.board_data.flatten().tolist()),
            ]
            args = [str(arg) for arg in args]
            message = concatBuffer(Message_Type.INITIAL_BOARD.value, args)
            self.sendAndFlush(conn, message)

            # send a message to current connection player to let it know about all the join players (except the current connection player)
            for key in self.players:
                if player_id == key:
                    continue
                args = [str(key)]
                message = concatBuffer(Message_Type.PLAYER_JOIN.value, args)
                self.sendAndFlush(conn, message)

            # send a message to all the joined players, let them know about new player joins (including the current connection player)
            args = [str(player.id)]
            message = concatBuffer(Message_Type.PLAYER_JOIN.value, args)

            for key in self.connections:
                self.sendAndFlush(self.connections[key], message)

            # send a message to all the joined players acknowledging the current connection player's position
            self.players[player_id].position = self.potential_player_positions.pop(0)

            # block the current position meaning the current player is holding it
            self.mutex_server_canvas_cells[self.players[player_id].position[0]][
                self.players[player_id].position[1]
            ].acquire()
            args = [
                player_id,
                *self.players[player_id].position,
            ]
            args = [str(arg) for arg in args]
            message = concatBuffer(Message_Type.PLAYER_POSITION.value, args)
            for key in self.connections:
                self.sendAndFlush(self.connections[key], message)

            # start a new thread to keep listening to the current connection player
            thread = threading.Thread(target=self.__listen, args=(player_id,))
            self.receiver_threads.append(thread)
            thread.start()

    def __listen(self, player_id):
        messageQueue = []
        bufferRemainder = ""
        while True:
            try:
                recv_data = self.connections[player_id].recv(
                    global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
                )
                if recv_data:
                    messages, remainder = splitBuffer(
                        bufferRemainder + recv_data.decode()
                    )
                    bufferRemainder = remainder
                    for i in range(len(messages)):
                        messageQueue.append(messages[i])
            except:
                message = concatBuffer(
                    Message_Type.PLAYER_DISCONNECT.value, [str(player_id)]
                )
                self.connections.pop(player_id)
                self.players.pop(player_id)
                for key in self.connections:
                    self.sendAndFlush(self.connections[key], message)
                print("Player", player_id + 1, "disconnected!")
                return

            while len(messageQueue) > 0:
                data = [int(arg) for arg in parseMessage(messageQueue.pop(0))]
                token = data[0]
                data = data[1:]
                if token == Message_Type.REQUEST_PLAYER_MOVE.value:
                    player_id = int(data[0])
                    position_x = int(data[1])
                    position_y = int(data[2])

                    if isValidMove(self.board_data, (position_x, position_y)) and not (
                        self.mutex_server_canvas_cells[position_x][position_y].locked()
                    ):
                        self.mutex_server_canvas_cells[position_x][position_y].acquire()
                        old_position = (
                            self.players[player_id].position[0],
                            self.players[player_id].position[1],
                        )

                        if self.mutex_server_canvas_cells[old_position[0]][
                            old_position[1]
                        ].locked():
                            self.mutex_server_canvas_cells[old_position[0]][
                                old_position[1]
                            ].release()

                        self.players[player_id].position = (
                            position_x,
                            position_y,
                        )

                        # increment the score based on the movement
                        if self.board_data[position_x][position_y] == 2:
                            self.board_data[position_x][position_y] = 0
                            self.players[player_id].score += 1

                        # encapsulate the positon to send
                        args = [str(player_id), str(position_x), str(position_y)]
                        message = concatBuffer(Message_Type.PLAYER_POSITION.value, args)

                        # send position of player move
                        for i in self.connections:
                            self.sendAndFlush(self.connections[i], message)

                        # encapsulate the score to send
                        args = [str(player_id), str(self.players[player_id].score)]
                        message = concatBuffer(Message_Type.PLAYER_SCORE.value, args)

                        for key in self.connections:
                            self.sendAndFlush(self.connections[key], message)

    def __dfsPopulation(self, i, j):
        if (
            i <= 0
            or i >= self.board_data.shape[0] - 1
            or j <= 0
            or j >= self.board_data.shape[1] - 1
            or self.__dd[i, j] == 1
        ):
            return 1
        self.__dd[i, j] = 1

        c = 0.8  # how many walls expected
        self.board_data[i, j] = np.random.choice(np.array([0, 1]), p=[c, 1 - c])
        if self.board_data[i, j] == 0:
            self.__dfsPopulation(i - 1, j)
            self.__dfsPopulation(i + 1, j)
            self.__dfsPopulation(i, j - 1)
            self.__dfsPopulation(i, j + 1)

    def populateCanvas(self):
        # set the border lines
        for i in range(self.board_data.shape[0]):
            self.board_data[0, i] = self.board_data[i, 0] = 1
            self.board_data[i, self.board_data.shape[0] - 1] = self.board_data[
                self.board_data.shape[0] - 1, i
            ] = 1

        i, j = np.random.randint(1, self.board_data.shape[0] - 2), np.random.randint(
            1, self.board_data.shape[0] - 2
        )
        self.board_data[i, j] = 0
        self.__dfsPopulation(i - 1, j)
        self.__dfsPopulation(i + 1, j)
        self.__dfsPopulation(i, j - 1)
        self.__dfsPopulation(i, j + 1)

    def getPotentialSpawnPositions(self):
        (n, m) = self.board_data.shape
        potential_positions = []
        for i in range(n):
            for j in range(m):
                if self.board_data[i, j] == Block_Type.DOT.value:
                    potential_positions.append((i, j))
        random.shuffle(potential_positions)
        return potential_positions

    def initialize_dots(self):
        self.board_data[self.board_data == 0] = 2

    def remove_spawn_dots(self):
        for i in self.players:
            player_x = self.players[i].position[0]
            player_y = self.players[i].position[1]
            self.board_data[player_x][player_y] = 0

    def initializeGameData(self):
        print("initializing game data...")
        self.board_data = np.ones(shape=global_constants.CANVAS_SIZE, dtype=np.int32)
        self.__dd = np.zeros_like(self.board_data)
        self.populateCanvas()
        self.initialize_dots()

        self.potential_player_positions = self.getPotentialSpawnPositions()

        self.mutex_server_canvas_cells = [
            [Lock() for _ in range(self.board_data.shape[1])]
            for _ in range(self.board_data.shape[0])
        ]

    def startConnectionListener(self):
        print("Server Started")
        print("-----------------")
        # for testing
        self.socket.bind(("", self.port))
        self.socket.listen()
        thread = threading.Thread(target=self.__listenIncommingConnection)
        thread.start()

    def getNumberConnections(self):
        return len(self.connections)

    def startGame(self):
        game_started_message = concatBuffer(Message_Type.HOST_GAME_STARTED.value)

        for key in self.connections:
            print("GAME STARTED")
            self.sendAndFlush(self.connections[key], game_started_message)

    def closeSocket(self):
        self.socket.close()
        # print("Closed socket.")


if __name__ == "__main__":
    server = Game_Server(5555)
    server.startConnectionListener()
