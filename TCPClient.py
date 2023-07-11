# adapted from https://realpython.com/python-sockets/
import sys
import socket
import threading


class TCPClient:
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        # socket.SOCK_STREAM is TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # establish TCP connection to the server
        self.socket.connect((self.host_ip, self.host_port))
        print("Connected to server")

        self.listen_thread = threading.Thread(target=self.listenToServer)
        self.listen_thread.start()

    def sendDataToServer(self, message):
        send_data = message.encode()
        self.socket.sendall(send_data)

    def listenToServer(self):
        while True:
            recv_data = self.socket.recv(128)
            if recv_data:
                print("Received message:", recv_data.decode("utf-8"))

    def close_socket(self):
        self.socket.close()
        print("Closed socket.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid Port No.")
        sys.exit(1)

    host_ip = "127.0.0.1"
    host_port = int(sys.argv[1])

    client = TCPClient(host_ip, host_port)

    # Send messages to the server
    while True:
        message = input("Send message to server: ")
        client.sendDataToServer(message)

    client.close_socket()
