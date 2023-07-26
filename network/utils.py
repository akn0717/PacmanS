
def concatBuffer(token, args):
    byte_array = bytearray((str(token) + " " + " ".join(args)).encode())
    return byte_array


def splitBuffer(buffer: bytearray):
    message = buffer.decode().split(" ")
    message = list(filter(lambda x: x != "", message))
    return message


def flush(socket):  # fake flush
    socket.sendall(" ".encode())
    return
