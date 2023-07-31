def concatBuffer(token, args=None):
    if args is not None:
        return (str(token) + " " + " ".join(args) + "\n").encode()
    else:
        return (str(token) + "\n").encode()


def splitBuffer(stringBuffer: str):
    messages = stringBuffer.split("\n")
    remainder = ""
    if stringBuffer[-1] != "\n":
        remainder = messages[-1]

    messages.pop(-1)
    return messages, remainder


def parseMessage(message):
    data = message.split(" ")
    # data = list(filter(lambda x: x != "", data))
    return data
