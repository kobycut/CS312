import numpy as np


class matrix():
    def __init__(self, parent_matrix, row, col, lower_bound):
        self.matrix = np.array(parent_matrix)
        self.lower_bound = lower_bound
        self.row = row
        self.col = col
    def row_reduce(self):
        for i in range(len(self.matrix)):
            if 0 not in self.matrix[i]:
                min_value = float('inf')
                for val in self.matrix[i]:
                    if val == float('inf'):
                        continue
                    if val < min_value:
                        min_value = val
                if min_value != float('inf'):
                    self.lower_bound += min_value
                for j in range(len(self.matrix[i])):
                    if self.matrix[i][j] == float('inf'):
                        continue
                    val = self.matrix[i][j]
                    val -= min_value
                    self.matrix[i][j] = val
    def col_reduce(self):
        self.matrix = self.matrix.transpose()
        self.row_reduce()
        self.matrix = self.matrix.transpose()
    def cross_out(self):
        for i in range(len(self.matrix)):
            self.matrix[self.row][i] = float('inf')
            self.matrix = self.matrix.transpose()
            self.matrix[self.col][i] = float('inf')
            self.matrix = self.matrix.transpose()
        self.matrix[self.row][self.col] = float('inf')
        self.matrix[self.col][self.row] = float('inf')

#
# matrix([[float('inf'), 3, 2, 4], [float('inf'), float('inf'), 1, 7], [3, 7, float('inf'), 1],
#         [5, 2, float('inf'), float('inf')]], 2, 3, None)
