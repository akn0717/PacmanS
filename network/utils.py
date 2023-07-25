from typing import Iterable


def concatBuffer(token, args):
    byte_array = bytearray((str(token) + " " + " ".join(args)).encode())
    return byte_array


def splitBuffer(buffer: bytearray):
    message = buffer.decode().split(" ")
    token = int(message[0])
    args = message[1:]
    return token, args
