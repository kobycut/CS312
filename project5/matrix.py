import numpy as np


class matrix():
    def __init__(self, array):

        self.matrix = np.array(array)
        self.lower_bound = 0
        self.row_reduce()
        self.col_reduce()

    #  check to make 0's infinities from first initialization
    def row_reduce(self):
        for i in range(len(self.matrix)):
            if 0 not in self.matrix[i]:
                min = float('inf')
                for val in self.matrix[i]:
                    if val == float('inf'):
                        continue
                    if val < min:
                        min = val
                self.lower_bound += min
                for j in range(len(self.matrix[i])):
                    if self.matrix[i][j] == float('inf'):
                        continue
                    val = self.matrix[i][j]
                    val -= min
                    self.matrix[i][j] = val

    def col_reduce(self):
        self.matrix = self.matrix.transpose()
        self.row_reduce()
        self.matrix = self.matrix.transpose()


matrix([[float('inf'), 3, 2, 4], [float('inf'), float('inf'), 1, 7], [3, 7, float('inf'), 1],
        [5, 2, float('inf'), float('inf')]])
