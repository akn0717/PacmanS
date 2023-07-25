from typing import Iterable


def concatBuffer(token, args: Iterable[str]):
    byte_array = bytearray((str(token) + " " + args.join(" ")).encode())
    return byte_array


def splitBuffer(buffer: bytearray):
    message = buffer.decode().split(" ")
    print("PRINTING SPLIT MSG")
    print(message)
    token = int(message[0])
    args = message[1:]
    return token, args
