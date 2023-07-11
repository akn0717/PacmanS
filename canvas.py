import numpy as np


class Canvas:
    def __init__(self, size):
        self.size = size
        self.data = np.ones((self.size, self.size), dtype=np.int32)
        self.dd = np.zeros((self.size, self.size), dtype=np.int32)

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
            or self.dd[i, j] == 1
        ):
            return 1
        self.dd[i, j] = 1

        c = 0.8
        self.data[i, j] = np.random.choice(np.array([0, 1]), p=[c, 1 - c])
        if self.data[i, j] == 0:
            self.__dfsPopulation(i - 1, j)
            self.__dfsPopulation(i + 1, j)
            self.__dfsPopulation(i, j - 1)
            self.__dfsPopulation(i, j + 1)

    def populateCanvas(self):
        # set the border lines
        for i in range(self.size):
            self.data[0, i] = self.data[i, 0] = 1
            self.data[i, self.size - 1] = self.data[self.size - 1, i] = 1

        i, j = np.random.randint(1, self.size - 2), np.random.randint(1, self.size - 2)
        self.data[i, j] = 0
        self.__dfsPopulation(i - 1, j)
        self.__dfsPopulation(i + 1, j)
        self.__dfsPopulation(i, j - 1)
        self.__dfsPopulation(i, j + 1)

    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                print(str(self.data[i, j]) + " ", end="")
            print()
