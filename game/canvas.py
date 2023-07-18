import numpy as np
from game.global_variables import CANVAS_SIZE


class Canvas:
    def __init__(self, data: np.ndarray = None, shape=CANVAS_SIZE, auto_populate=False):
        self.__data = np.ones(shape, dtype=np.int32)
        if data != None:
            self.__data = data.copy()
        self.shape = data.shape

        if auto_populate:
            self.__dd = np.zeros_like(self.data)
            self.populateCanvas()

    @classmethod
    def fromData(cls, data: np.ndarray):
        cls(data=data)

    @classmethod
    def fromSize(cls, shape: int):
        cls(shape=shape)

    def __blockType(self, i, j):
        code = 0
        if i - 1 >= 0:
            code |= self.data[i - 1][j] == 1
        if i + 1 < self.size:
            code |= (self.data[i + 1][j] == 1) << 1
        if j - 1 >= 0:
            code |= (self.data[i][j - 1] == 1) << 2
        if j + 1 < self.size:
            code |= (self.data[i][j + 1] == 1) << 3
        return code

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
        self.data[i, j] = np.random.choice(np.array([0, 1]), p=[c, 1 - c])
        if self.data[i, j] == 0:
            self.__dfsPopulation(i - 1, j)
            self.__dfsPopulation(i + 1, j)
            self.__dfsPopulation(i, j - 1)
            self.__dfsPopulation(i, j + 1)

    def populateCanvas(self):
        # set the border lines
        for i in range(self.size):
            self.__data[0, i] = self.data[i, 0] = 1
            self.__data[i, self.size - 1] = self.data[self.size - 1, i] = 1

        i, j = np.random.randint(1, self.size - 2), np.random.randint(1, self.size - 2)
        self.__data[i, j] = 0
        self.__dfsPopulation(i - 1, j)
        self.__dfsPopulation(i + 1, j)
        self.__dfsPopulation(i, j - 1)
        self.__dfsPopulation(i, j + 1)

    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                print(str(self.data[i, j]) + " ", end="")
            print()
