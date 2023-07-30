# adapted from https://realpython.com/python-sockets/
from multiprocessing import Queue
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
        self.connections = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mutex_server_canvas_cells = None
        self.board_data = None
        self.players = []

    def sendAndFlush(self, conn, message):
        conn.sendall(message)
        flush(conn)

    def __listenIncommingConnection(self):

        while True:
            conn, _ = self.socket.accept()
            self.connections.append(conn)

            global_variables.NUMBER_CONNECTIONS += 1
            print(global_variables.NUMBER_CONNECTIONS)

            player_id = (
                len(self.connections) - 1
            )  # player id is set to the connection index
            player = Pacman(player_id, "test")
            self.players.append(player)
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

            player_joined_args = [str(player.id), "testname"]

            player_joined_message = concatBuffer(
                Message_Type.PLAYER_JOIN.value, player_joined_args
            )
            for conn in self.connections:
                self.sendAndFlush(conn, player_joined_message)

            player_position_message = [
                player_id,
                *self.potential_player_positions[player_id],
            ]
            args = [str(arg) for arg in player_position_message]
            self.players[player_id].position = self.potential_player_positions[
                player_id
            ]
            # self.mutex_server_canvas_cells[player_position_message[1]][
            #     player_position_message[2]
            # ].acquire()
            message = concatBuffer(Message_Type.PLAYER_POSITION.value, args)
            self.sendAndFlush(conn, message)
            thread = threading.Thread(target=self.__listen, args=(player_id,))
            thread.start()

    def __listen(self, player_id):
        bufferQueue = Queue()
        while True:
            recv_data = self.connections[player_id].recv(
                global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
            )
            if recv_data:
                data = splitBuffer(recv_data)
                print("Server received data:", recv_data)
                print("Server received parsed data", data)
                for i in range(len(data)):
                    bufferQueue.put(data[i])

            if not (bufferQueue.empty()):
                token = int(bufferQueue.get())

                if token == Message_Type.REQUEST_PLAYER_MOVE.value:
                    data = [bufferQueue.get() for _ in range(3)]
                    print("Server received Request Move:", data)
                    player_id = int(data[0])
                    position_x = int(data[1])
                    position_y = int(data[2])

                    if isValidMove(self.board_data, (position_x, position_y)):
                        # self.mutex_server_canvas_cells[position_x][position_y].acquire()
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
                        #     conn.sendall(message)

                        # bad practice, needs to change later
                        # if self.mutex_server_canvas_cells[old_position[0]][
                        #     old_position[1]
                        # ].locked():
                        #     self.mutex_server_canvas_cells[old_position[0]][
                        #         old_position[1]
                        #     ].release()

                        
                        self.players[player_id].position = (
                            position_x,
                            position_y,
                        )

                        # increment the score based on the movement
                        if self.board_data[position_x][position_y] == 2:
                            self.board_data[position_x][position_y] = 0
                            self.players[player_id].score += 1
                        # print("score value:", self.players[player_id].score)

                        # encapsulate the positon to send
                        args = [str(player_id), str(position_x), str(position_y)]
                        message = concatBuffer(Message_Type.PLAYER_POSITION.value, args)
                        print("Server move player to", self.players[player_id].position)
                        
                        # send position of player move
                        for i in range(len(self.connections)):
                            self.sendAndFlush(self.connections[i], message)
                            
                        # encapsulate the score to send
                        args = [str(player_id), str(self.players[player_id].score)]
                        message = concatBuffer(Message_Type.PLAYER_SCORE.value, args)

                        # send position of player move
                        for i in range(len(self.connections)):
                            self.sendAndFlush(self.connections[i], message)


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


    def initialize_dots(self):
        self.board_data[self.board_data == 0] = 2
        

    def remove_spawn_dots(self):
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", len(self.connections))
        for i in range(global_variables.NUMBER_CONNECTIONS):
            player_y = self.potential_player_positions[i][0]
            player_x = self.potential_player_positions[i][1]
            self.board_data[player_y][player_x] = 0

    def initializeGameData(self):
        print("initializing game data...")
        self.board_data = np.ones(shape=global_constants.CANVAS_SIZE, dtype=np.int32)
        self.__dd = np.zeros_like(self.board_data)
        self.populateCanvas()
        self.potential_player_positions = self.populatePlayerPosition(
            global_constants.NUM_PLAYERS
        )

        self.initialize_dots()


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

    def startGame(self):
        game_started_message = concatBuffer(Message_Type.HOST_GAME_STARTED.value)

        for conn in self.connections:
            print("GAME STARTED")
            self.sendAndFlush(conn, game_started_message)

    def closeSocket(self):
        self.socket.close()
        print("Closed socket.")


if __name__ == "__main__":
    server = Game_Server(5555)
    server.startConnectionListener()
