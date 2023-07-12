import argparse

from canvas import Canvas


def run(args):
    canvas = Canvas(20)
    canvas.populateCanvas()
    canvas.draw()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    run(args)
