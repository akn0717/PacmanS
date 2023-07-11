# adapted from https://realpython.com/python-sockets/
import socket
import threading


class TCPServer:
    def __init__(self, port):
        self.port = port
        # socket.SOCK_STREAM is TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # start server binding at specific port in TCP
        self.socket.bind(('', self.port))
        print("Server Started")
        print("-----------------")
        self.socket.listen()  # start listening for connection request
        self.connections = []

    def threadedConnection(self, conn):
        while True:
            recv_data = conn.recv(128)
            if recv_data:
                print("Message received from {}".format(conn))
                print("Message is {}".format(recv_data.decode("utf-8")))
            for connection in self.connections:
                if (connection != conn):
                    connection.sendall(
                        recv_data)
        conn.close()
        print("Connection closed.")

    def startServer(self):
        while True:
            conn, _ = self.socket.accept()
            self.connections.append(conn)
            thread = threading.Thread(
                target=self.threadedConnection, args=(conn,))
            thread.start()

    def closeSocket(self):
        self.socket.close()
        print("Closed socket.")


if __name__ == "__main__":
    server = TCPServer(5555)
    server.startServer()
