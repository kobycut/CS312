# Uncomment this line to import some functions that can help
# you debug your algorithm
import time

import numpy as np
# from matplotlib import pyplot as plt

import generate
from plotting import draw_line, draw_hull, circle_point


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def get_data(self):
        return self.data


class LinkedList:
    def __init__(self, tail, head):
        self.head = head
        self.tail = tail


def count_nodes(head):
    data = head.get_data()
    size = 1
    while True:
        head = head.next
        head_data = head.get_data()
        if data == head_data:
            break
        size += 1
    return size


def x_coord(point):
    return point[0]


def get_slope(x1, x2, y1, y2):
    return (y2 - y1) / (x2 - x1)


def find_upper_tangent(l, r):
    p = l.head
    q = r.tail

    px = p.get_data()[0]
    py = p.get_data()[1]
    qx = q.get_data()[0]
    qy = q.get_data()[1]

    qxnext = q.next.get_data()[0]
    qynext = q.next.get_data()[1]

    pxprev = p.prev.get_data()[0]
    pyprev = p.prev.get_data()[1]

    done = False

    while not done:
        done = True
        while True:
            current_slope = get_slope(px, qx, py, qy)  # get slope of temp line
            new_slope = get_slope(pxprev, qx, pyprev, qy)  # get slope of neighbor line
            if current_slope > new_slope:
                r = p.prev

                p = r
                px = p.get_data()[0]
                py = p.get_data()[1]
                pxprev = p.prev.get_data()[0]
                pyprev = p.prev.get_data()[1]
                done = False
            else:
                break
        while True:
            current_slope = get_slope(px, qx, py, qy)
            new_slope = get_slope(px, qxnext, py, qynext)
            if current_slope < new_slope:
                r = q.next

                q = r
                qx = q.get_data()[0]
                qy = q.get_data()[1]
                qxnext = q.next.get_data()[0]
                qynext = q.next.get_data()[1]
                done = False
            else:
                break

    return p, q


def find_lower_tangent(l, r):
    p = l.head
    q = r.tail
    px = p.get_data()[0]
    py = p.get_data()[1]
    qx = q.get_data()[0]
    qy = q.get_data()[1]

    qxprev = q.prev.get_data()[0]
    qyprev = q.prev.get_data()[1]

    pxnext = p.next.get_data()[0]
    pynext = p.next.get_data()[1]

    done = False

    while not done:
        done = True
        while True:
            current_slope = get_slope(px, qx, py, qy)  # get slope of temp line
            new_slope = get_slope(pxnext, qx, pynext, qy)  # get slope of neighbor line
            if current_slope < new_slope:
                r = p.next

                p = r
                px = p.get_data()[0]
                py = p.get_data()[1]
                pxnext = p.next.get_data()[0]
                pynext = p.next.get_data()[1]

                done = False
            else:
                break
        while True:
            current_slope = get_slope(px, qx, py, qy)
            new_slope = get_slope(px, qxprev, py, qyprev)
            if current_slope > new_slope:
                r = q.prev
                q = r
                qx = q.get_data()[0]
                qy = q.get_data()[1]
                qxprev = q.prev.get_data()[0]
                qyprev = q.prev.get_data()[1]
                done = False
            else:
                break
    return p, q


def merge(l, r):
    upper_left_tangent, upper_right_tangent = find_upper_tangent(l, r)
    lower_left_tangent, lower_right_tangent = find_lower_tangent(l, r)

    upper_left_tangent.next = upper_right_tangent
    upper_right_tangent.prev = upper_left_tangent

    lower_left_tangent.prev = lower_right_tangent
    lower_right_tangent.next = lower_left_tangent

    hull = LinkedList(l.tail, r.head)
    return hull


def recursive_helper(points):
    if len(points) < 2:
        node = Node(points[0])
        node.next = node
        node.prev = node
        return LinkedList(node, node)
    mid = len(points) // 2
    L = recursive_helper(points[:mid])
    R = recursive_helper(points[mid:])

    H = merge(L, R)

    return H


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    start_time = time.time()
    """Return the subset of provided points that define the convex hull"""
    sorted_points = sorted(points, key=x_coord)
    H = recursive_helper(sorted_points)
    lst = []
    H_size = count_nodes(H.head)
    for i in range(H_size):
        head = H.head
        tup = (head.get_data()[0], head.get_data()[1])
        lst.append(tup)
        H.head = H.head.next
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"took {elapsed_time} seconds")
    return lst

# for empirical analysis tests:
# def run_tests():
#     n_lst = [10, 100, 1000, 10000, 100000, 500000, 1000000]
#     mean_times = []
#     for n in n_lst:
#         times = []
#         for i in range(5):
#
#             set = generate.generate_random_points('normal', n, None)
#
#             start = time.time()
#             compute_hull(set)
#             end = time.time()
#             elapsed = end - start
#             times.append(elapsed)
#         mean_times.append(np.mean(times))
#
#     plt.plot(n_lst, mean_times, marker='o')
#     plt.xlabel('Number of Points (n)')
#     plt.ylabel('Mean Time (seconds)')
#     plt.title('Empirical Analysis: Convex Hull Computation')
#     table_data = [[n, f"{mean_time:.6f}"] for n, mean_time in zip(n_lst, mean_times)]
#
#     # Create the table
#     table = plt.table(cellText=table_data, colLabels=["Number of Points (n)", "Mean Time (s)"],
#               loc="upper right", cellLoc="center", colLoc="center", bbox=[1, 0.2, 1.07, 0.5])
#     table.auto_set_column_width([0, 1])
#     # Adjust plot to make room for the table
#     plt.subplots_adjust(right=0.545)
#     plt.grid(True)
#     plt.show()
#
# run_tests()