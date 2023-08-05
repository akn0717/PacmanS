# adapted from https://realpython.com/python-sockets/
import errno
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

        # varible contans all the mutex lock for each cell
        self.mutex_server_canvas_cells = None

        self.board_data = None
        self.players = {}
        self.receiver_threads = []
        self.incommingThread = None
        self.isGameStarted = False
        self.connections_dict_mutex = Lock()

    def sendAndFlush(self, conn, message):
        try:
            conn.sendall(message)
        except:
            return

    def __listenIncommingConnection(self):
        while not (self.isGameStarted):
            if self.getNumberConnections() >= global_constants.MAX_NUM_PLAYERS:
                continue
            try:
                (
                    conn,
                    _,
                ) = (
                    self.socket.accept()
                )  # accept the connection if any, this is blocking with timeout as set in the line 327, because we want to stop the thread when we don't want more connections
            except socket.timeout:  # timeout exception just continue looping
                continue
            except:
                return  # if there is any critical exception, just return

            conn.setblocking(0)

            # Exchange initial messages which are initial board state, player id, spawning player position.
            ## Picking a new player id for new connection, player_id is the key of the player in player dictionary, also the key of the player in the connection dictionary
            player_id = -1
            for i in range(4):
                if i not in self.players:
                    player_id = i
                    break

            with self.connections_dict_mutex:
                self.connections[player_id] = conn
            player = Pacman(player_id)
            self.players[player_id] = player
            print("Player", player_id + 1, "joined!")
            ## send a message to current connection player to let it know its id
            message = concatBuffer(Message_Type.PLAYER_ID.value, [str(player_id)])
            self.sendAndFlush(conn, message)

            ## send a message to the current player to update its initial board
            args = [
                self.board_data.shape[0],
                self.board_data.shape[1],
                *(self.board_data.flatten().tolist()),
            ]
            args = [str(arg) for arg in args]
            message = concatBuffer(Message_Type.INITIAL_BOARD.value, args)
            self.sendAndFlush(conn, message)

            ## send a message to current connection player to let it know about all the join players (except the current connection player)
            for key in self.players:
                if player_id == key:
                    continue
                args = [str(key)]
                message = concatBuffer(Message_Type.PLAYER_JOIN.value, args)
                self.sendAndFlush(conn, message)

            ## send a message to all the joined players, let them know about new player joins (including the current connection player)
            args = [str(player.id)]
            message = concatBuffer(Message_Type.PLAYER_JOIN.value, args)

            with self.connections_dict_mutex:
                for key in self.connections:
                    self.sendAndFlush(self.connections[key], message)

            # pop a random position from the potential spawning list and assign it to the current player
            self.players[player_id].position = self.potential_player_positions.pop(0)

            ## block the current position meaning the current player is holding it
            self.mutex_server_canvas_cells[self.players[player_id].position[0]][
                self.players[player_id].position[1]
            ].acquire()
            self.obstacle_data[self.players[player_id].position[0]][
                self.players[player_id].position[1]
            ] = 1
            ## release the block after setting the state to occupied
            self.mutex_server_canvas_cells[self.players[player_id].position[0]][
                self.players[player_id].position[1]
            ].release()

            # send a message to all the joined players acknowledging the current connection player's position
            args = [
                player_id,
                *self.players[player_id].position,
            ]
            args = [str(arg) for arg in args]
            message = concatBuffer(Message_Type.PLAYER_POSITION.value, args)
            with self.connections_dict_mutex:
                for key in self.connections:
                    self.sendAndFlush(self.connections[key], message)

            # start a new thread to keep listening to the current connection player
            thread = threading.Thread(target=self.__client_listen, args=(player_id,))
            self.receiver_threads.append(thread)
            thread.start()

    # each client listener is a thread running this function, it keeps listening to each client
    def __client_listen(self, player_id):
        messageQueue = []
        bufferRemainder = ""

        # looping receiving messages from clients
        while True:
            # shutdown the thread if the host close the game
            with global_variables.QUIT_GAME_LOCK:
                if global_variables.QUIT_GAME:
                    self.close_socket()
                    return
            try:
                with self.connections_dict_mutex:
                    recv_data = self.connections[player_id].recv(
                        global_constants.NUM_DEFAULT_COMMUNICATION_BYTES
                    )  # try to receive, this is non-blocking as set in line 52, we don't want the thread to be blocked as we don't want to stop the thread from processing the current messages
                if recv_data:
                    # concat the remainder buffer (incomplete message) with the new buffer and process the whole
                    messages, remainder = splitBuffer(
                        bufferRemainder + recv_data.decode()
                    )
                    bufferRemainder = remainder
                    for i in range(len(messages)):
                        messageQueue.append(
                            messages[i]
                        )  # enqueue the newly received messages to the message queue
            except socket.error as e:
                err = e.args[0]
                if (
                    err == errno.EAGAIN or err == errno.EWOULDBLOCK
                ):  # normal error dealing with non-blocking socket
                    continue
                else:  # if there is other exception, the player may lost connection or some other issues, just kick it out of the current session
                    with self.connections_dict_mutex:
                        position = self.players[player_id].position

                        # remove the occupation of the current player in its current position
                        self.mutex_server_canvas_cells[position[0]][
                            position[1]
                        ].acquire()  # acquire the lock of modifying the cell state
                        self.obstacle_data[
                            position[0],
                            position[1],
                        ] = 0  # modify it to empty
                        self.mutex_server_canvas_cells[position[0]][
                            position[1]
                        ].release()  # release the lock

                        self.connections.pop(
                            player_id
                        )  # remove the player from the connection and player dictionary
                        self.players.pop(player_id)

                        message = concatBuffer(
                            Message_Type.PLAYER_DISCONNECT.value, [str(player_id)]
                        )  # send a message to all players telling the player was disconnected
                        for key in self.connections:
                            self.sendAndFlush(self.connections[key], message)

                    print("Player", player_id + 1, "disconnected!")
                    return

            # process one by one the message in message queue
            while len(messageQueue) > 0:
                data = [int(arg) for arg in parseMessage(messageQueue.pop(0))]
                token = data[0]
                data = data[1:]

                # if the token is request player move type
                if token == Message_Type.REQUEST_PLAYER_MOVE.value:
                    player_id = int(data[0])
                    new_position = (int(data[1]), int(data[2]))
                    old_position = self.players[
                        player_id
                    ].position  # old position is the current player position

                    # check if the requested move is a valid move (not going out of bounds and not going through wall)
                    if isValidMove(self.board_data, (new_position[0], new_position[1])):
                        self.mutex_server_canvas_cells[old_position[0]][
                            old_position[1]
                        ].acquire()  # acquire the lock for the old position cell
                        self.mutex_server_canvas_cells[new_position[0]][
                            new_position[1]
                        ].acquire()  # acquire the lock for the new position cell
                        if self.obstacle_data[new_position[0]][new_position[1]] == 0:
                            self.obstacle_data[
                                old_position[0], old_position[1]
                            ] = 0  # set the old position cell to empty
                            self.obstacle_data[
                                new_position[0], new_position[1]
                            ] = 1  # set the new position cell as occupied
                            self.players[player_id].position = (
                                new_position[0],
                                new_position[1],
                            )
                            # increment the score based on the movement
                            if (
                                self.board_data[new_position[0]][new_position[1]]
                                == Block_Type.DOT.value
                            ):
                                self.board_data[new_position[0]][
                                    new_position[1]
                                ] = 0  # set the current board cell to empty
                                self.players[
                                    player_id
                                ].score += (
                                    1  # update the score of the player accordingly
                                )
                            # increment the score based on the movement
                            elif (
                                self.board_data[new_position[0]][new_position[1]]
                                == Block_Type.BIG_DOT.value
                            ):
                                self.board_data[new_position[0]][
                                    new_position[1]
                                ] = 0  # set the current board cell to empty
                                self.players[
                                    player_id
                                ].score += (
                                    3  # update the score of the player accordingly
                                )

                            # encapsulate the score to send
                            args = [
                                str(player_id),
                                str(self.players[player_id].score),
                            ]
                            message = concatBuffer(
                                Message_Type.PLAYER_SCORE.value, args
                            )
                            with self.connections_dict_mutex:
                                for key in self.connections:
                                    self.sendAndFlush(
                                        self.connections[key], message
                                    )  # send to all players the score of current player

                            # encapsulate the positon to send
                            args = [
                                str(player_id),
                                str(new_position[0]),
                                str(new_position[1]),
                            ]
                            message = concatBuffer(
                                Message_Type.PLAYER_POSITION.value, args
                            )
                            # send position of player move
                            with self.connections_dict_mutex:
                                for key in self.connections:
                                    self.sendAndFlush(
                                        self.connections[key], message
                                    )  # send to all players the position of current player

                        self.mutex_server_canvas_cells[new_position[0]][
                            new_position[1]
                        ].release()  # release the lock for the new position cell
                        self.mutex_server_canvas_cells[old_position[0]][
                            old_position[1]
                        ].release()  # release the lock for the old position cell

    # this function is to automatically create a board maze with all the empty blocks are connected to each other meaning if there is an empty block, there should be a path to it
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

    # create a random maze using dfs
    def populateCanvas(self):
        # set the border lines to be 1s
        for i in range(self.board_data.shape[0]):
            self.board_data[0, i] = self.board_data[i, 0] = 1
            self.board_data[i, self.board_data.shape[0] - 1] = self.board_data[
                self.board_data.shape[0] - 1, i
            ] = 1

        # pick any position on the board and start dfs from there
        i, j = np.random.randint(1, self.board_data.shape[0] - 2), np.random.randint(
            1, self.board_data.shape[0] - 2
        )
        self.board_data[i, j] = 0
        self.__dfsPopulation(i - 1, j)
        self.__dfsPopulation(i + 1, j)
        self.__dfsPopulation(i, j - 1)
        self.__dfsPopulation(i, j + 1)

    # this function return a list of tuples that are free to be spawned in
    def getPotentialSpawnPositions(self):
        (n, m) = self.board_data.shape
        potential_positions = []
        for i in range(n):
            for j in range(m):
                if self.board_data[i, j] != Block_Type.WALL.value:
                    potential_positions.append((i, j))
        random.shuffle(potential_positions)
        return potential_positions

    def initialize_dots(self):  #
        weight = [0.9, 0.1]  # [2, 3]
        zero_list = self.board_data[self.board_data == 0]
        self.board_data[self.board_data == 0] = np.random.choice(
            [2, 3], size=len(zero_list), p=weight
        )
        # self.board_data[self.board_data == 0] = dot_type

    # sometime players may spawn on the dots, should remove the dots before players spawn
    def remove_spawn_dots(self):
        for i in self.players:
            player_x = self.players[i].position[0]
            player_y = self.players[i].position[1]
            self.board_data[player_x][player_y] = 0

    # initialize the game data in the server
    def initializeGameData(self):
        print("initializing game data...")
        self.board_data = np.ones(shape=global_constants.CANVAS_SIZE, dtype=np.int32)
        self.obstacle_data = np.zeros_like(self.board_data)
        self.__dd = np.zeros_like(self.board_data)
        self.populateCanvas()
        self.initialize_dots()

        self.potential_player_positions = self.getPotentialSpawnPositions()

        # varible contans all the mutex lock for each cell, a 2d array, each cell is a lock of the corresponding cell on the board data
        self.mutex_server_canvas_cells = [
            [Lock() for _ in range(self.board_data.shape[1])]
            for _ in range(self.board_data.shape[0])
        ]

    def startConnectionListener(self):
        print("Server Started")
        print("-----------------")
        # bind the socket to the specified address and port
        self.socket.bind(("", self.port))
        # set a timeout for accepting connection
        self.socket.settimeout(5)
        self.socket.listen()
        # start a thread to handle accepting incoming connections
        self.incommingThread = threading.Thread(target=self.__listenIncommingConnection)
        self.incommingThread.start()

    def getNumberConnections(self):
        # return current number of active connections with the server
        return len(self.connections)

    def startGame(self):
        # when host starts game, send a message to all clients to start game
        game_started_message = concatBuffer(Message_Type.HOST_GAME_STARTED.value)
        with self.connections_dict_mutex:
            for key in self.connections:
                print("Game started")
                self.sendAndFlush(self.connections[key], game_started_message)
        # start a thread to check if game over condition met
        game_over_thread = threading.Thread(target=self._check_if_game_over)
        game_over_thread.start()
        self.isGameStarted = True

    def _check_if_game_over(self):
        # check if game over condition met
        while True:
            number_of_remaining_small_dots = np.count_nonzero(
                global_variables.CANVAS.board_data == 2
            )
            number_of_remaining_big_dots = np.count_nonzero(
                global_variables.CANVAS.board_data == 3
            )
            number_of_remaining_dots = (
                number_of_remaining_small_dots + number_of_remaining_big_dots
            )
            # if no big dots or small dots remain, send message to all active players
            # to stop the game as it is game over
            if number_of_remaining_dots == 0:
                message = concatBuffer(Message_Type.GAME_OVER.value)
                with self.connections_dict_mutex:
                    for key in self.connections:
                        self.sendAndFlush(self.connections[key], message)
                print("Game over")
                return
            # if game is quit by host, automatically return the thread
            with global_variables.QUIT_GAME_LOCK:
                if global_variables.QUIT_GAME:
                    return
            # check if game_over condition met every 5 seconds
            threading.Event().wait(5)

    def close_socket(self):
        with self.connections_dict_mutex:
            for player_id in self.connections:
                self.connections[player_id].close()
        self.socket.close()

    def __del__(self):
        self.close_socket()
        if self.incommingThread is not None:
            self.incommingThread.join()
            self.incommingThread = None
        for thread in self.receiver_threads:
            thread.join()


if __name__ == "__main__":
    server = Game_Server(5555)
    server.startConnectionListener()
