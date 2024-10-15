class PriorityQueueArray:

    def __init__(self, v, dist):
        self.PQ = {}
        self.nodes = v
        self.dist = dist
        self.make_queue(self.nodes, self.dist)

    def decrease_key(self, v, dist):
        self.PQ[v] = dist

    def pop_min(self):
        min_node = None
        least = float('inf')
        for i in self.PQ.keys():
            dist = self.PQ[i]
            if dist < least:
                least = dist
                min_node = i
        self.PQ.pop(min_node)
        return min_node

    def make_queue(self, v, dist):
        for node in v:
            self.PQ[node] = dist[node]

    def check_empty(self):
        return len(self.PQ)


class PriorityQueueHeap:
    def __init__(self, V, dist):
        self.index_dict = {}
        self.heap = []
        self.dist_dict = dist
        self.make_heap(V)

    def push(self, item):
        self.heap.append(item)
        self.index_dict[item] = len(self.heap)
        L = (self.index_dict[item] // 2) - 1
        if L == -1:
            L = 0
        while self.dist_dict[item] < self.dist_dict[self.heap[L]]:

            self.swap(self.index_dict[item] - 1, L)
            L = (self.index_dict[item] // 2) - 1
            if L == -1:
                L = 0

    def check_empty(self):
        return len(self.heap)

    def swap(self, child_index, parent_index):
        child_val = self.heap[child_index]
        parent_val = self.heap[parent_index]
        self.heap[child_index] = parent_val
        self.heap[parent_index] = child_val
        self.index_dict[child_val] = parent_index + 1
        self.index_dict[parent_val] = child_index + 1

    def pop_min(self):
        self.swap(0, len(self.heap) - 1)
        least = self.heap.pop()
        self.index_dict.pop(least)

        if len(self.heap) < 2:
            return least

        top = self.heap[0]

        if len(self.heap) == 2:
            child1 = self.heap[(self.index_dict[top] * 2) - 1]
            while self.dist_dict[top] > self.dist_dict[child1]:
                self.swap(self.index_dict[child1] - 1, self.index_dict[top] - 1)
                if len(self.heap) < (self.index_dict[top] * 2)-1:
                    break
                child1 = self.heap[(self.index_dict[top] * 2) - 1]

        if len(self.heap) > 2:
            child1 = self.heap[(self.index_dict[top] * 2) - 1]
            child2 = self.heap[(self.index_dict[top] * 2)]
            while self.dist_dict[top] > self.dist_dict[child1] or self.dist_dict[top] > self.dist_dict[child2]:
                lesser_child = child1
                if self.dist_dict[child2] < self.dist_dict[child1]:
                    lesser_child = child2
                # if self.index_dict[lesser_child]-1 < 0:
                #     break
                self.swap(self.index_dict[lesser_child] - 1, self.index_dict[top] - 1)
                if len(self.heap) - 1 >= ((self.index_dict[top] * 2) - 1):
                    child1 = self.heap[(self.index_dict[top] * 2) - 1]
                else:
                    break
                if len(self.heap) - 1 >= (self.index_dict[top] * 2):
                    child2 = self.heap[(self.index_dict[top] * 2)]
                else:
                    break

        # check to see if there is a second child.

        return least

    def decrease_key(self, v, dist):
        self.dist_dict[v] = dist
        L = (self.index_dict[v] // 2) - 1
        if L == -1:
            L = 0
        while self.dist_dict[v] < self.dist_dict[self.heap[L]]:

            self.swap(self.index_dict[v] - 1, L)
            L = (self.index_dict[v] // 2) - 1
            if L == -1:
                L = 0

    def make_heap(self, V):
        for i in V:
            self.push(i)
