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
        flush(conn)

    def __listenIncommingConnection(self):
        while True:
            conn, _ = self.socket.accept()

            player_id = -1
            for i in range(4):
                if i not in self.players:
                    player_id = i
                    break
            self.connections[player_id] = conn

            player = Pacman(player_id)
            self.players[player_id] = player

            message = concatBuffer(Message_Type.PLAYER_ID.value, [str(player_id)])
            self.sendAndFlush(conn, message)

            args = [
                self.board_data.shape[0],
                self.board_data.shape[1],
                *(self.board_data.flatten().tolist()),
            ]
            args = [str(arg) for arg in args]
            message = concatBuffer(Message_Type.INITIAL_BOARD.value, args)
            self.sendAndFlush(conn, message)

            for key in self.players:
                if player_id == key:
                    continue
                player_joined_args = [str(key)]
                player_joined_message = concatBuffer(
                    Message_Type.PLAYER_JOIN.value, player_joined_args
                )
                self.sendAndFlush(conn, player_joined_message)

            player_joined_args = [str(player.id)]
            player_joined_message = concatBuffer(
                Message_Type.PLAYER_JOIN.value, player_joined_args
            )
            for key in self.connections:
                self.sendAndFlush(self.connections[key], player_joined_message)

            self.players[player_id].position = self.potential_player_positions.pop(0)
            player_position_message = [
                player_id,
                *self.players[player_id].position,
            ]
            args = [str(arg) for arg in player_position_message]

            self.mutex_server_canvas_cells[self.players[player_id].position[0]][
                self.players[player_id].position[1]
            ].acquire()
            message = concatBuffer(Message_Type.PLAYER_POSITION.value, args)
            self.sendAndFlush(conn, message)
            thread = threading.Thread(target=self.__listen, args=(player_id,))
            self.receiver_threads.append(thread)
            thread.start()

    def __listen(self, player_id):
        bufferQueue = []
        while True:
            try:
                recv_data = self.connections[player_id].recv(
                    global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
                )
                if recv_data:
                    data = splitBuffer(recv_data)
                    for i in range(len(data)):
                        bufferQueue.append(data[i])
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

            if (
                len(bufferQueue) > 0
                and len(bufferQueue) >= Message_Type.NUM_ARGS.value[int(bufferQueue[0])]
            ):
                token = int(bufferQueue.pop(0))
                data = [
                    int(bufferQueue.pop(0))
                    for _ in range(Message_Type.NUM_ARGS.value[token] - 1)
                ]
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

                        # UPDATE BLOCK FOR UPDATE a block from dot to empty for scoring
                        # self.board_data[
                        #     old_position[0], old_position[1]
                        # ] = Block_Type.EMPTY.value
                        # message = concatBuffer(
                        #     Message_Type.UPDATE_BLOCK.value,
                        #     [
                        #         str(position_x),
                        #         str(position_y),
                        #         str(Block_Type.EMPTY.value),
                        #     ],
                        # )
                        # for conn in self.connections:
                        #     conn.sendall(message)

                        # bad practice, needs to change later
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
                        args = [str(player_id), str(position_x), str(position_y)]
                        message = concatBuffer(Message_Type.PLAYER_POSITION.value, args)
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
                if self.board_data[i, j] == 0:
                    potential_positions.append((i, j))
        random.shuffle(potential_positions)
        return potential_positions

    def initializeGameData(self):
        self.board_data = np.ones(shape=global_constants.CANVAS_SIZE, dtype=np.int32)
        self.__dd = np.zeros_like(self.board_data)
        self.populateCanvas()
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
        print("Closed socket.")


if __name__ == "__main__":
    server = Game_Server(5555)
    server.startConnectionListener()
