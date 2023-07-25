# adapted from https://realpython.com/python-sockets/
from multiprocessing import Lock
import random
import socket
import threading
import numpy as np
from game.game_sprites import Pacman
from game.global_constants import Message_Type, Block_Type
import game.global_constants as global_constants
import game.global_variables as global_variables
from network.utils import *


class Game_Server:
    def __init__(self, port):
        self.port = port
        self.connections = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mutex_server_canvas_cells = None
        self.board_data = None
        self.players = []

    def __listenIncommingConnection(self):
        while True:
            conn, _ = self.socket.accept()
            self.connections.append(conn)
            global_variables.NUMBER_CONNECTIONS += 1
            player_id = (
                len(self.connections) - 1
            )  # player id is set to the connection index
            player = Pacman(player_id, "")
            self.players.append(player)
            conn.send(str(player_id).encode())
            player_joined_message = concatBuffer(
                Message_Type.PLAYER_JOIN, player.id + " " + player.name
            )
            for i in range(self.connections):
                self.connections[i].send(player_joined_message)

            # Send initial board
            args = [
                self.board_data.shape[0],
                self.board_data.shape[1],
                *(self.board_data.flatten().tolist()),
            ]
            board_data_message = concatBuffer(Message_Type.INITIAL_BOARD, args)
            conn.send(board_data_message)
            thread = threading.Thread(target=self.__listen, args=(player_id,))
            thread.start()

    def __listen(self, player_id):
        while True:
            recv_data = self.connections(player_id).recv(
                global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
            )
            if recv_data:
                token, data = splitBuffer(recv_data)
                if token == Message_Type.REQUEST_PLAYER_MOVE:
                    player_id, position_x, position_y = data
                    player_id = int(player_id)
                    position_x = int(position_x)
                    position_y = int(position_y)
                    if not (
                        self.mutex_server_canvas_cells[position_x][position_y].locked()
                    ):
                        self.mutex_server_canvas_cells[position_x][position_y].acquire()
                        old_position = (
                            self.players[int(player_id)].position[0],
                            self.players[int(player_id)].position[1],
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
                        #     conn.send(message)

                        self.mutex_server_canvas_cells[old_position[0]][
                            old_position[1]
                        ].release()
                        self.players[player_id] = (
                            position_x,
                            position_y,
                        )
                        message = concatBuffer(
                            Message_Type.PLAYER_POSITION.value, [position_x, position_y]
                        )
                        for conn in self.connections:
                            conn.send(message)

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

    def populatePlayerPosition(self, num_players):
        (n, m) = self.board_data.shape
        potential_positions = []
        for i in range(n):
            for j in range(m):
                if self.board_data[i, j] == 0:
                    potential_positions.append((i, j))
        return random.choices(potential_positions, k=num_players)

    def initializeGameData(self):
        self.board_data = np.ones(shape=global_constants.CANVAS_SIZE, dtype=np.int32)
        self.__dd = np.zeros_like(self.board_data)
        self.populateCanvas()
        self.players = self.populatePlayerPosition(global_constants.NUM_PLAYERS)
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

    def closeSocket(self):
        self.socket.close()
        print("Closed socket.")


if __name__ == "__main__":
    server = Game_Server(5555)
    server.startConnectionListener()
