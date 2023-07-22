# adapted from https://realpython.com/python-sockets/
import socket
import threading
import numpy as np
import game.global_constants as global_constants


class GameServer:
    def __init__(self, port):
        self.port = port
        self.connections = []


    def threadedConnection(self, conn):
        while True:
            recv_data = conn.recv(128)
            if recv_data:
                print("Message received from {}".format(conn))
                print("Message is {}".format(recv_data.decode("utf-8")))
            for connection in self.connections:
                if connection != conn:
                    connection.sendall(recv_data)
        conn.close()
        print("Connection closed.")

    def __dfsPopulation(self, i, j):
        if (
            i <= 0
            or i >= self.size - 1
            or j <= 0
            or j >= self.size - 1
            or self.__dd[i, j] == 1
        ):
            return 1
        self.__dd[i, j] = 1

        c = 0.8  # how many walls expected
        self.board_data[i, j] = np.random.choice(np.array([0, 1]), p=[c, 1 - c])
        if self.data[i, j] == 0:
            self.__dfsPopulation(i - 1, j)
            self.__dfsPopulation(i + 1, j)
            self.__dfsPopulation(i, j - 1)
            self.__dfsPopulation(i, j + 1)

    def populateCanvas(self):
        # set the border lines
        for i in range(self.size):
            self.board_data[0, i] = self.data[i, 0] = 1
            self.board_data[i, self.size - 1] = self.data[self.size - 1, i] = 1

        i, j = np.random.randint(1, self.size - 2), np.random.randint(1, self.size - 2)
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
        return np.random.choice(potential_positions, num_players)

    def initializeGameData(self):
        self.board_data = np.ones(shape=global_constants.CANVAS_SIZE)
        self.__dd = np.zeros_like(self.board_data)
        self.populateCanvas()
        self.players = self.populatePlayerPosition(4)

    def startServer(self):
        # socket.SOCK_STREAM is TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # start server binding at specific port in TCP
        self.socket.bind(("", self.port))
        self.socket.listen()  # start listening for connection request
        print("Server Started")
        print("-----------------")
        while True:
            conn, _ = self.socket.accept()
            self.connections.append(conn)
            thread = threading.Thread(target=self.threadedConnection, args=(conn,))
            thread.start()

    def closeSocket(self):
        self.socket.close()
        print("Closed socket.")


if __name__ == "__main__":
    server = GameServer(5555)
    server.startServer()
