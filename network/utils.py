from typing import Iterable


def concatBuffer(token, args):
    byte_array = bytearray((str(token) + " " + " ".join(args)).encode())
    return byte_array


def splitBuffer(buffer: bytearray):
    message = buffer.decode().split(" ")
    return message
