def concatBuffer(token, args=None):
    if args is not None:
        return bytearray((str(token) + " " + " ".join(args)).encode())
    else:
        return bytearray(str(token)).encode()


def splitBuffer(buffer: bytearray):
    message = buffer.decode().split(" ")
    message = list(filter(lambda x: x != "", message))
    return message


def flush(socket):  # fake flush
    socket.sendall(" ".encode())
    return
